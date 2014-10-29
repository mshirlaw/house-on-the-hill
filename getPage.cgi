#!/usr/bin/perl
use warnings;
use strict;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use DB_File;

# Create CGI object
my $cgi = CGI->new;

# Extract cookie if it is present
my $cookie_present = $cgi->cookie("user");

# Set the pages directory
my $pages_directory = "./pages/";
my $domain = "getPage.cgi?page=";

# Test for invalid page number in GET request
# No such page: $validPage=0
# Page is valid: $validPage=1
# No page supplied: $validPage=2
my $validPage=0;

# Alphanumeric page number only
my $pageNum;
if(defined $cgi->param("page")){
    ($pageNum) = $cgi->param("page") =~ /([\w]{1,})/;
}
else{
    
    $pageNum = "";
    $validPage=2;
}

opendir(my $dir, $pages_directory) || die "Could not open pages directory.\n";
for my $page (readdir($dir)){
    if($page eq $pageNum){
	$validPage=1;
    } 
}

# Close the pages directory
closedir $dir;

# If there is already a cookie set, update it
if(defined $cookie_present){

    # Tie hash to DB_File
    my $UID = $cookie_present;
    tie (my %db_hash, "DB_File", "./profiles/" . $UID . ".db");

    if($validPage == 1){
	
	# Set page number to $pageNum
	$db_hash{"page"} = $pageNum;

	# Update expiry date - number of seconds since January 1, 1970 + 7 days.
	my $expiry = time() + 604800;
	$db_hash{"expiry"} = "$expiry";

	my $cookie = $cgi->cookie(-name => "user", -value => "$UID", -expires => "+7d");
	print $cgi->header(-cookie => $cookie);
    }
    else{
	
	# Store expiry date - number of seconds since January 1, 1970 + 7 days.
	my $expiry = time() + 604800;
	$db_hash{"expiry"} = "$expiry";

	my $cookie = $cgi->cookie(-name => "user", -value => "$UID", -expires => "+7d");
	print $cgi->header(-cookie => $cookie);
    }

    # Untie
    untie %db_hash;

}
else{

    # Delete expired profiles
    opendir(my $profiles_dir, "./profiles/") || die "Couldn't open directory.\n";
    for my $entry (readdir($profiles_dir)) {
	if(! -d $entry){
	    tie (my %db_hash, "DB_File", "./profiles/" . $entry);
	    if(defined $db_hash{"expiry"} && time() > $db_hash{"expiry"}){
		system("rm ./profiles/" . $entry);
	    }
	    untie %db_hash;
	}
    }

    # A random UID between 0 and 10000
    my $UID = int(rand(10000));

    # Check if that username already exists                                                                 
    while (-e "./profiles/$UID.db"){
	$UID = int(rand(10000));
    }
    
    # Tie hash to DB_File
    tie (my %db_hash, "DB_File", "./profiles/" . $UID . ".db");
   
    # Set page number to 1
    $db_hash{"page"} = 1;

    # Store expiry date - number of seconds since January 1, 1970 + 7 days.
    my $expiry = time() + 604800;
    $db_hash{"expiry"} = "$expiry";

    # Untie
    untie %db_hash;

    # Create a cookie with the new UID
    my $cookie = $cgi->cookie(-name => "user", -value => "$UID", -expires => "+7d");
    print $cgi->header(-cookie => $cookie);
}

# Set title and stylesheet
print $cgi->start_html("-title"=>"House on the Hill", 
		       "-style"=>"css/adventure.css",
		       "-script"=>[{"-type"=>"javascript", 
				    "-src"=>"//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"},
				   {"-type"=>"javascript", 
				    "-src"=>"javascript/toggle.js"},]);

# Set up the top div
print "<div id=\"top\">";
print "<div class=\"container\">";

print "<a href=\"index.cgi\"><img src=\"img/title_crop.png\" alt=\"House on the Hill\" id=\"title_img\"></a>";

print "<div class=\"nav-bar\">";
print $cgi->a({"href"=>"index.cgi"},"Home");
print $cgi->a({"href"=>"getPage.cgi?page=1"},"Start Over");
print $cgi->a({"href"=>"stats.cgi"},"Statistics");
print "</div>";

print $cgi->p({"id"=>"tagline"},"An adventure like no other.");
print $cgi->p({"id"=>"lesser_tag"},"This game will inspire and intrigue? Can you escape?");


# Don't display castle on pages
if($validPage > 1){
    print $cgi->img({"src"=>"img/castle.png","alt"=>"Adventure Background","id"=>"castle"});
}

print "</div>";
print "</div>";

# Set up the middle div
print "<div id=\"middle_cgi\">";
print "\t<div class=\"container\">";
print "\t\t<div class=\"scenario\">";

if($validPage == 1){
    
    # Open the correct page file for reading e.g. 1
    open(my $myPage, $pages_directory . $pageNum) || die "Cannot open page.\n";
    
    system("perl ./scripts/trackerAdd.pl $pageNum");

    # Store each line of this page as an array element
    my @array = <$myPage>;
    
    # Count the number of choices
    my $choices = 0;
    while (($array[$choices]) ne "\n" ){
	$choices=$choices+1;
    }
    
    # Split the choices into a hash
    my $counter = 0;
    my %hash = ();
    while($counter<$choices){
	my @line = split(' ', $array[$counter]);
	my $key = shift @line;
	$hash{$key} = "@line";
	$counter=$counter+1;
    }
    
    # Skip blank line
    $choices++;
    
    print "<div class=\"container\">";
    #print "<p class=\"story_page_header\">Page $pageNum...</p>";
    print "</div>";
    
    # Print scenario for this page
    while($choices < @array){
	print $cgi->p($array[$choices]);
	$choices++;
	# Print a blank line if necessary
	if(($choices == @array) && ($array[$choices-1] ne "\n")){
	    print "<br />";
	}
    }				    
    
    # Print each option sorted by key
    foreach my $option (sort keys %hash) {
	print "<img src=\"./img/arrow.png\" class=\"bullet\"><a href=\"$domain$option\">$hash{$option}</a>";
    }
    
    # Close filehandle
    close ($myPage); 
    
    print "\t\t</div>";
    print "\t</div>";
    print "</div>";    
}
elsif($validPage==2){

    if (defined $cookie_present && $cookie_present > 0)
    {
	my $UID = $cookie_present;
	tie (my %db_hash, "DB_File", "./profiles/" . $UID . ".db");

	print "<div class=\"container\">";
	print "<p class=\"story_page_header\">Welcome back!</p>";
	print "</div>";
	print "<p>Thank you for playing \"The House on The Hill\"! ";

	# Check if there is a cookie set but no .db profile present (tampering)
	if(defined $db_hash{"page"}){
	    print "The last time you played, you finished on page $db_hash{\"page\"}. ";
	    print "What would you like to do today?</p><p>You can start over by pressing the \"Reset\" button ";
	    print "below or you can continue your game from where you last finished by pressing the ";
	    print "\"Continue\" button. Please make a choice!</p>";
	    print "<br /><br />";
	    print "<div class=\"nav-bar\">";
	    print $cgi->a({"href"=>"getPage.cgi?page=1"},"Reset");
	    print $cgi->a({"href"=>"getPage.cgi?page=$db_hash{\"page\"}"},"Continue");
	    print "</div>";
	}
	else{
	    print "It looks like you have visited this page before, however, ";
	    print "we are unable to determine which page you finished on last time you played! ";
	    print "What would you like to do today?</p><p>You can start over by pressing ";
	    print "the \"Reset\" button below. ";
	    print "If you press the \"Continue\" button you may see an error message. ";
	    print "Please make a choice!</p>";
	    print "<br /><br />";
	    print "<div class=\"nav-bar\">";
	    print $cgi->a({"href"=>"getPage.cgi?page=1"},"Reset");
	    print $cgi->a({"href"=>"getPage.cgi?page=error"},"Continue");
	    print "</div>";
	}
    }
    else{
	print "<div class=\"container\">";
        print "<p class=\"story_page_header\">Welcome!</p>";
        print "</div>";
	print "<p>Thank you for choosing to play \"The House on The Hill\"! ";
	print "I am sure you will enjoy this game. If you return to this page in the future you will be ";
	print "able to continue from where you left off or start a new game! ";
	print "Please click the \"Start Game\" button below to begin:</p>";
	print "<br /><br />";
	print "<div class=\"nav-bar\">";
	print $cgi->a({"href"=>"getPage.cgi?page=1"},"Start Game");
	print "</div>";
    }

    print "</div>";
    print "</div>";
    print "</div>";
}
else{
    
    print $cgi->p({"class"=>"error"},"Invalid page number supplied in GET request!");
    print $cgi->p({"class"=>"error"},"Please press \"Start Over\" to try again.");
    print "</div>";
    print "</div>";
    print "</div>";    
}

# Set up bottom div
print $cgi->div({"id"=>"bottom"},
                $cgi->div({"class"=>"container"},
                          $cgi->div({"id"=>"footer"},
                                    $cgi->address({"id"=>"a_left"},"&copy; Matthew Shirlaw"),
                                    $cgi->address({"id"=>"a_center"},"Assignment 3"),
                                    $cgi->address({"id"=>"a_right"},"COMP315")
                          )
                )
    );

# Output end of the HTML body
print $cgi->end_html;

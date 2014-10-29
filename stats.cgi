#!/usr/bin/perl
# Displays stats for the game 
use warnings;
use strict;
use CGI;

# Create CGI object
my $cgi = CGI->new;

# Determine if we should reset statistics
if($cgi->param("reset") eq "true"){
    # Reset tracker
    system("perl ./scripts/trackerReset.pl");
}

# Print header.
print $cgi->header;

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
print $cgi->a({"href"=>"stats.cgi?reset=true"},"Reset");
print "</div>";

print $cgi->p({"id"=>"tagline"},"An adventure like no other.");
print $cgi->p({"id"=>"lesser_tag"},"This game will inspire and intrigue? Can you escape?");

#print $cgi->img({"src"=>"img/castle.png","alt"=>"Adventure Background","id"=>"castle"});

print "</div>";
print "</div>";

# Set up the middle div
print "<div id=\"middle_cgi\">";
print "<div class=\"container\">";

print $cgi->p({"class"=>"scenario_header"},"Game Statistics");
print "<div id=\"summary_table\">";
print "<br />";
print "<table>";
print $cgi->Tr($cgi->th("Item"),$cgi->th("Statistic"));

# Count the number of pages in the pages directory
my $counter = 0;
my $page_directory = "./pages/";
opendir(my $all_pages, $page_directory) || die "Couldn't open directory.\n";
for my $entry (readdir($all_pages)){
    if(-f "$page_directory$entry"){
        $counter++;
    }
}
closedir $all_pages;

print $cgi->Tr($cgi->td("Number of pages:"),$cgi->td("$counter"));

# Count number of endings
my $endString = `perl ./scripts/findEndings.pl`;
my $end = 0;
if($endString =~ /(\d+)/){
    $end =  $1;
}

print $cgi->Tr($cgi->td("Number of endings:"),$cgi->td("$end"));

# Count number of page view
my ($totalViews) = `perl ./scripts/trackerTotal.pl` =~ /(\d+)/;
print $cgi->Tr($cgi->td("Total page views:"),$cgi->td("$totalViews"));

# Count current players
my $currentPlayers = 0;

# Open a directory filehandle to the profiles directory
opendir(my $profiles_dir, "./profiles/") || die "Couldn't open directory.\n";
for my $entry (readdir($profiles_dir)) {
    if(! -d $entry){
	$currentPlayers++;
    }
}
print $cgi->Tr($cgi->td("Current number of players:"),$cgi->td("$currentPlayers"));

# Check that the game passes validation
my $gameValidation = `perl ./scripts/validation.pl`;

print $cgi->Tr($cgi->td("Validation status:"),$cgi->td("$gameValidation"));

# Display page view statistics
my @endPages = split(" ",`perl ./scripts/endPages.pl`);
my @pageViews = split("\n", `perl ./scripts/trackerView.pl`);
my %hash = ();
my $numEndViews = 0;

print "<tr>";
print "<td>End page views:</td>";
print "<td>";
print "<ul>";

for my $end (@endPages){
    my $count = 0;
    while ($count < @pageViews){
	if($pageViews[$count] =~ /Page $end has been visited (\d+) times./){
	    $hash{"Page $end"} = $1;
	    $numEndViews+=$1;
	}
	$count++;
    }
    if(not exists $hash{"Page $end"}){
	$hash{"Page $end"} = 0; 
    }
}

if(!$numEndViews){
    print "<li>No end page views yet!</li>";
}
else{
    for my $key (sort keys %hash){
	my $percent = int((($hash{$key}/$numEndViews)*100)) . "%"; 
	print "<li>$key - $hash{$key} views ($percent)</li>";
    }
}

print "</ul>";
print "</td>";
print "</tr>";

print "</table>";
print "</div>";

print "</div>";
print "</div>";


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

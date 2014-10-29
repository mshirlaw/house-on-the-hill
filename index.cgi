#!/usr/bin/perl

use warnings;
use strict;
use CGI;

# Create CGI object.
my $cgi = CGI->new;

# Print header.
print $cgi->header;

# Set title and stylesheet                                                      
print $cgi->start_html("-title"=>"House on the Hill",
                       "-style"=>"css/adventure.css",
                       "-script"=>[{"-type"=>"javascript",
                                    "-src"=>"javascript/toggle.js"},]);
# Set up the top div
print "<div id=\"top\">";
print "<div class=\"container\">";

print "<a href=\"index.cgi\"><img src=\"img/title_crop.png\" alt=\"House on the Hill\" id=\"title_img\"></a>";

print "<div class=\"nav-bar\">";
print $cgi->a({"href"=>"index.cgi"},"Home");
print $cgi->a({"href"=>"getPage.cgi"},"Start Game");
print $cgi->a({"href"=>"stats.cgi"},"Statistics");
print "</div>";

print $cgi->p({"id"=>"tagline"},"An adventure like no other.");
print $cgi->p({"id"=>"lesser_tag"},"This game will inspire and intrigue? Can you escape?");
print $cgi->img({"src"=>"img/castle.png","alt"=>"Adventure Background","id"=>"castle"});

print "</div>";
print "</div>";

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

# Set up the middle div
print "<div id=\"middle_cgi\">";
print "<div class=\"container\">";

print $cgi->p({"class"=>"scenario_header"},"Background");
print "<div class=\"scenario\" style=\"padding-bottom:0px\">";
print $cgi->p("House on the Hill is a text based adventure game, written in the thriller genre. The player awakes in an unfamiliar house, in complete darkness and is then forced to make a series of choices in an attempt to escape from the house. The decisions that the player makes will ultimately shape the game and could represent the difference between life and death. Can you survive the House on the Hill?");
print $cgi->p("Inspiration for this story has been drawn from older movies in the thriller / horror genre such as Hostel and Saw where the main character awakes in a terrifying scenario which will offer the ultimate test of their survival ability.");
print "</div>";

print $cgi->p({"class"=>"scenario_header"},"You awake inside a room...");
print "<div id=\"left_col\">";
print "<div class=\"scenario\">";
print $cgi->p("It is pitch black. You can't see anything but you sense that there is someone else in the room with you.");
print $cgi->p("You take a breath. A foul odour that you have never smelt before pierces your nostrils.");
print "</div>";
print "</div>";

print "<div id=\"right_col\">";
print "<div class=\"scenario\">";
print $cgi->p("You think you can see a light in front of you but it's so dark you aren't completely sure. It could be your eyes playing tricks on you.");
print $cgi->p("What do you do?");
print "</div>";
print "</div>";

print "<div id=\"page_count\">";
print $cgi->p("There are currently $counter pages in this adventure!");
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

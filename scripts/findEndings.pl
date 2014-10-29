#!/usr/bin/perl
use strict;
use warnings;

# Global variable to store number of endings
my $endings = 0;

# String to store location of pages directory
my $dirString = "./pages/";

# Open a directory filehandle to the pages directory
opendir(my $page_directory, $dirString) || die "Couldn't open directory.\n";

# Read the contents of the pages directory then
# Loop through all entries and store contents of each file in an array
for my $entry (readdir($page_directory)){
    if (!-d $entry){
	open(my $readfile, "<", $dirString . "$entry") || die "Cannot open file.\n";
	my @lines = <$readfile>;

	# If the page starts with a newline character it is an ending
	if($lines[0] eq "\n"){
	    $endings++;
	}
	close $readfile;
    }
}

# Print the number of endings
print "Endings: $endings\n";

# Close the pages directory
closedir $page_directory;

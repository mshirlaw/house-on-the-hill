#!/usr/bin/perl
use strict;
use warnings;

# Array to store end pages
my @endings = ();
my $count = 0;

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
	    $endings[$count] = $entry;
	    $count++;
	}
	close $readfile;
    }
}

# Print the page numbers for end pages
print "@endings\n";

# Close the pages directory
closedir $page_directory;

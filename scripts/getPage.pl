#!/usr/bin/perl
# A simple perl program used to control a text based game
use warnings;
use strict;

# Set the pages directory
my $pages_directory = "./pages/";

# Check for the appropriate number of cmd line args
# Display an error message and exit if incorrect
if (@ARGV == 1){
    # Set page number to the page requested by the user
    my $pageNum = $ARGV[0];
    
    # Open the correct page file for reading e.g. 1
    open(my $myPage, $pages_directory . $pageNum) || die "Cannot open page.\n";
    
    # Track pages visited
    system("perl trackerAdd.pl $pageNum");
    
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
    
    # Print scenario for this page
    while($choices < @array){
	print "$array[$choices]";
	$choices++;
	# Print a blank line if necessary
	if(($choices == @array) && ($array[$choices-1] ne "\n")){
	    print "\n";
	}
    }
    
    # Print each option sorted by key
    foreach my $option (sort keys %hash) {
	print "$hash{$option} -> Go to page $option.\n";
    }
    
    # Close filehandle
    close ($myPage); 
}
else {
    die "Incorrect usage. Please use:\ngetPage PAGE_NUMBER\n";
}

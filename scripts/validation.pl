#!/usr/bin/perl
use warnings;
use strict;

# Should correspond with how you can reach your page subdirectory from where you currently are
my $page_directory = "./pages/";

# Pages we intend to visit, one at a time, discovered by parsing choices and starting with the first page.
my @upcoming = ();

# Hash containing all pages mentioned or existing in our program, along with "Not Created", "Not Visited", or "Visited" indicating its status.
my %pages;

# Open a directory filehandle to the pages directory                            
opendir(my $all_pages, $page_directory) || die "Couldn't open directory.\n";

# Add each adventure page to the hash with the value "Not Visited"
for my $entry (readdir($all_pages)){
    # Use pattern matching to add numbered pages only
    if($entry =~ /\d/){
	$pages{$entry} = "Not Visited";
    }
    if ($entry =~ /1/){
	# Add the first page to the @upcoming array to initialise it
	push @upcoming, $entry;
    }
}

# Check upcoming pages
# Set all accessible pages to Visited
# Set inaccessible pages to Not Visited
# Set missing pages to Not Created
while (my $item = shift @upcoming){ 
    if (defined $pages{$item} == 0){
	$pages{$item} = "Not Created";
    }elsif($pages{$item} eq "Not Visited"){
	open(my $file, "<", $page_directory . $item) || die "Cannot open file.\n";
	while ((my $line = <$file>) ne "\n"){
	    push @upcoming, $line =~ /^(\w{1,})/;
	}
	$pages{$item} = "Visited";
	close $file;
    }
}

my $valid = 1;
# Check that all pages been visited
for my $vpNum (sort keys %pages){
    if ($pages{$vpNum} ne "Visited"){
	$valid=0;
    }
}

if($valid){
    print "Passed\n";
}
else{
    print "Failed\n";
}

# Close pages directory
close $all_pages;

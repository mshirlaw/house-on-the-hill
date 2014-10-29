#!/usr/bin/perl
use warnings;
use strict;
use DB_File;

# Set up a second database location
my $visits_total_db = "../visits/visits_total.db";

# Tie the second database to the visits_total array
tie(my %visits_total, "DB_File", $visits_total_db) || die "Could not open database.";

# Get the output from a call to trackerTotal.pl
my $output = `perl trackerTotal.pl`;

# Remove new line character
chomp $output;

# Debug
#print "Output of trackerTotal: $output\n";
#print "Stored in hash: $visits_total{\"Total\"}\n";

# Check whether there have been any new visitors to the pages 
if ($output eq "There have been 0 visits to the adventure pages."){
    print "The tracker has been reset.\n";
}elsif($visits_total{"Total"} eq $output){
    print "There have been no recent visits.\n";
}else{
    print "There have been recent visitors!\n";
    print "Updating the stored hash!\n";
    %visits_total = ();
    $visits_total{"Total"}=$output;
}

# Close database connection
untie %visits_total;

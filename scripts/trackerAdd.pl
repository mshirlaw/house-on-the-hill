#!/usr/bin/perl
use warnings;
use strict;
use DB_File;

# Check for correct number of cmd args
die "Correct usage: perl trackerAdd.pl <Page Number>\n" if @ARGV ==0;

# Create a hash and set it equal to location of db
my $visits_db = "./visits/visits.db";

# Tie %visits to the visits database, 
tie (my %visits, "DB_File", $visits_db) || die "Could not open database.\n";

# Increment count of visits
$visits{$ARGV[0]}++;

# Untie and close connection to the database
untie %visits;

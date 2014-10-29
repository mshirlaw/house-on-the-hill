#!/usr/bin/perl
use warnings;
use strict;
use DB_File;

# Set up the database location
my $visits_db = "./visits/visits.db";

# Tie the database to the visits hash
tie(my %visits, "DB_File", $visits_db) || die "Could not open database.";

# For each sorted key in the %visits hash
# Print out the number of times the page was visited
for my $key (sort keys %visits){
    print "Page $key has been visited $visits{$key} times.\n";
}

# Close database connection
untie %visits;

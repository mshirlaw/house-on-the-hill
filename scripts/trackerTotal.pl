#!/usr/bin/perl
use warnings; 
use strict;
use DB_File;

# Set up database locations
my $visits_db = "./visits/visits.db";
my $visits_total_db = "./visits/visits_total.db";

# Tie the database to the visits hash
tie(my %visits, "DB_File", $visits_db) || die "Could not open database.";

# Variable to store the total
my $total = 0;

# Loop through the keys in the hash sum the number of times visited
for my $key (sort keys %visits){
    $total = $total + $visits{$key};
}

# Print the total, save in %visits_toal
print "There have been $total visits to the adventure pages.\n";

# Close database connection
untie %visits;






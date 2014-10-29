#!/usr/bin/perl
use warnings;
use strict;
use DB_File;

# Set up database location
my $visits_db = "./visits/visits.db";

# Tie the database to the visits hash
tie(my %visits, "DB_File", $visits_db) || die "Could not open database.";

# Set the %visits to an empty hash
%visits = ();

# Close database connection
untie %visits;

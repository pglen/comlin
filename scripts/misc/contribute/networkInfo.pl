#!/usr/bin/perl
###########################################################################
##                                                                       ##
##       script contributed by Matthew Cline <matt@nightrealms.com>      ##
##                                                                       ##
##                                                                       ##
## This program is free software; you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation; either version 2 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
###########################################################################
use strict;

my $ifconfig = `ifconfig`;

$ifconfig =~ /^\s+inet addr:(\S+)\s+Bcast:(\S+)\s+Mask:(\S+)/m;
my($addr, $bcast, $mask) = ($1, $2, $3);

if ($? != 0) {
	die "ifconfig failed\n";
}

if (!$addr || !$bcast || !$mask) {
	die "Couldn't get info from ifconfig\n";
}

my $route = `route -n`;

$route =~ /^0.0.0.0\s+(\S+)/m;
my $gateway=$1;

if ($? != 0) {
	die "route failed\n";
}

if (!$gateway) {
	die "Couldn't get info from route\n";
}

print "ADDRESS=$addr\n";
print "NETMASK=$mask\n";
print "GATEWAY=$gateway\n";

exit 0;

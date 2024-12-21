#!/usr/bin/perl

open(fp, "aa.aa");

while(<fp>)
	{
	@bb = split(/ +/);
	print $bb[2] . "\n";
	}


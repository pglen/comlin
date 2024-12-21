#!/usr/bin/perl

open (FH, "XF86Config.new");

while(<FH>)
	{
	if (m/^Section *\"Device/)
		{
		$on = 1;
		}
	elsif (m/^Section/)
		{
		$on = 0;
		}
	if($on)
		{
		if (m/^[ \t]*Driver/)
			{
			@aa = split(/[ \t]+/);
			@aa[2] =~ s/\"//g;
			print @aa[2];
			}
		}
	}

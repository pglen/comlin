#!/usr/bin/perl
# Utility to fill up file with stuff

if (@ARGV < 3)
	{
    print "Usage: fillfile.pl filename size fillhar\n"; 
	exit;
	}

$ffile = shift @ARGV;
$fsize = shift @ARGV;
$fchar = shift @ARGV;

$fsize += 0;
$lenx = length($fchar);

	if($fsize == 0)
		{
		print "Must specify file size\n";
		exit(0);
		}

    #print "Filling file '$ffile' $fsize bytes with '$fchar' len=$lenx\n";

    if(!open(OUT, ">$ffile"))
    	{
		print "Cannot create $ffile $!\n"; exit;
    	}

    while ($fsize > 0)
    	{    	
		print OUT $fchar;
		$fsize = $fsize - $lenx;
		#print "$fsize ";
		}
	close(OUT);

exit(0);

# --------------------------------------------------------------
# Set file properties back to original
# use: fileprop $filename, @tempstat

sub fileprop

{
    my($fname, @co) = @_;
    #print "$fname size = $co[7]\n";

    if(!chown($co[4], $co[5], $fname))
    	{
		print "Warning: Cannot change owner/group on $fname $!\n";
    	}
    if(!utime($co[8], $co[9], $fname))
    	{
		print "Cannot change time/date on $fname $!\n";
    	}
    if(!chmod($co[2], $fname))
    	{
		print "Cannot change mode on $fname $1\n";
    	}
    1;
}

#end of d2u


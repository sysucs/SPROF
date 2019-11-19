while(<>)
{
chomp $_;
#system "check_rewritepdb.pl $_>$_.pdb";
system "getpdbseq.pl $_ >$_.seq";
open(FN,"$_.seq");
@fn=<FN>;chomp $fn[0];$l=length $fn[0];
print "\"$_\"        $l\n";
}

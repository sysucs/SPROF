#!/usr/bin/env/perl -w
open(LIST,"$ARGV[0]");
@list=<LIST>;
for(@list)
{
    chomp $_;$id=$_;
    open(PDB,"$_");
    @pdb=<PDB>;
    for(@pdb)
    {
        if($_=~m/^SEQRES/)
        {
            if($_=~m/\s+DT\s+/)
            {
                print "$id\n";last;
            }
        }
    }
}

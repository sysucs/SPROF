#!/bin/bash

infile=$1
#id=$2

# Change directory
#cd results/$id || exit 1

# Make copy of input file
cp $infile $infile.pdb || exit 2

# Extract backbone
export DATADIR="/home/cs/SPROF/run/SPIN2/"
/home/cs/SPROF/run/SPIN2/bin/get_ala_backbone.pl $infile || exit 3

# Generate fragments
echo -e "\"$infile.ALA.pdb\"\\t`grep CA $infile.ALA.pdb | wc -l`" > $infile.list
/home/cs/SPROF/run/SPIN2/bin/featuregen_fragments /home/cs/SPROF/run/SPIN2/data/db/ /home/cs/SPROF/run/SPIN2/data/list ./ ./$infile.list || exit 4
/home/cs/SPROF/run/SPIN2/bin/get_SP.pl $infile || exit 5

# Generate rotomers
/home/cs/SPROF/run/SPIN2/bin/featuregen_rotomers /home/cs/SPROF/run/SPIN2/data/lib/dfirelib1 ./ $infile.ALA.pdb > $infile.sc || exit 6
/home/cs/SPROF/run/SPIN2/bin/get_SC.pl $infile || exit 7
\cat $infile.sc.nml | tr -s " " | cut -d " " -f 2-27,29-114 > $infile.features.rotomers || exit 8

# Extract atom positions
# Print file     extract columns            separate squashed fields                                                         del spaces  remove CB    del start spaces  del trailing sp   replace N      replace CA      replace C      replace O      write to file
cat $infile.ALA.pdb | cut -c 13-16,23-26,31-54 | sed 's:^\(.\{4\}\)\(.\{4\}\)\(.\{8\}\)\(.\{8\}\)\(.\{8\}\).*$:\1 \2 \3 \4 \5:' | tr -s " " | grep -v CB | sed 's:^[ ]*::' | sed 's:[ ]*$::' | sed 's:N:0:' | sed 's:CA:1:' | sed 's:C:2:' | sed 's:O:3:' > $infile.positions || exit 9

# Run classifier
#/home/cs/SPROF/run/SPIN2/bin/spin2.py _tmp.positions _tmp.features.fragments _tmp.features.rotomers > $1.txt || exit 10
# Clean things up

mv $infile.features.fragments /home/cs/SPROF/run/features/$1.frag

rm $infile* || exit 11

#!/bin/bash

infile=$1
id=$2

# Change directory
cd results/$id || exit 1

# Make copy of input file
cp $infile _tmp.pdb || exit 2

# Extract backbone
export DATADIR="../../data/"
../../bin/get_ala_backbone.pl _tmp || exit 3

# Generate fragments
echo -e "\"_tmp.ALA.pdb\"\\t`grep CA _tmp.ALA.pdb | wc -l`" > _tmp.list
../../bin/featuregen_fragments ../../data/db/ ../../data/list ./ ./_tmp.list || exit 4
../../bin/get_SP.pl _tmp || exit 5

# Generate rotomers
../../bin/featuregen_rotomers ../../data/lib/dfirelib1 ./ _tmp.ALA.pdb > _tmp.sc || exit 6
../../bin/get_SC.pl _tmp || exit 7
cat _tmp.sc.nml | tr -s " " | cut -d " " -f 2-27,29-114 > _tmp.features.rotomers || exit 8

# Extract atom positions
# Print file     extract columns            separate squashed fields                                                         del spaces  remove CB    del start spaces  del trailing sp   replace N      replace CA      replace C      replace O      write to file
cat _tmp.ALA.pdb | cut -c 13-16,23-26,31-54 | sed 's:^\(.\{4\}\)\(.\{4\}\)\(.\{8\}\)\(.\{8\}\)\(.\{8\}\).*$:\1 \2 \3 \4 \5:' | tr -s " " | grep -v CB | sed 's:^[ ]*::' | sed 's:[ ]*$::' | sed 's:N:0:' | sed 's:CA:1:' | sed 's:C:2:' | sed 's:O:3:' > _tmp.positions || exit 9

# Run classifier
../../bin/spin2.py _tmp.positions _tmp.features.fragments _tmp.features.rotomers > results.txt || exit 10

# Clean things up
rm _tmp* || exit 11

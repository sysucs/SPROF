cp $1 /home/cs/SPROF/run/
cd /home/cs/SPROF/run/
./caltheta $1 > ./features/$1.t
./calphipsiomega $1 > ./features/$1.om
./dfire_rotamer $1 > ./features/$1.en

dssp -i $1 -o ./features/$1.d
./getdssp ./features/$1.d > ./features/$1.dssp


/home/cs/SPROF/run/SPIN2/results/process_pdb.sh $1


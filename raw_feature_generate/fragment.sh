for file in *
do
{
        cp $file /home/cs/SPROF/run/
        cd /home/cs/SPROF/run/
        /home/cs/SPROF/run/SPIN2/results/process_pdb2.sh $file
	cd -
}&
done

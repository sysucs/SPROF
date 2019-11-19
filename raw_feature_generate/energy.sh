for file in *
do
        cp $file /home/cs/SPROF/run/
        cd /home/cs/SPROF/run/
        ./caltheta $file > ./features/$file.t
        ./calphipsiomega $file > ./features/$file.om
        ./dfire_rotamer $file > ./features/$file.en
        cd -
done


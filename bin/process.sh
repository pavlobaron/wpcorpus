#!/bin/sh

PAR=4

cd ../
rm -rf ./corpus/text
mkdir -p ./corpus/text

for n in $(seq $PAR)
do
    rm /tmp/wiki$n.d
done

count=1
cd lib/wpcorpus
for f in ../../dump/chunk/*.xml
  do
    echo "Processing $f file.."
    python process.py $f $count &

    if [ $((count % PAR)) == 0 ]; then
        echo "waiting for results..."
        while [ ! -f /tmp/wiki1.d -o ! -f /tmp/wiki2.d -o ! -f /tmp/wiki3.d -o ! -f /tmp/wiki4.d ]
        do
  	    sleep 5
        done

        for n in $(seq $PAR)
        do
            rm /tmp/wiki$n.d
        done

	count=1
    else
	count=$((count + 1))
    fi
done

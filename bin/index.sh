#!/bin/sh

sudo rabbitmq-server -detached

sleep 5

cd ../
rm -rf ./corpus/ix
mkdir -p ./corpus/ix
cd lib/wpcorpus
python index.py


#!/bin/bash
# Builds a docker image for myproject
# takes 1 argument which is the name of a dockerfile e.g. train-gpu.Dockerfile

echo "enter a dockerfile as an argument e.g. 'source utils/builddocker.sh install/gpu.Dockerfile'"
echo ""
echo "options are:"
ls install/ | grep 'Dockerfile'
echo "building docker image for $1"

sudo docker build -t ml_project:v1 install/ -f $1

echo "Done!"

#!/bin/bash
# Runs a Jupyter notebook server for a prebuilt docker image named 'ml_project:v1'
# see script builddocker.sh for how to build the image.
# Run this script from project root, 
# such as it maps the current directory to a folder within the docker image

GPU=$(sudo lshw -numeric -C display)

if [[ $GPU == *"NVIDIA"* ]]; then
    echo "Trying to run with GPU (make sure you have nvidia-docker installed)"
    sudo docker run --gpus all -v $(pwd):/tf -it --rm -p 8892:8888 ml_project:v1
else
    echo "Running with CPU only"
    sudo docker run -v $(pwd):/tf -it --rm -p 8892:8888 ml_project:v1
fi

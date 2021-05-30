#!/bin/bash
# Runs a Jupyter notebook server for a prebuilt docker image tagged 'ml_project:v1'
# see script builddocker.ps1 for how to build the image
# it also maps the project root directory to a folder within the docker image

sudo docker run -v ${PWD}:/tf -it --rm -p 8888:8888 ml_project:v1

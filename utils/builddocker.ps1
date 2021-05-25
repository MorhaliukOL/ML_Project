#!/bin/bash
# Builds a docker image for ML_Project
# takes 1 argument which is the name of a dockerfile e.g. train-gpu.Dockerfile
# It assumes all Dockerfiles are in ML_Project/install/ directory

$Dockerfile = $args[0]

# $INSTALL_DIR must contain Dockerfiles and all files that
# need to be copied to docker image, like 'requirements.txt'
$INSTALL_DIR=Join-Path ${PWD} "install"
$DOCKERFILE_PATH=Join-Path $INSTALL_DIR $Dockerfile

docker build -t "ml_project:v1" -f $DOCKERFILE_PATH $INSTALL_DIR


docker build -t "ml_project:v1" -f Join-Path Join-Path ${PWD} "install" $args[0] Join-Path ${PWD} "install"

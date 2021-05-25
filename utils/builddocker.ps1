#!/bin/bash
# Builds a docker image for ML_Project
# takes 1 argument which is the name of a dockerfile e.g. train-gpu.Dockerfile
# It assumes all Dockerfiles are in ML_Project/install/ directory

$Dockerfile = $args[0]
# Project root directory
$ROOT_DIR=${PWD} | split-path

$INSTALL_DIR=Join-Path $ROOT_DIR "install"
$DOCKERFILE_PATH=Join-Path $INSTALL_DIR $Dockerfile

docker build -t "ml_project:v1" -f $DOCKERFILE_PATH $INSTALL_DIR

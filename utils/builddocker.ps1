# Builds a docker image for ML_Project
# takes 1 argument - path to a dockerfile e.g. './install/train-gpu.Dockerfile'
# It assumes all Dockerfiles are in ML_Project/install/ directory


# $INSTALL_DIR - directory that contains Dockerfiles and all files that
# need to be copied to docker image, like 'requirements.txt'
$INSTALL_DIR=Join-Path ${PWD} "install"
$DOCKERFILE_PATH=$args[0]

docker build -t "ml_project:v1" -f $DOCKERFILE_PATH $INSTALL_DIR

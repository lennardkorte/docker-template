#! /bin/bash

PROJECT_NAME="project_template"
NAME_IMAGE="image-${PROJECT_NAME}"
NAME_CONTAINER="container-${PROJECT_NAME}"
FILENAME="${PROJECT_NAME}.py"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DATA_SRC_DIR=$SCRIPT_DIR/data/read_only/
WORKING_DIR=$SCRIPT_DIR/data/working/

GREEN=`tput setaf 2`
RESET=`tput sgr0`

echo -e "${GREEN}\n\nBuilding docker-image...${RESET}"
docker build -t $NAME_IMAGE .

echo -e "${GREEN}\n\nRemoving additional <none> images...${RESET}"
docker rm $(docker ps -a -q) > /dev/null 2>&1
docker image prune -f

echo -e "${GREEN}\n\nShow all images:${RESET}"
docker image ls

echo -e "${GREEN}\n\nRun docker-image:${RESET}"
args="$@"
docker run \
-it --rm \
--gpus all \
--shm-size 8G \
--name $NAME_CONTAINER \
--mount type=bind,source=${DATA_SRC_DIR},target=/docker/data/read_only,readonly \
--mount type=bind,source=${WORKING_DIR},target=/docker/data/working \
-i $NAME_IMAGE "src/${FILENAME} ${args}"


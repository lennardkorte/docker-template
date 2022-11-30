#! /bin/bash

project_name="testproject"
name_image="image-${project_name}"
name_container="container-${project_name}"
filename="${project_name}.py"
#data_source_dir=/home/Korte/${project_name}/data_source

green=`tput setaf 2`
reset=`tput sgr0`

echo -e "${green}\n\nBuilding docker-image...${reset}"
docker build -t $name_image --build-arg name=$project_name .

echo -e "${green}\n\nRemoving additional <none> images...${reset}"
docker rm $(docker ps -a -q) > /dev/null 2>&1
docker image prune -f

echo -e "${green}\n\nShow all images:${reset}"
docker image ls

echo -e "${green}\n\nRun docker-image:${reset}"
args="$@"
docker run \
-it --rm \
--gpus all \
--shm-size 8G \
--name $name_container \
-i $name_image "src/${filename} ${args}"

#--mount type=bind,source=${data_source_dir},target=/${project_name}/data_source,readonly \
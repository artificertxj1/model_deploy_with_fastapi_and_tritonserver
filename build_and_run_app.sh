#!/bin/bash
DOCKER_INSTALLED=$( docker -v )
if [ $? -eq "0" ]; then
	echo "Docker installed"
else
	echo "Docker not installed"
    echo "Exit On Error..."
    exit 1
fi

RUN="run"
STOP="stop"
TRITONSERVER_REQUIRED="nvcr.io/nvidia/tritonserver:20.10-py3"
TRITONSERVER_NAME="tricorder_overhead_classify"
APP_IMAGE_NAME="tricorder_overhead_api_image"
APP_DOCKER_FILE="Tricorder_Dockerfile"
APP_CONTAINER_NAME="tricorder_overhead_api_container"
if [ $1 == $RUN ]; then
	TRITON_IMAGE_EXISTS=$( docker images -q $tritonserver_required )
	if [[ -n "$TRITON_IMAGE_EXISTS" ]]; then
		echo "Required TritonServer Image $TRITONSERVER_REQUIRED Exists."
	else
		echo "Required TritonServer Image $TRITONSERVER_REQUIRED Not Found! Will Start Pulling Image"
		echo "Start Pulling TritonServer Image"
		docker pull "$TRITONSERVER_REQUIRED"
        echo "TritonServer Image Is Ready!"
	fi

	TRITON_CONTAINER_RUNNING=$( docker container ps -q -f name=$TRITONSERVER_NAME )
	#if [ -z "$TRITON_CONTAINER_RUNNING" ]; then
	#	echo "empty"
	#fi
	if [ -z "$TRITON_CONTAINER_RUNNING" ]; then
		echo "TritonServer $TRITONSERVER_NAME Is Not Running, Will Start The Container Now"
		echo "Starting the $TRITONSERVER_NAME container now..."
		docker run -d --rm --name $TRITONSERVER_NAME --gpus=1 -p8000:8000 -p8001:8001 -p8002:8002 -v$PWD/jit_models:/models $TRITONSERVER_REQUIRED tritonserver --model-repository=/models --log-verbose=5 --log-info true --log-warning=true --log-error=true --model-control-mode=poll
		echo "TritonServer $TRITONSERVER_NAME is running now"
	else
		echo "TritonServer $TRITONSERVER_NAME is running now"
	fi

	APP_CONTAINER_EXISTS=$( docker images -q $APP_IMAGE_NAME )
	if [[ -n "$APP_CONTAINER_EXISTS" ]]; then
        echo "APP Image $APP_IMAGE_NAME Exists"
    else
        echo "APP Image $APP_IMAGE_NAME Not Found, Building from Dockerfile now."
        echo "Building APP Image From $APP_DOCKER_FILE"
        docker build -t $APP_IMAGE_NAME -f $APP_DOCKER_FILE .
        echo "APP Image Is Ready!"
    fi
    APP_CONTAINER_RUNNING=$( docker container ps -q -f name=$APP_CONTAINER_NAME )
    #echo "$APP_CONTAINER_RUNNING"
    if [ -z "$APP_CONTAINER_RUNNING" ]; then
        echo "APP Container $APP_CONTAINER_NAME Is Not Running, Will Start The Container Now"
        echo "Starting APP Container $APP_CONTAINER_NAME ..."
        docker run -d --rm --name $APP_CONTAINER_NAME -v /home/ubuntu/image_data:/image_data --network="host" -p 8080:8080 $APP_IMAGE_NAME
        echo "APP Container Is Running Now!"
    else
        echo "APP Container Is Running Now!"
    fi
elif [ $1 == $STOP ]; then
    echo "Stop APP Container Now"
    docker container stop $APP_CONTAINER_NAME
    echo "Stop Triton Container Now"
    docker container stop $TRITONSERVER_NAME
else
    echo "Non-recognized Op name $1"
fi

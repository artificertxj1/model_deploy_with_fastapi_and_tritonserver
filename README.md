# An example of deploying model using FastAPI and TritonServer

FastAPI: https://fastapi.tiangolo.com

TritonServer: https://github.com/triton-inference-server/server

To start app run:

    bash build_and_run_app.sh run

To stop app run:

    bash build_and_run_app.sh stop
    
Once the app starts running:

  To check model and triton-server status: 

    curl localhost:8080/health
  
  To make a prediction of an image:
  
    curl --header "Content-Type: application/json" \
           --request POST \
           --data '{"img_ID":Key_ID of the image,"img_Path":Image save path}' \
            localhost:8080/predict

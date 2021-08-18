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
  
  To classify an image:
  
    curl --header "Content-Type: application/json" \
           --request POST \
           --data '{"img_ID":Key_ID of the image,"img_Path":Image save path}' \
            localhost:8080/predict
            
Image file reading and storage have a directory dependency (/home/ubuntu/image_data). If users have image data located in other local directories, users can change the line 56 in build_and_run_app.sh "-v /home/ubuntu/image_data:/image_data" to "-v <YOUR-IMAGE-DIRECTORY>:/image_data".  API container will bind this localhost directory to container volume /image_data. When you send a request to port 8080, img_Path should be "/image_data/<NAME_OF_IMAGE>" 

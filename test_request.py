import os
import glob
import requests

REST_API_URL = "http://localhost:8080/predict"

file_paths = glob.glob("/home/m31770/triton/image_data/*.png")


for file in file_paths:
    img_ID = os.path.basename(file).split(".")[0]
    img_Path = os.path.join("/image_data", img_ID+".png")
    payload={"img_ID":img_ID, "img_Path":img_Path}
    res = requests.post(REST_API_URL, json=payload).json()
    print(res)

class configs:
    
    def __init__(self):
        self.triton_url="localhost:8001"
        self.model="resnet"
        self.model_version= 1
        self.class_labels={
                    "0":"Common Image",
                    "1":"Overhead Image"
                 }
    
    
cfg = configs()


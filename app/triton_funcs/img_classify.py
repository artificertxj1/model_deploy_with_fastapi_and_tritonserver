import os
import pathlib
import json
from typing import Union, Optional, Tuple, List


import numpy as np
from PIL import Image
from torchvision import transforms
import tritonclient.grpc as triton_grpc

from app.triton_funcs.resnet_infer import InferResnet
from app.triton_funcs.triton_cfg import cfg

class ModelDoesNotExistError(KeyError):
    pass

class ImageClassifier:
    config = cfg
    img_transforms = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    def __init__(self)->None:
        #self.config = self._read_config(self.config_path)
        
        try:
            model_name = self.config.model #["model"]
            model_version    = self.config.model_version #["model_version"]
            self.class_labels = self.config.class_labels #["class_labels"]
        except KeyError:
            raise ModelDoesNotExistError
          
        self.triton_client = triton_grpc.InferenceServerClient(
            url=self.config.triton_url, #["triton_url"],
            verbose=False,
            ssl=False
        )
        
        model_config = {"model":model_name, "version":model_version}
        self.classifier = self._initialize_model(model_config)
        
        
    def __call__(self, img_path:str)->Tuple[int, str]:
        file = pathlib.Path(img_path)
        if not file.exists():
            return (-1, "null")
        img = Image.open(file)
        if img.mode != "RGB":
            img = img.convert("RGB")
    
        triton_input = self.img_transforms(img).view(-1, 3, 224, 224).numpy()
        res = int(self.classifier(triton_input)[0])
        label = self.class_labels[str(res)]
        return (res, label)
            
            
    def _initialize_model(self, config:dict):
        model = config["model"]
        if model == "resnet":
            model = InferResnet
        else:
            raise NotImplementedError
        
         
        return model(self.triton_client, config["model"], config["version"])
    
    
    
    
    
    @staticmethod
    def _read_config(config_path:str)->dict:
        with open(config_path) as config_f:
            return json.load(config_f)
    
    

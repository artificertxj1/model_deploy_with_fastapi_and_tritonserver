from abc import ABC, abstractmethod
import logging
from functools import partial
from typing import Tuple, Union

import numpy as np

import tritonclient.grpc as triton_grpc
from tritonclient.grpc import InferenceServerClient

class TritonModel(ABC):
    __name__ = ""
    
    def __init__(self, triton_client: InferenceServerClient, model_name: str,
                 model_version: Union[str, int]):
        self.infer = partial(triton_client.infer, model_name=model_name, 
                             model_version=str(model_version))
        self.logger = logging.getLogger("overhead_classify").getChild(self.__name__)
    
    @abstractmethod
    def __call__(self):
        pass
    
    
    
class InferResnet(TritonModel):
    __name__ = "resnet"
    infer_batch_size = 32
    
    def _query_resnet_model(self, img:np.ndarray)->np.ndarray:
        input_name  = "INPUT__0"
        output_name = "OUTPUT__0"
        
        triton_inputs = [triton_grpc.InferInput(input_name, img.shape, "FP32")]
        triton_inputs[0].set_data_from_numpy(img)
        
        triton_outputs = [triton_grpc.InferRequestedOutput(output_name)]
        
        predict = self.infer(inputs=triton_inputs, outputs=triton_outputs)
        
        score = predict.as_numpy(output_name)
        
        return score
    
    def __call__(self, img:np.ndarray):
        """
        img: [batch_size, 3, 224, 224]
        return: 
            a list of prediction label
        """
        input_batch_size = img.shape[0]
        batched_inputs = [
            img[i:i+self.infer_batch_size] for i in range(0, input_batch_size, self.infer_batch_size)
        ]
        predicts = []
        for i, batch in enumerate(batched_inputs, 1):
            scores = self._query_resnet_model(batch)
            for sc in scores:
                sft_sc = softmax(sc)
                predicts.append(np.argmax(sft_sc))
        return predicts
                

def softmax(x):
    y = np.exp(x - np.max(x))
    f_x = y / np.sum(np.exp(x))
    return f_x
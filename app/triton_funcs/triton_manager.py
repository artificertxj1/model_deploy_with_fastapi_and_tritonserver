import os
import json
import tritonclient.grpc as triton_grpc

from app.triton_funcs.triton_cfg import cfg

class TritonManager():
    triton_url = cfg.triton_url
    model      = cfg.model

    def __init__(self):
        
        
        #self.config = self._read_config(self.config_path)

        self.triton_client = triton_grpc.InferenceServerClient(
                    url=str(self.triton_url),
                    verbose=False,
                    ssl=False
                )
        
        self.ready_models = self._get_ready_models()

    def _get_all_models(self)->list:
        response = self.triton_client.get_model_repository_index()
        return response.models

    def _get_ready_models(self)->set:
        return set([model.name for model in self._get_all_models() if model.state=="READY"])
    
    def get_model_health(self)->str:
        model_status = "DOWN"
        model_name = self.model #["model"]
        if {model_name}.intersection(self.ready_models):
            model_status = "OK"
        return model_status
    
    def check_server_status(self)->str:
        """
        return "DOWN" if server is down. 
        return "ERROR" if server is up but there are not available models.
        otherwise return "OK"
        """
        ready_server = self.triton_client.is_server_ready()
        if ready_server and len(self.ready_models) > 0:
            return "OK"
        if ready_server:
            return "ERROR"
        return "DOWN"

    @staticmethod
    def _read_config(config_path:str) -> dict:
        with open(config_path) as config_f:
            return json.load(config_f)


import sys
from fastapi import APIRouter
from app.triton_funcs.triton_manager import TritonManager

#define the router
router = APIRouter()
triton_mgr = TritonManager()

@router.get("")
def get_heath():
    
    health = {"model":"DOWN", "server":"DOWN"}
    health["model"] = triton_mgr.get_model_health()
    health["server"] = triton_mgr.check_server_status()
    return health
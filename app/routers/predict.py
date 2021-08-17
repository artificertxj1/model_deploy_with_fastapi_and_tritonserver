from fastapi import APIRouter

from app.controller.predict_controller import make_prediction
from app.controller.predict_pydantic import PredictIn, PredictOut

router = APIRouter()

@router.post("", response_model=PredictOut)
def predict(predict_in: PredictIn):
    return make_prediction(predict_in)
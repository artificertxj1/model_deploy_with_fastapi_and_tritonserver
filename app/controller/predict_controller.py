from app.triton_funcs.img_classify import ImageClassifier
from app.controller.predict_pydantic import PredictIn, PredictOut

def make_prediction(predict_in:PredictIn)->PredictOut:
    classifier = ImageClassifier()
    
    class_num, class_label = classifier(predict_in.img_Path)
    
    img_ID = predict_in.img_ID
    
    return PredictOut(img_ID=img_ID, pred_class_num=class_num, pred_class_label=class_label)
    
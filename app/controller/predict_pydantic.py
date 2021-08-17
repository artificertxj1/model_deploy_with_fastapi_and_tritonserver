from typing import List, Optional

from pydantic import BaseModel
from pydantic.fields import Field

class PredictIn(BaseModel):
    img_ID: str = Field(..., 
                        example="01c0b749-c3c9-48c0-b77e-5117aea622c6",
                        description="This is the query ID of the image",
                       )
    img_Path: str = Field(...,
                          example="/home/m31770/triton/image_data/sample.png",
                          description="The storage location of the input image",
                         )

class PredictOut(BaseModel):
    img_ID: str = Field(...,
                        example="01c0b749-c3c9-48c0-b77e-5117aea622c6",
                        description="This is the query ID of the input image",)
     
    pred_class_num: int = Field(...,
                                example=1,
                                description="The predicted class number",)
    
    pred_class_label: str = Field(..., 
                                  example="Overhead Image",
                                  description="Corresponding text label of the class")
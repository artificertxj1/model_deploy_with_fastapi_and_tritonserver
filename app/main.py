__version__ = "0.1.0"
__description__ = "REST API for overhead imagery classification"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from app.routers import health, predict

def app_func()->FastAPI:
    app = FastAPI(root_path="/", title="OverheadClassifier", 
                  description=__description__,
                  version=__version__)
    
    origins = ["*"]
    app.add_middleware(CORSMiddleware,
                       allow_origins=origins,
                       allow_methods=["*"],
                       allow_headers=["*"])
    app.include_router(health.router, prefix="/health", tags=["Check Server Health"])
    app.include_router(predict.router, prefix="/predict", tags=["Make Predictions"])
    
    @app.get("/")
    async def root():
        version = app.openapi()["info"]["version"]
        return {"app": "OverheadClassifier", "version": version, "swagger": app.docs_url, "redoc": app.redoc_url}

    return app


app = app_func()
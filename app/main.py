from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from . import company
from . import models
from .database import engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(company.router)
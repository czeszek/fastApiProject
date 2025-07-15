from fastapi import FastAPI
from app.routers import company_routes
import models
from database import engine

app = FastAPI()
models.Base.metadata.create_all(bing=engine)

app.include_router(company_routes.router)
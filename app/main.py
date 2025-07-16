from fastapi import FastAPI
from app.routers import company_routes, chat_routes
from app import models
from app.database import engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(company_routes.router)
app.include_router(chat_routes.router)
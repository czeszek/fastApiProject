from fastapi import FastAPI
from app.routers import company_routes
from app import models
from app.database import engine

app = FastAPI()

# Tworzenie tabel w bazie danych (jeśli nie istnieją)
models.Base.metadata.create_all(bind=engine)

# Rejestracja routerów
app.include_router(company_routes.router)

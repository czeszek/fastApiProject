from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
 
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
 
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
 
@router.get("/register", response_class=HTMLResponse)
async def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
 
 
@router.post("/register")
async def register_company(
    name: str = Form(...),
    whatsapp_number: str = Form(...),
    industry: str = Form(...),
    db: Session = Depends(get_db)
):
    new_company = models.Company(
        name=name,
        whatsapp_number=whatsapp_number,
        industry=industry
    )
    db.add(new_company)
    db.commit()
    return RedirectResponse(url="/register", status_code=303, background=False)
 
 
@router.get("/configure/{company_id}", response_class=HTMLResponse)
async def show_configure_form(request: Request, company_id: int, db: Session = Depends(get_db)):
    return templates.TemplateResponse("configure.html", {"request": request, "company_id": company_id})
 
 
@router.post("/configure/{company_id}")
async def save_configuration(
    company_id: int,
    api_key: str = Form(...),
    business_id: str = Form(...),
    phone_number_id: str = Form(...),
    db: Session = Depends(get_db)
):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if company:
        company.api_key = api_key
        company.business_id = business_id
        company.phone_number_id = phone_number_id
        db.commit()
    return RedirectResponse("/register", status_code=303)
 
 
@router.get("/companies", response_class=HTMLResponse)
async def list_companies(request: Request, db: Session = Depends(get_db)):
    companies = db.query(models.Company).all()
    return templates.TemplateResponse("companies.html", {"request": request, "companies": companies})
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from ..database import SessionLocal
from ..models import *
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(str(__file__).replace('routers/', '')).parent / "templates"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
async def show_register_form(request: Request):
    return templates.TemplateResponse("companies.html", {"request": request})

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
    new_company = Company(name=name, whatsapp_number=whatsapp_number, industry=industry)
    db.add(new_company)
    db.commit()
    return RedirectResponse("/register", status_code=303)

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
    company = db.query(Company).filter(Company.id == company_id).first()
    if company:
        company.api_key = api_key
        company.business_id = business_id
        company.phone_number_id = phone_number_id
        db.commit()
    return RedirectResponse("/register", status_code=303)

@router.get("/chat/{company_id}", response_class=HTMLResponse)
async def show_chat_interface(request: Request, company_id: int, db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).filter(ChatMessage.company_id == company_id).all()
    return templates.TemplateResponse("chat.html", {"request": request, "messages": messages, "company_id": company_id})

@router.post("/chat/{company_id}")
async def process_chat_message(company_id: int, message: str = Form(...), db: Session = Depends(get_db)):
    user_msg = ChatMessage(company_id=company_id, sender="user", content=message)
    db.add(user_msg)

    lower_msg = message.lower()
    if "price" in lower_msg:
        reply = "Our prices start from 99 PLN."
    elif "help" in lower_msg:
        reply = "What exactly do you need help with?"
    elif "thank" in lower_msg:
        reply = "Glad I could help!"
    else:
        reply = "Sorry, I didn't understand. Type 'help' to see available options."

    bot_msg = ChatMessage(company_id=company_id, sender="bot", content=reply)
    db.add(bot_msg)
    db.commit()

    return RedirectResponse(f"/chat/{company_id}", status_code=303)


@router.get("/companies", response_class=HTMLResponse)
async def list_companies(request: Request, db: Session = Depends(get_db)):
    companies = db.query(Company).all()
    return templates.TemplateResponse("companies.html", {"request": request, "companies": companies})
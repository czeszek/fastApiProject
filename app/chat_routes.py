from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import ChatMessage

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/chat/{company_id}", response_class=HTMLResponse)
async def show_chat_interface(request: Request, company_id: int, db: Session = Depends(get_db)):
    messages = db.query(ChatMessage).filter(ChatMessage.company_id == company_id).all()
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "messages": messages,
        "company_id": company_id
    })


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
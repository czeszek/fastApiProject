from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    whatsapp_number = Column(String)
    industry = Column(String)
    api_key = Column(String, nullable=True)
    business_id = Column(String, nullable=True)
    phone_number_id = Column(String, nullable=True)

    messages = relationship("ChatMessage", back_populates="company")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    sender = Column(String)
    content = Column(String)

    company = relationship("Company", back_populates="messages")
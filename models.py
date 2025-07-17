from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    whatsapp_number = Column(String)
    industry = Column(String)
    api_key = Column(String, nullable=True)
    business_id = Column(String, nullable=True)
    phone_number_id = Column(String, nullable=True)
    #user_id = Column(Integer, ForeignKey("users.id")) 

    messages = relationship("ChatMessage", back_populates="company")
    #user = relationship("User", back_populates="companies")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    sender = Column(String)
    content = Column(String)

    company = relationship("Company", back_populates="messages")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    username = Column(String)
    password = Column(String)

    #companies = relationship("Company", back_populates="user")
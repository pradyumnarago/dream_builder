from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .user_model import User
from sqlalchemy.ext.declarative import declarative_base
from app.extensions import db

class Chat(db.Model):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    user = relationship("User", backref="chats")

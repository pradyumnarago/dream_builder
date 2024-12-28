from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from .user_model import User
from sqlalchemy.ext.declarative import declarative_base
from app.extensions import db

class Habit(db.Model):
    __tablename__ = 'habit'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    frequency = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    progress = Column(Float, nullable=False)

    user = relationship("User", backref="habits")

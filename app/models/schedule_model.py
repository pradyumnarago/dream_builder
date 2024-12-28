from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Time, Text, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from .user_model import User
from app.extensions import db

class Schedule(db.Model):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_time = Column(Time, nullable=False)  # Changed to Time
    end_time = Column(Time, nullable=False)    # Changed to Time
    created_at = Column(DateTime, nullable=False)

    user = relationship("User", backref="schedules")

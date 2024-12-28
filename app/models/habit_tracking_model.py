from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .habit_model import Habit
from .user_model import User
from sqlalchemy.ext.declarative import declarative_base
from app.extensions import db

class HabitTracking(db.Model):
    __tablename__ = 'habit_tracking'

    tracking_id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    followed = Column(Boolean, nullable=True)
    habit_id = Column(Integer, ForeignKey('habit.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    habit = relationship("Habit", backref="habit_trackings")
    user = relationship("User", backref="habit_trackings")

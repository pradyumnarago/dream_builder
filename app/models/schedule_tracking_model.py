from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .schedule_model import Schedule
from .user_model import User
from sqlalchemy.ext.declarative import declarative_base
from app.extensions import db

class ScheduleTracking(db.Model):
    __tablename__ = 'schedule_tracking'

    tracking_id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    followed = Column(Boolean, nullable=True)
    schedule_id = Column(Integer, ForeignKey('schedule.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    schedule = relationship("Schedule", backref="schedule_trackings")
    user = relationship("User", backref="schedule_trackings")

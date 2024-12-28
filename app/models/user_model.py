from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Float, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from app.extensions import db
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    dob = Column(Date, nullable=False)
    password = Column(String(200), nullable=False)
    password_hash = Column(String(255), nullable=False)
    last_name = Column(String(100), nullable=True)
    date_joined = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=True)
    is_active = Column(Boolean, default=True)
    first_name = Column(String(100), nullable=True)
    reset_token = Column(String(255), nullable=True)  # Store the reset token
    reset_token_expiration = Column(DateTime, nullable=True)  # Token expiration time

    def get_id(self):
        return str(self.id)
    def is_authenticated(self):
        return self.is_active  # Return True if user is active

    def is_active(self):
        return self.is_active  # This ensures the user is marked as active

    def is_anonymous(self):
        return False  # Since you have a login system, users are not anonymous


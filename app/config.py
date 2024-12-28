import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://root:Pradyu$#9164@localhost/dream_builder'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'

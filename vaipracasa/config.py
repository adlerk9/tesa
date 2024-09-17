import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:senha1234@localhost/Adler'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
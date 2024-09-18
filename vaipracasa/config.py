import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:senha1234@localhost/Adler'
    SQLALCHEMY_DATABASE_URI = 'postgresql://adler_user:o7prblu8C1SCunm3jTvHlNVUUMPeFzFI@dpg-crl0b7ggph6c73anhhr0-a.oregon-postgres.render.com/adler'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
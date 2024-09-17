import sys
import os

# Adiciona o diretório principal ao caminho de pesquisa do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db

def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_db()
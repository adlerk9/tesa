from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Modelos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loginUser = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(999), nullable=False)
    tipoUser = db.Column(db.String(10), nullable=False)
    products = db.relationship('Product', backref='user', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    loginUser = db.Column(db.String(80), db.ForeignKey('user.loginUser'), nullable=False)
    qtde = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)

# Rotas
@app.route('/')
def index():
    if 'loginUser' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    loginUser = request.form['loginUser']
    senha = request.form['senha']
    user = User.query.filter_by(loginUser=loginUser).first()
    if user and check_password_hash(user.senha, senha):
        session['loginUser'] = user.loginUser
        return redirect(url_for('dashboard'))
    return 'Login ou senha incorretos', 401

@app.route('/logout')
def logout():
    session.pop('loginUser', None)
    return redirect(url_for('index'))

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        loginUser = request.form['loginUser']
        senha = request.form['senha']
        tipoUser = request.form['tipoUser']
        hashed_password = generate_password_hash(senha)
        new_user = User(loginUser=loginUser, senha=hashed_password, tipoUser=tipoUser)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register_user.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'loginUser' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nome = request.form['nome']
        qtde = request.form['qtde']
        preco = request.form['preco']
        user_login = session['loginUser']

        user = User.query.filter_by(loginUser=user_login).first()
        if user.tipoUser == 'normal' and Product.query.filter_by(loginUser=user_login).count() >= 3:
            return 'Você atingiu o limite de produtos.', 403

        new_product = Product(nome=nome, qtde=qtde, preco=preco, loginUser=user_login)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('add_product.html')

@app.route('/dashboard')
def dashboard():
    if 'loginUser' not in session:
        return redirect(url_for('index'))
    
    user_login = session['loginUser']
    user_products = Product.query.filter_by(loginUser=user_login).all()
    return render_template('dashboard.html', products=user_products)

if __name__ == '__main__':
    app.run(debug=True)

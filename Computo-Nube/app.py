from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_clave_secreta_muy_segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veterinaria_pro.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- MODELOS ---

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_dueno = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    nombre_mascota = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False) # Perro, Gato, etc.
    raza = db.Column(db.String(50))
    edad = db.Column(db.Integer)
    servicio = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.String(20), nullable=False)
    mensaje = db.Column(db.Text)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- RUTAS DE AUTENTICACIÓN ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('ver_citas'))
        flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# --- RUTAS DE LA VETERINARIA ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agendar', methods=['POST'])
def agendar():
    nueva_cita = Cita(
        nombre_dueno=request.form['dueno'],
        telefono=request.form['telefono'],
        email=request.form['email'],
        nombre_mascota=request.form['mascota'],
        especie=request.form['especie'],
        raza=request.form['raza'],
        edad=request.form['edad'],
        servicio=request.form['servicio'],
        fecha=request.form['fecha'],
        mensaje=request.form['mensaje']
    )
    db.session.add(nueva_cita)
    db.session.commit()
    flash('¡Cita agendada con éxito!')
    return redirect(url_for('index'))

@app.route('/citas')
@login_required
def ver_citas():
    citas = Cita.query.order_by(Cita.id.desc()).all()
    return render_template('citas.html', citas=citas)

# Crear base de datos y un usuario de prueba
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        hashed_pw = generate_password_hash('admin123', method='pbkdf2:sha256')
        admin = User(username='admin', password=hashed_pw)
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)

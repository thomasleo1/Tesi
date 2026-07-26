import os
from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Configurano il server
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)


# Crea la classe User che contiene gli utenti registrati
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Crea la classe BLEData per raccogliere i dati
class BLEData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.String(17), nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    stato = db.Column(db.String(10), nullable=False)


# Route per aggiornare i dati
@app.route('/update', methods=['POST'])
def update_data():
    try:
        print("Ricevuta una richiesta di aggiornamento.")

        data = request.json
        mac_address = data.get('Indirizzo MAC')
        distance = data.get('Distanza')
        stato = data.get('Stato')

        print(f"Ricevuti i dati del dispositivo {mac_address} urtato a distanza: {distance}")

        ble_data = BLEData(mac_address=mac_address, distance=distance, time=datetime.utcnow(), stato=stato)

        db.session.add(ble_data)
        db.session.commit()

        return 'Dati ricevuti con successo!'
    except Exception as e:
        print(f"Errore nell'aggiornamento dei dati: {str(e)}")
        return 'Errore nell\'aggiornamento dei dati', 500


# Route per la schermata di login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Credenziali errate')

    return render_template('login.html', error=None)


# Route per il logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


# Route di default
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    data = BLEData.query.all()
    return render_template('data.html', data=data)


# Avvia il server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)


# Per inserire un utente
# new_user = User(username='tleo')
# new_user.set_password("12345")
# db.session.add(new_user)
# db.session.commit()

## existing_user = User.query.filter_by(username='tleo').first()
##       if existing_user:
##           db.session.delete(existing_user)
##           db.session.commit()
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import hashlib
import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Asegúrate de cambiar esto por una clave secreta propia

# Configuración de la conexión a la base de datos
db_config = {
    'host': 'destiny-rails-db.ctg4eu8q2gxd.sa-east-1.rds.amazonaws.com',
    'user': 'porterbd',
    'password': 'destinyrails2024',
    'database': 'blackboxassist',
}

@app.route('/')
def landing_page():
    mensaje_login = session.pop('mensaje_login', None)
    alerta_registro = session.pop('alerta_registro', None)
    return render_template('landing.html', mensaje_login=mensaje_login, alerta_registro=alerta_registro)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        dob = request.form.get('dob')
        postcode = request.form.get('postcode')
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Verificar si el usuario ya existe en la base de datos
        cursor.execute('SELECT username FROM users WHERE username = %s', (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            # Si el usuario ya existe, mostrar una alerta en la página de registro
            session['alerta_registro'] = 'El usuario ya está registrado. Por favor, elige otro nombre de usuario.'
            return redirect(url_for('landing_page'))

        # Si el usuario no existe, insertarlo en la base de datos
        cursor.execute('INSERT INTO users (email, mobile, dob, postcode, username, password) VALUES (%s, %s, %s, %s, %s, %s)', 
                       (email, mobile, dob, postcode, username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('landing_page'))

    return render_template('registro.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, hashed_password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['username'] = user['username']
            session['last_login'] = str(datetime.datetime.now())
            return redirect(url_for('landing_page'))
        else:
            session['mensaje_login'] = 'Nombre de usuario o contraseña incorrectos. Inténtalo de nuevo.'
            return redirect(url_for('landing_page'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('last_login', None)
    return redirect(url_for('landing_page'))

if __name__ == '__main__':
    app.run(debug=True)

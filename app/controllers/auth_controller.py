from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.user_service import UserService

import datetime

auth_controller = Blueprint('auth_controller', __name__)

@auth_controller.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Utiliza UserService para validar el usuario
        user = UserService.validate_user(username, password)
        
        if user:
            session['username'] = user['username']
            session['last_login'] = str(datetime.datetime.now())
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('main.landing_page'))
        else:
            flash('Nombre de usuario o contraseña incorrectos. Inténtalo de nuevo.', 'error')
            return redirect(url_for('auth_controller.login'))
    
    return render_template('landing.html')
@auth_controller.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('main.landing_page'))
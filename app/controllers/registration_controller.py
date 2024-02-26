from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.services.user_service import UserService

registration_controller = Blueprint('registration_controller', __name__)

@registration_controller.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Extraer los datos del formulario
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        dob = request.form.get('dob')
        postcode = request.form.get('postcode')
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Verificar si ya existe un usuario con el mismo nombre de usuario, correo electrónico o número de teléfono
        if UserService.username_exists(username):
            return jsonify({'success': False, 'message': 'El nombre de usuario ya está en uso. Por favor, elige otro.'})
        
        if UserService.email_exists(email):
            return jsonify({'success': False, 'message': 'El correo electrónico ya está en uso. Por favor, utiliza otro.'})
        
        if UserService.mobile_exists(mobile):
            return jsonify({'success': False, 'message': 'El número de teléfono ya está en uso. Por favor, utiliza otro.'})

        # Utilizar UserService para crear el usuario
        success, message = UserService.create_user(email, mobile, dob, postcode, username, password)
        
        if success:
            # Si el registro es exitoso, mostrar la alerta y redirigir al landing page
            flash('Registro exitoso. Por favor, inicia sesión.', 'success')
            return jsonify({'success': True})
        
        # Si hay un error, mostrar el mensaje en una alerta
        flash(message, 'error')
        return jsonify({'success': False, 'message': message})
    
    # Si se solicita la página de registro mediante GET, renderizar el formulario
    return render_template('registro.html')

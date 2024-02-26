# app/services/user_service.py

import mysql.connector
from app.config.config import Config
import hashlib

class UserService:
    @staticmethod
    def get_db_connection():
        return mysql.connector.connect(
            host=Config.MYSQL_DATABASE_HOST,
            user=Config.MYSQL_DATABASE_USER,
            password=Config.MYSQL_DATABASE_PASSWORD,
            database=Config.MYSQL_DATABASE_DB
        )

    @staticmethod
    def create_user(email, mobile, dob, postcode, username, password):
        conn = UserService.get_db_connection()
        cursor = conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            # Verificar si el nombre de usuario ya existe
            if UserService.username_exists(username):
                return False, "El nombre de usuario ya está en uso."
            # Verificar si el correo electrónico ya existe
            if UserService.email_exists(email):
                return False, "El correo electrónico ya está en uso."
            # Verificar si el número de teléfono ya existe
            if UserService.mobile_exists(mobile):
                return False, "El número de teléfono ya está en uso."
            
            cursor.execute('INSERT INTO users (email, mobile, dob, postcode, username, password) VALUES (%s, %s, %s, %s, %s, %s)', 
                            (email, mobile, dob, postcode, username, hashed_password))
            conn.commit()
            return True, "Usuario registrado con éxito."
        except mysql.connector.Error as err:
            return False, str(err)
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def validate_user(username, password):
        conn = UserService.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, hashed_password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    
    @staticmethod
    def username_exists(username):
        conn = UserService.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = %s', (username,))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count > 0
    
    @staticmethod
    def email_exists(email):
        conn = UserService.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE email = %s', (email,))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count > 0
    
    @staticmethod
    def mobile_exists(mobile):
        conn = UserService.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE mobile = %s', (mobile,))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count > 0

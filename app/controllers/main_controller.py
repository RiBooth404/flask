from flask import Blueprint, render_template

main_controller = Blueprint('main', __name__)

@main_controller.route('/')
def landing_page():
    return render_template('landing.html')

from flask import Flask, render_template, redirect, url_for, flash, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegisterForm
from werkzeug.security import check_password_hash, generate_password_hash
from blueprints.auth import user_mg, login_manager
from blueprints.tasks import task_mg
from database import db
from config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(user_mg)
app.register_blueprint(task_mg)

Bootstrap(app)

db.init_app(app)
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Czas trwania sesji

login_manager.init_app(app)
login_manager.login_view = 'user_mg.login'  

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Nie znaleziono'}), 404)

@app.route('/')
def start():
    return render_template('start.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
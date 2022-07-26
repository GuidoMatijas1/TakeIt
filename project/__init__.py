from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_mail import Mail, Message


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    app.config['SECRET_KEY'] = 'top-secret!'
    app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'apikey'
    # app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
    app.config['MAIL_PASSWORD'] = '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'
    # app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
    app.config['MAIL_DEFAULT_SENDER'] ='TakeItApp@takeit.lol'
    mail = Mail(app)
    # app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    # app.config['MAIL_PORT'] = 465
    # app.config['MAIL_USERNAME'] = 'takeitapp0@gmail.com'
    # app.config['MAIL_PASSWORD'] = 'jhoznewwarrylbws'
    # app.config['MAIL_USE_TLS'] = False
    # app.config['MAIL_USE_SSL'] = True
    #
    # mail = Mail(app)

    uploads_dir = os.path.join('project/static/images')

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    from .models import Gmah
    from .models import Products

    @login_manager.user_loader
    def load_user(user_id):
        gmah_user = Gmah.query.get(int(user_id))
        user_user = User.query.get(int(user_id))
        if gmah_user:
            return gmah_user
        if user_user:
            return user_user

    return app

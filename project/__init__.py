from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def create_app(database_uri="sqlite:///db.sqlite3"):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # blueprint for auth routes in the app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for social parts
    from .social import social as social_blueprint
    app.register_blueprint(social_blueprint)

    return app

app = create_app()
with app.app_context():
    db.create_all()
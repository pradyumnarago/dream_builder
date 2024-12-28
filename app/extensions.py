from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
bcrypt = Bcrypt()
from flask_mail import Mail

mail = Mail()

def init_app(app):
    """Initialize all the extensions."""
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Configure LoginManager
    login_manager.login_view = 'auth.login'  # Redirect to login page if not authenticated
    login_manager.login_message_category = 'info'  # Flash message category

    # Configure the app for Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'pradyumnaragothaman@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ejll pjhv qwqt mcmg'
    app.config['MAIL_DEFAULT_SENDER'] = 'pradyumnaragothaman@gmail.com'

    # Initialize Flask-Mail
    mail.init_app(app)

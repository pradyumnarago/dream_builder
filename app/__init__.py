from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.extensions import init_app,login_manager
from app.models.user_model import User  # Import User model
from flask import Flask, redirect, url_for

@login_manager.user_loader
def load_user(user_id):
    """Load user from the session."""
    return User.query.get(int(user_id))

# Initialize SQLAlchemy and Migrate globally

# def create_app():
#     app = Flask(__name__)
    
#     # Configurations
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Pradyu$#9164@localhost/dream_builder'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db = SQLAlchemy(app)
#     # Initialize the extensions with the app
#     #db.init_app(app)
#     migrate.init_app(app, db)  # Bind Flask-Migrate to the app and database
    
#     # Register your blueprints here (example)
#     from app.routes.auth_routes import auth_bp
#     from app.routes.dashboard import dashboard_bp
#     from app.routes.counselling import counselling_bp
#     from app.routes.progress import progress_bp
#     from app.routes.schedule import schedule_bp
#     from app.routes.habit import habit_bp

#     app.register_blueprint(auth_bp, url_prefix='/auth')
#     app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
#     app.register_blueprint(counselling_bp, url_prefix='/counselling')
#     app.register_blueprint(progress_bp, url_prefix='/progress')
#     app.register_blueprint(schedule_bp, url_prefix='/schedule')
#     app.register_blueprint(habit_bp, url_prefix='/habit')

#     return app

def create_app():
    global app
    # Configurations
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Pradyu$#9164@localhost/dream_builder'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    init_app(app)  # Correctly initialize db with the app

    # Import models (make sure to import models here to avoid circular imports)
    with app.app_context():
        from app.models import User, Chat, Schedule, Habit, HabitTracking, ScheduleTracking

    # Register your blueprints here (example)
    from app.routes.auth_routes import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.counselling import counselling_bp
    from app.routes.progress import progress_bp
    from app.routes.schedule import schedule_bp
    from app.routes.habit import habit_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(counselling_bp, url_prefix='/counselling')
    app.register_blueprint(progress_bp, url_prefix='/progress')
    app.register_blueprint(schedule_bp, url_prefix='/schedule')
    app.register_blueprint(habit_bp, url_prefix='/habit')
    
    @app.route('/')
    def root():
        # Redirect to the login page
        return redirect(url_for('auth.login'))

    return app

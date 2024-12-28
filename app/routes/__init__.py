# # app/routes/__init__.py

# from flask import Blueprint

# # Import individual blueprints from other route files
# from app.routes.auth_routes import auth_bp
# from app.routes.dashboard import dashboard_bp
# from app.routes.counselling import counselling_bp
# from app.routes.schedule import schedule_bp
# from app.routes.habit import habit_bp
# from app.routes.progress import progress_bp
# from app.routes.api import api_bp

# # List of all Blueprints to register in the main app
# blueprints = [
#     auth_bp,
#     dashboard_bp,
#     counselling_bp,
#     schedule_bp,
#     habit_bp,
#     progress_bp,
#     api_bp
# ]

# # Function to register all blueprints to the Flask app
# def register_blueprints(app):
#     for blueprint in blueprints:
#         app.register_blueprint(blueprint)

# from flask import Flask
# from app.routes.auth_routes import auth_bp
# from app.routes.dashboard import dashboard_bp
# from app.routes.counselling import counselling_bp
# from app.routes.progress import progress_bp
# from app.routes.schedule import schedule_bp
# from app.routes.habit import habit_bp

# def create_app():
#     app = Flask(__name__)
#     app.register_blueprint(auth_bp, url_prefix='/auth')
#     app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
#     app.register_blueprint(counselling_bp, url_prefix='/counselling')
#     app.register_blueprint(progress_bp, url_prefix='/progress')
#     app.register_blueprint(schedule_bp, url_prefix='/schedule')
#     app.register_blueprint(habit_bp, url_prefix='/habit')
#     return app


from flask import Blueprint, Flask

from app.routes.auth_routes import auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.counselling import counselling_bp
from app.routes.progress import progress_bp
from app.routes.schedule import schedule_bp
from app.routes.habit import habit_bp

# Register blueprints in the app
def init_app(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(counselling_bp, url_prefix='/counselling')
    app.register_blueprint(progress_bp, url_prefix='/progress')
    app.register_blueprint(schedule_bp, url_prefix='/schedule')
    app.register_blueprint(habit_bp, url_prefix='/habit')

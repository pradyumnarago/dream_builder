# #from app.routes import init_app
# from flask import Flask;
# from app.routes.auth_routes import auth_bp
# from app.routes.dashboard import dashboard_bp
# from app.routes.counselling import counselling_bp
# from app.routes.progress import progress_bp
# from app.routes.schedule import schedule_bp
# from app.routes.habit import habit_bp

# if __name__=="__main__":
#     app = Flask(__name__,template_folder='/templates')
#     app.register_blueprint(auth_bp, url_prefix='/auth')
#     app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
#     app.register_blueprint(counselling_bp, url_prefix='/counselling')
#     app.register_blueprint(progress_bp, url_prefix='/progress')
#     app.register_blueprint(schedule_bp, url_prefix='/schedule')
#     app.register_blueprint(habit_bp, url_prefix='/habit')

#     print("Blueprints registered:", app.blueprints)
#     app.run(debug=True)


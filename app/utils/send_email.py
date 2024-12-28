from flask_mail import Message
#from app import mail # Assuming you have Flask-Mail set up
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta
from app.extensions import mail,db
from app.config import Config
def generate_reset_token(user):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    token = serializer.dumps(user.email, salt='password-reset-salt')
    user.reset_token = token
    user.reset_token_expiration = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()
    return token

def send_password_reset_email(to_email, reset_link):
    """Send the password reset link via email."""
    msg = Message(
        subject='Password Reset Request',
        recipients=[to_email],
        body=f'Click the following link to reset your password: {reset_link}'
    )
    mail.send(msg)

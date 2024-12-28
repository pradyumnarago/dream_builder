from app import create_app
from flask import Flask, redirect, url_for

app = create_app()

@app.route('/')
def root():
    # Redirect to the login page
    return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.run(debug=True)

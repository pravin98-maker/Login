from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key for production

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect to 'login' page if unauthenticated

# User model
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# In-memory user data (for demo purposes only)
users = {
    "user1": User(1, "user1", "password1"),
    "user2": User(2, "user2", "password2")
}

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((u for u in users.values() if u.username == username and u.password == password), None)
        
        if user:
            login_user(user)
            return redirect(url_for('protected'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/protected')
@login_required
def protected():
    return f'Hello, {current_user.username}! You are logged in.'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)

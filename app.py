from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Simulated user database
users = {
    "user": "password"  # Example username and password
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('welcome'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('home'))

@app.route('/welcome')
def welcome():
    if 'username' in session:
        return f'Welcome, {session["username"]}!'
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)


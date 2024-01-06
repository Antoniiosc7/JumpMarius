from flask import Flask, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess, os
from flask_login import login_required
from flask_login import LoginManager
app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager(app)
CORS(app, supports_credentials=True)

users_db = {}
scores_db = {}
users_db['user'] = generate_password_hash('password')
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users_db and check_password_hash(users_db[username], password):
        session['username'] = username
        print("Login successful")

        # Obtén la ruta del directorio actual
        current_directory = os.path.dirname(os.path.realpath(__file__))

        # Construye la ruta completa al script menu.py
        menu_script_path = os.path.join(current_directory, '..', 'menu.py')

        # Ejecuta el script menu.py
        os.system(f"python {menu_script_path}")
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
@app.route('/get_users', methods=['GET'])
@login_required
def get_users():
    return jsonify(list(users_db.keys()))

# Resto del código...
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/save_score', methods=['POST'])
def save_score():
    if 'username' in session:
        username = session['username']
        data = request.get_json()
        score = data.get('score')

        if username in scores_db:
            scores_db[username] = max(scores_db[username], score)
        else:
            scores_db[username] = score

        return jsonify({'message': 'Score saved successfully'}), 200
    else:
        return jsonify({'message': 'User not logged in'}), 401

@app.route('/get_top_scores', methods=['GET'])
def get_top_scores():
    top_scores = sorted(scores_db.items(), key=lambda x: x[1], reverse=True)[:10]
    return jsonify(top_scores)

if __name__ == '__main__':
    app.run(debug=True)

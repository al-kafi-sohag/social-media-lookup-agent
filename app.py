from flask import Flask, render_template, request, jsonify, session, Response
from flask_session import Session
from main import process_social_media_lookup
import time
import uuid
import secrets

app = Flask(__name__, template_folder='views/')
app.secret_key = secrets.token_hex(16)  # Generates a 32-character hexadecimal string

# Configure server-side session
app.config['SESSION_TYPE'] = 'filesystem'  # You can also use 'redis', 'memcached', etc.
Session(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'userName' in request.form:
            user_input = request.form['userName']
            chat_id = str(uuid.uuid4())
            session[chat_id] = []
            process_social_media_lookup(user_input, session, chat_id)
            return jsonify({"chat_id": chat_id})
        else:
            return jsonify({"status": 0, "message": "Invalid request"})

    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    if 'chat_id' in data:
        chat_id = data['chat_id']
        if chat_id in session:
            result = session[chat_id]
            return jsonify({"status": 1, "result": result})
        else:
            return jsonify({"status": 0, "message": "Invalid chat ID"})
    else:
        return jsonify({"status": 0, "message": "Invalid request"})

@app.route('/check_session', methods=['GET'])
def check_session():
    return jsonify(dict(session))

@app.route('/clear_sessions', methods=['GET'])
def clear_sessions():
    session.clear()
    return jsonify({"status": 1, "message": "All sessions cleared"})

if __name__ == '__main__':
    app.run(debug=True)
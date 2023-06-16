import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
messages = []
usernames = set()
dev_menu_opened = False
dev_password = "devpassword"

# Scan the "backgrounds" folder for image files
backgrounds_folder = "backgrounds"
backgrounds = []
if os.path.isdir(backgrounds_folder):
    for filename in os.listdir(backgrounds_folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
            backgrounds.append(filename)


@app.route('/')
def index():
    return render_template('ModernOne.html', backgrounds=backgrounds)


# Add the '/dev_menu' route to handle dev menu actions
@app.route('/dev_menu', methods=['POST'])
def dev_menu():
    global dev_menu_opened
    action = request.form['action']
    password = request.form['password']

    if action == 'open':
        if password == dev_password:
            dev_menu_opened = True
    elif action == 'close':
        dev_menu_opened = False
    elif action == 'clear_messages':
        if dev_menu_opened:
            messages.clear()

    return jsonify({'success': True})


@app.route('/chat')
def chat():
    return jsonify(messages)


@app.route('/send', methods=['POST'])
def send():
    message = request.form['message']
    username = request.form['username']
    messages.append({'username': username, 'message': message})
    return jsonify({'username': username, 'message': message})


@app.route('/join', methods=['POST'])
def join():
    username = request.form['username']
    if username in usernames:
        return jsonify({'error': 'Username already taken'})
    usernames.add(username)
    messages.append({'username': 'ChatBot', 'message': f'{username} joined the chat'})
    return jsonify({'username': username})


@app.route('/leave', methods=['POST'])
def leave():
    username = request.form['username']
    usernames.remove(username)
    messages.append({'username': 'ChatBot', 'message': f'{username} left the chat'})
    return jsonify({'message': 'Left the chat'})


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)

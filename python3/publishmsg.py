from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# The secret key is needed for some session features, any string works
app.config['SECRET_KEY'] = 'pi-secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    # data is a dict: {'msg': 'hello', 'id': 'socket_id'}
    # This sends it to everyone, including the sender
    emit('message', data, broadcast=True)

if __name__ == '__main__':
    # host='0.0.0.0' allows access from other devices on your network
    socketio.run(app, host='0.0.0.0', port=15, debug=True)

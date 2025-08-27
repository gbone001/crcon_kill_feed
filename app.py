import os
import json
from flask import Flask, send_from_directory, jsonify
from flask_socketio import SocketIO, emit
from log_stream_manager import LogStreamManager
from helpers.filters import parse_args, should_show_kill

app = Flask(__name__, static_folder='public')
socketio = SocketIO(app, cors_allowed_origins="*")

filters = parse_args()
log_stream_manager = LogStreamManager()
connected_clients = set()

@app.route('/filters.json')
def filters_json():
    return jsonify(filters)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@socketio.on('connect')
def handle_connect():
    connected_clients.add(request.sid)

@socketio.on('disconnect')
def handle_disconnect():
    connected_clients.discard(request.sid)

# Listen for KILL events from log stream manager
@log_stream_manager.on('KILL')
def handle_kill(log):
    if not should_show_kill(log, filters):
        return
    data = { 'type': 'KILL', 'payload': log }
    socketio.emit('kill_event', data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    log_stream_manager.subscribe('KILL')
    log_stream_manager.start()
    print(f"🎯 Kill Feed Server running at http://localhost:{port}")
    print("🛠 Filters:", filters)
    socketio.run(app, port=port)

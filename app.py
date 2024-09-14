from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send, emit
from flask_socketio import disconnect

app = Flask(__name__)
socketio = SocketIO(app)  # 初始化 Flask-SocketIO


# 处理 GET 请求
@app.route('/get_example', methods=['GET'])
def get_example():
    message = request.args.get('message', 'Hello, World!')
    return jsonify({
        'method': 'GET',
        'message': message
    })


# 处理 POST 请求
@app.route('/post_example', methods=['POST'])
def post_example():
    data = request.json
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    message = data.get('message', 'No message received')
    return jsonify({
        'method': 'POST',
        'received_message': message
    })


# 用于存储每个客户端的连接
clients = {}


# WebSocket 连接事件
@socketio.on('connect')
def handle_connect():
    session_id = request.sid  # 获取当前连接的 session ID
    clients[session_id] = request.remote_addr  # 将客户端存储到字典中
    print(f'Client {session_id} connected from {request.remote_addr}')
    emit('message', 'Welcome to the WebSocket server!')  # 向客户端发送欢迎信息


# WebSocket 断开连接事件
@socketio.on('disconnect')
def handle_disconnect():
    session_id = request.sid  # 获取当前连接的 session ID
    if session_id in clients:
        print(f'Client {session_id} disconnected')
        clients.pop(session_id)  # 移除客户端
    else:
        print(f'Unknown client {session_id} tried to disconnect')


# 处理 WebSocket 收到的消息并回复该客户端
@socketio.on('message')
def handle_message(message):
    session_id = request.sid  # 获取当前客户端的 session ID
    print(f'Received message from {session_id}: {message}')

    # 向特定客户端发送消息（非广播）
    emit('message', f'Server received your message: {message}', to=session_id)
    # send(f'Server received: {message}', broadcast=True)  # 广播给所有连接的客户端


if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)  # 允许使用 Werkzeug

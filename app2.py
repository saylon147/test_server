import socket


# 创建 TCP 服务器
def start_server():
    host = '127.0.0.1'  # 服务器地址
    port = 5000  # 服务器端口

    # 创建 TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定服务器地址和端口
    server_socket.bind((host, port))

    # 启动监听
    server_socket.listen(1)
    print(f"Server started and listening on {host}:{port}...")

    # 接受客户端连接
    conn, addr = server_socket.accept()
    print(f"Connection from {addr} established!")

    while True:
        # 接收客户端发送的数据
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        print(f"Received from client: {data}")

        # 根据接收的数据回复客户端
        if data == '你好！':
            conn.send('你发送了：你好！'.encode('utf-8'))
        elif data == '再见！':
            conn.send('断开连接'.encode('utf-8'))
            break   # 断开了客户端
        else:
            conn.send('未知消息'.encode('utf-8'))

    # 关闭连接
    conn.close()
    print("Connection closed.")


if __name__ == '__main__':
    start_server()

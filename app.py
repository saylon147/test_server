from flask import Flask, request, jsonify

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import socket
import json
import threading
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    file = '/index.html'
    return render_template(file)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    file = '/contact.html'
    if request.method == 'POST':
        try:
            host = socket.gethostname()
            port = 5000
            client_socket = socket.socket()
            client_socket.connect((host, port))

            name = request.form['name']
            mail = request.form['email']
            text = request.form['text']
            message = [name, mail, text]

            # Convert the list to a JSON string and encode it to bytes
            message = json.dumps(message).encode('utf-8')
            client_socket.send(message)

            client_socket.close()
        except Exception as e:
            return render_template('error.html')  # Redirect to error page
            

    return render_template(file)

@app.errorhandler(500)
def internal_error(error):
    return render_template('/error.html'), 500 

def run_flask_app():
    app.run(host='0.0.0.0', port=3000)

def run_socket_server():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)

    while True:
        connection, address = server_socket.accept()

        # Receive the data and decode it from bytes to a JSON string
        data = connection.recv(1024).decode('utf-8')
        # Convert the JSON string back to a list
        data = json.loads(data)

        # Check if the directory exists and create it if it doesn't
        if not os.path.exists('Task_4/storage'):
            os.makedirs('Task_4/storage')

        # Check if the file exists and create it if it doesn't
        if not os.path.isfile('Task_4/storage/data.json'):
            with open('Task_4/storage/data.json', 'w') as f:
                json.dump({}, f)

        # Save the data to a JSON file
        with open('Task_4/storage/data.json', 'a') as f:
            json.dump({str(datetime.now()): data}, f)

if __name__ ==  '__main__':
    # Run the Flask app and the socket server in different threads
    threading.Thread(target=run_flask_app).start()
    threading.Thread(target=run_socket_server).start()

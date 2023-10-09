import random
from socket import *
from threading import *
import json

server_name = 'localhost'
server_port = 1500

def handle_client(client_socket, addr):
    try:
        request = client_socket.recv(2048).decode()
        request_data = json.loads(request)

        method = request_data.get("method", "").lower()
        num_1 = request_data.get("Number1", 0)
        num_2 = request_data.get("Number2", 0)

        response = {}

        if method == "random":
            response["result"] = random.randint(num_1, num_2)
        elif method == "add":
            response["result"] = num_1 + num_2
        elif method == "subtract":
            response["result"] = num_1 - num_2
        else:
            response["error"] = "invalid operation"

        client_socket.send(json.dumps(response).encode())

    except Exception as e:
        print(f"an error occured while handling client {addr}: {e}")
    finally:
        client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', server_name))
    server_socket.listen(5)
    print(f'server is ready and listening on port {server_port}')

    while 1:
        connection_socket, addr = server_socket.accept()
        print(f'Connected to a client from address {addr}')
        Thread(target=handle_client, args=(connection_socket, addr)).start()

    client_socket = socket(AF_INET, SOCK_STREAM)

    try:
        client_socket.connect((server_name, server_port))

        method = input('choose operation (Random/Add/Subtract): ')
        num_1 = int(input('enter number1: '))
        num_2 = int(input('enter number2: '))

        request_data = {
            "method": method,
            "Number1": num_1,
            "Number2": num_2
        }

        client_socket.send(json.dumps(request_data).encode())

        response = client_socket.recv(2048).decode()
        response_data = json.loads(response)

        if "result" in response_data:
            print('response from server:', response_data["result"])
        elif "error" in response_data:
            print('error from server:', response_data["error"])

    except Exception as e:
        print(f'an error occurred: {e}')
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
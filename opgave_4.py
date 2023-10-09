import random
from socket import *
from threading import *

server_name = 'localhost'
server_port = 1500

def handle_client(client_socket, addr):
    try:
        request = client_socket.recv(2048).decode()
        request_data = request.split()
        response = ''

        if(request_data[0].lower() == "random"):
            num_1 = int(request_data[1])
            num_2 = int(request_data[2])
            response = f'random number between {num_1} and {num_2} =  {(random.randint(num_1,num_2))}'
        elif(request_data[0].lower() == "add"):
            num_1 = int(request_data[1])
            num_2 = int(request_data[2])
            response = f'{num_1} + {num_2} = {(num_1+num_2)}'
        elif(request_data[0].lower() == "subtract"):
            num_1 = int(request_data[1])
            num_2 = int(request_data[2])
            response = f'{num_1} - {num_2} = {(num_1-num_2)}'
        else:
            response = f'operation not valid {request_data[0]}'

        client_socket.send(response.encode())
        
    except Exception as e:
        print(f"an error occured while handling client {addr}: {e}")
    finally:
        client_socket.close()

def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(1)
    print('server is ready and listening on port', server_port)

    while 1:
        connection_socket, addr = server_socket.accept()
        print('connected to a client from address', addr)
        Thread(target=handle_client, args=(connection_socket, addr)).start()

    client_socket = socket(AF_INET, SOCK_STREAM)
    server_port = 1500

    try:
        client_socket.connect((server_name, server_port))

        request = input('choose operation (Random/Add/Subtract): ')
        num_1 = int(input('enter number1: '))
        num_2 = int(input('enter number2: '))

        request_data = f'{request} {num_1} {num_2}'

        client_socket.send(request_data.encode())

        response = client_socket.recv(2048)
        print('response from server:', response)

    except Exception as e:
        print(f'an error occurred while trying to execute operation: {e}')
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()


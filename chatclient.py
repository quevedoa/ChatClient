from email.base64mime import header_length
import socket
import sys

HEADER_LENGTH = 10

IP = "143.47.184.219"
PORT = 5378

my_username = input("Username: ")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
s.setblocking(False)

username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
s.sendall(username_header + username)

while True:
    message = input(f"{my_username} > ")

    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        s.sendall(message_header + message)

    try:
        while True:
            # Receive things
            res_username_header = s.recv(HEADER_LENGTH)
            if not len(res_username_header):
                print("connection closed by the server")
                sys.exit()

            username_length = int(res_username_header.decode("utf-8").strip())
            username = s.recv(username_length).decode("utf-8")

            message_header = s.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = s.recv(message_length).decode("utf-8")

            print(f"{username} > {message}")
    except Exception as e:
        print("General error", str(e))
        sys.exit()

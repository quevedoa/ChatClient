from email import message
from email.base64mime import header_length
import socket
import re
import threading
import sys

finished = False
userTaken = True
username = ""
again = False

IP = "143.47.184.219"
PORT = 5378

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))


def listen_to_server():
    while True:
        try:
            server_message = s.recv(1024).decode("utf-8")[:-1]
            if re.match(r"WHO-OK", server_message):
                list_users = server_message.split(" ")[1:]
                print(f"Online Users: {list_users}")
            elif re.match(r"SEND-OK", server_message):
                pass
            elif re.match(r"UNKNOWN", server_message):
                print("User is not logged in yet.")
            elif re.match(r"DELIVERY", server_message):
                message = re.search(r"DELIVERY ([\w\.-]+) ([\w\s]+)", server_message)
                print(f"\n{message.group(1)} > {message.group(2)}")
            elif re.match(r"IN-USE", server_message):
                print(f"Username already taken. Try again.")
                # username = ""
                # username = input("Username: ")
                # first_handshake = f"HELLO-FROM {username}\n".encode("utf-8")
                # s.sendall(first_handshake)
            elif re.match(r"HELLO", server_message):
                userTaken = False
                print(f"Login Successful!\n")
            elif re.match(r"BUSY", server_message):
                pass
            elif re.match(r"BAD-RQST-HDR", server_message):
                pass
            elif re.match(r"BAD-RQST-BODY", server_message):
                pass
        except OSError as msg:
            print(msg)


t = threading.Thread(target=listen_to_server, daemon=True)
t.start()


def check_online_users():
    # Check who is online and adds them to a list
    who_online = f"WHO\n".encode("utf-8")
    s.sendall(who_online)
    t.join(0.3)


# Main Loop

username = input("Username: ")
first_handshake = f"HELLO-FROM {username}\n".encode("utf-8")
s.sendall(first_handshake)

check_online_users()

while True:
    command = input(f"{username} > ")

    if command == "!quit":
        print("Goodbye.")
        sys.exit()

    if command == "!who":
        check_online_users()

    elif re.search(r"@([\w\.-]+?) ([\w\s]+)", command):
        match = re.search(r"@([\w\.-]+?) ([\w\s]+)", command)
        recipient = match.group(1)
        body = match.group(2)
        command = f"SEND {recipient} {body}"
        s.sendall(f"{command}\n".encode("utf-8"))
        t.join(0.3)

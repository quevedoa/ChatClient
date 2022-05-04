from logging import raiseExceptions
import socket
import re
import threading
import sys

userTaken = True
stop_thread = False

# IP = "143.47.184.219"
# PORT = 5378

IP = "192.168.16.44"
PORT = 1234


def deleteLastLine():
    # Writes ANSI codes to perform cursor movement and current line clear
    cursorUp = "\x1b[1A"
    eraseLine = "\x1b[2K"
    sys.stdout.write(cursorUp)
    sys.stdout.write(eraseLine)


def check_online_users():
    # Check who is online and adds them to a list
    who_online = f"WHO\n".encode("utf-8")
    s.sendall(who_online)
    listen_thread.join(0.2)


while userTaken:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    try:
        username = input("Username: ")
        first_handshake = f"HELLO-FROM {username}"
        s.sendall(f"{first_handshake}\n".encode("utf-8"))
        handshake = s.recv(1024).decode("utf-8")[:-1]
        if re.match(r"HELLO", handshake):
            userTaken = False
            print(f"Login Successful!\n")
        elif re.match(r"IN-USE", handshake):
            print("Username already in use. Try with another one.")
            s.close()
        elif re.match(r"BUSY", handshake):
            print("Server is too busy. Try again later.")
            s.close()
            sys.exit()
    except Exception as ex:
        print(ex)
        sys.exit()


def listen():
    while True:
        try:
            server_message = s.recv(2).decode("utf-8")
            while not server_message.endswith("\n"):
                server_message += s.recv(2).decode("utf-8")
            if re.match(r"WHO-OK", server_message):
                list_users = server_message[:-1].split(" ")[1:]
                print(f"Online Users: {list_users}")
            elif re.match(r"SEND-OK", server_message):
                pass
            elif re.match(r"UNKNOWN", server_message):
                print("User is not logged in yet.")
            elif re.match(r"DELIVERY", server_message):
                message = re.search(r"DELIVERY ([\w\.-]+) ([\w\s]+)", server_message)
                print(f"\n{message.group(1)} > {message.group(2)}")
            elif re.match(r"HELLO", server_message):
                print(f"Login Successful!\n")
            elif re.match(r"BAD-RQST-HDR", server_message):
                pass
            elif re.match(r"BAD-RQST-BODY", server_message):
                pass
            else:
                raiseExceptions()
        except Exception as ex:
            s.close()
            break


def write():
    while True:
        command = input(f"{username} > ")

        if command == "!quit":
            s.sendall("!quit\n".encode("utf-8"))
            print("Goodbye.")
            s.close()
            sys.exit()

        if command == "!who":
            check_online_users()

        elif re.search(r"@([\w\.-]+?) ([\w\s]+)", command):
            match = re.search(r"@([\w\.-]+?) ([\w\s]+)", command)
            recipient = match.group(1)
            body = match.group(2)
            command = f"SEND {recipient} {body}"
            s.sendall(f"{command}\n".encode("utf-8"))


listen_thread = threading.Thread(target=listen)
listen_thread.start()

check_online_users()
print()

write_thread = threading.Thread(target=write)
write_thread.start()

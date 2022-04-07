import socket as s
import threading as t

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
host_port = ("143.47.184.219", 5378)
sock.connect(host_port)

## send data to the other application
buffer = "Sockets are great!".encode("utf-8")
num_bytes_sent = sock.send(buffer)
sock.sendall(buffer)


# sendall calls send repeatedly until all bytes are sent.
#string_bytes = "Sockets are great!".encode("utf-8")
#sock.sendall(string_bytes)

## receive data from the other application
# Waiting until data comes in; receive at most 4096 bytes.
data = sock.recv(4096)

if not data:
    print("Socket is closed.")
else:
    print("Socket has data.")

# exceptions
try:
    sock.send("how to handle errors?".encode("utf-8"))
    answer = sock.recv(4096)
except OSError as msg:
    print(msg)

## closing the connection
sock.close()

# threading: the args par must be a tuple!
thread = t.Thread(target=print, args=("hello", "world"))

# running the function specified in a new thread
thread.start()

# waiting for the thread to finish (100 ms in this case)
thread.join(0.1)

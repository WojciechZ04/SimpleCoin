import socket
import threading
import time


print(threading.active_count(),'aktywne')
HEADER = 64
PORT = 5051
# Pobierz nazwę hosta komputera
host_name = socket.gethostname()

# Pobierz adres IP na podstawie nazwy hosta
SERVER = socket.gethostbyname(host_name)
print(SERVER)

ADDR = (SERVER, PORT)
print(ADDR)
FORMAT ='utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        print('ile tu widac konekszyns?:' , len(connections))
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
    conn.close()



connections = []
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        connections.append((conn,addr))
        print('konekszyns', len(connections))
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        print(thread)
        thread.start()
        time.sleep(0.5)
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
print("[STARTING] server is starting...")
start()

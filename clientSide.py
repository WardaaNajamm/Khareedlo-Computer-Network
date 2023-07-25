import socket
from ftpClient import ftp_client
from smtpClient import Feedback
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

    connected = True
    Servermsg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER] {Servermsg}")
    
    while connected:
        Clientmsg = input("> ")
        client.send(Clientmsg.encode(FORMAT))

        if Clientmsg == "q": #DISCONNECT_MSG:
            connected = False
        elif Clientmsg == "feedback":
            Servermsg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {Servermsg}")
            username = input(">Enter your email: ")
            password = input(">Enter your password: ")
            Feedback(username,password)
        elif Clientmsg == "5":
            Servermsg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {Servermsg}")
            username = input(">Enter your KAREEDLO username: ")
            password = input(">Enter your KAREEDLO password: ")
            ftp_client("127.0.0.1",username,password)
        else:
            Servermsg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {Servermsg}")

if __name__ == "__main__":
    main()
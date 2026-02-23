
import socket
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

HOST = "0.0.0.0"
PORT = int(input("Insert port: "))
FOLDER = str(input("Insert project folder path: "))

clients = []

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        file_path = event.src_path

        try:
            with open(file_path, "rb") as f:
                content = f.read()

                data = {
                    "path": os.path.relpath(file_path, FOLDER),
                    "content": content.decode("latin1")
                }
                message = json.dumps(data).encode("latin1")
                for client in clients:
                    client.sendall(message)

                print("File modified:", file_path)
        except Exception as e:
            print("Error:", e)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("Server is starting...")

    while True:
        conn, adrr = server.accept()
        clients.append(conn)
        print("Client connected:", adrr)


if __name__ == "__main__":
    observer = Observer()
    observer.schedule(ChangeHandler(), FOLDER, recursive=True)
    observer.start()
    start_server()

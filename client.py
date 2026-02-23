
import socket
import json
import os
from time import sleep


def load_env(path="data.env"):
    if not os.path.exists(path):
        return

    with open(path) as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            key, value = line.split("=", 1)
            os.environ[key.strip()] = value.strip()


load_env()
sleep(1)
print("loaded env",os.environ.get("SERVER_IP"))
SERVER_IP = os.environ["SERVER_IP"]
PORT = int(input("Insert port: "))
FOLDER = str(input("Insert destination folder path: "))


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))
    print("Conectando al servidor...")

    while True:
        data = client.recv(9999999)
        if not data: break
        info = json.loads(data.decode("latin1"))
        file_path = os.path.join(FOLDER, info["path"])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(info["content"].encode("latin1"))
        print("File received:", file_path)

if __name__ == "__main__":
    start_client()


# Server-Skript: server.py


import socket
import threading

import json
import time
import configparser

import logging

# Logger konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# config files
CONFIG_FILE = "./config.cfg"

# user & password file
USER_PASSWD_DB = "./user_passwd.txt"


    # Windows Server
    #with open("C:\user_passwd.txt", "r") as file:


# Globale Variable für Benutzerdaten
user_data_cache = []
TIMEOUT = 10



def read_user_data():
    global user_data_cache
    while True:
        try:
            with open(USER_PASSWD_DB, "r") as file:
                user_data_cache = json.load(file)
        except Exception as e:
            logger.error(f"Fehler beim Lesen der Datei: {e}")
        time.sleep(TIMEOUT)  # Aktualisieren der Benutzerdaten basierend auf dem Timeout-Wert

def validate_token(token):
    for user in user_data_cache:
        if user["token"] == token:
            return user
    return None

def handle_client(connection, address):
    while True:
        try:
            data = connection.recv(1024).decode()
            if not data:
                break

            user_info = validate_token(data)
            if user_info:
                response = json.dumps(user_info)
                connection.sendall(response.encode())
            else:
                logger.error("Ungültiges Token.")
                connection.sendall("Wrong token".encode('utf-8'))
        except Exception as e:
            logger.error(f"Fehler bei der Kommunikation mit {address}: {e}")
            break

    connection.close()

def start_server():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    port = config.getint('Server', 'port', fallback=8798)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Hinzufügen dieser Zeile
    server.bind(("0.0.0.0", port))
    server.listen()
    logger.info(f"Server lauscht auf Port {port}")

    user_data_thread = threading.Thread(target=read_user_data, daemon=True)
    user_data_thread.start()

    while True:
        conn, addr = server.accept()
        logger.info(f"Verbunden mit {addr}")
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()


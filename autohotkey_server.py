

# Server-Skript: server.py

import socket
import threading
import json
import time

        #with open("C:\user_passwd.txt", "r") as file:


def read_user_data():
    try:
        with open("./user_passwd.txt", "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {e}")
        return []

def handle_client(connection, address):
    while True:
        user_data = read_user_data()

        if user_data:
            try:
                # Senden der gesamten Liste der Benutzerdaten auf einmal
                connection.sendall(json.dumps(user_data).encode())
                time.sleep(6)  # Warten zwischen dem Senden jedes Benutzers
            except Exception as e:
                print(f"Fehler beim Senden der Daten an {address}: {e}")
                connection.close()  # Schließt die Verbindung im Fehlerfall
                return  # Beendet den aktuellen Thread
        else:
            print("Keine Benutzerdaten zum Senden.")
            time.sleep(10)  # Verbindung schließen und Thread beenden bei Fehler

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8798))
    server.listen()
    print("Server lauscht auf Port 8798")

    while True:
        conn, addr = server.accept()
        print(f"Verbunden mit {addr}")
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()

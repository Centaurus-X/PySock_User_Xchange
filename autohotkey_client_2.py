
# autohotkey_client


import socket

import os
import time
import json

import keyboard
import struct
import netifaces as ni
import configparser

import threading
import subprocess
import concurrent.futures

import logging

# Logger konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# config files
CONFIG_FILE = "./config.cfg"


def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config['SERVER']['IP'], int(config['SERVER']['PORT'])


def connect_to_server(ip, port):
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))
            logger.info("Verbindung zum Server hergestellt.")
            return client
        except Exception as e:
            logger.error(f"Verbindungsfehler: {e}")
            time.sleep(5)


def send_token_and_receive_data(ip, port):
    client_socket = None
    while True:
        try:
            # Verbindung herstellen, falls noch nicht geschehen
            if client_socket is None:
                client_socket = connect_to_server(ip, port)

            token = input("Bitte Token eingeben: ")
            client_socket.send(token.encode())

            data = client_socket.recv(1024)
            if not data:
                raise Exception("Verbindung zum Server verloren.")
            logger.info(f"Daten empfangen: {data.decode()}")

        except Exception as e:
            logger.error(f"Fehler bei der Datenübertragung: {e}")
            client_socket = None  # Setzt client_socket zurück, um erneute Verbindung zu initiieren
            time.sleep(5)  # Wartezeit vor dem erneuten Verbindungsversuch


def authenticate_and_login():
    # Hier implementieren wir die Legitimations- und Anmelde-Logik
    # Diese Funktion wird im neuen Thread ausgeführt
    logger.info("Legitimation gestartet.")
    # Befehl zum Ausführen der T2med-Anwendung mit Administratorrechten
    cmd = "runas /user:Administrator /savecred \"C:\\Path\\to\\T2med.exe\""  # Ersetzen Sie "C:\\Path\\to\\T2med.exe" durch den tatsächlichen Pfad zur T2med-Anwendung
    subprocess.Popen(cmd, shell=True)  # Führt den Befehl aus


def listen_for_hotkey():
    # Diese Funktion wird im Hauptthread ausgeführt und hört auf die Tastenkombination
    while True:
        if keyboard.is_pressed("ctrl+alt+r"):
            logger.info("Tastenkombination erkannt. Legitimation wird gestartet.")
            threading.Thread(target=authenticate_and_login).start()
            time.sleep(1)  # Um mehrfaches Auslösen der Tastenkombination zu verhindern


if __name__ == "__main__":
    server_ip, server_port = load_config()
    # Starten Sie den Thread, der auf die Tastenkombination hört
    threading.Thread(target=listen_for_hotkey).start()
    # Starten Sie den Thread, der die Kommunikation mit dem Server übernimmt
    threading.Thread(target=send_token_and_receive_data, args=(server_ip, server_port)).start()




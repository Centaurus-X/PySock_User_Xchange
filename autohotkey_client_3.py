
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

def automatic_login(username, password):
    try:
        # Starten des Anmeldeprozesses
        subprocess.Popen(["T2med.exe"])
        time.sleep(2)  # Wartezeit für das Öffnen des Programms

        # Automatische Eingabe von Benutzername und Passwort
        keyboard.write(username)
        keyboard.press_and_release('tab')  # Wechsel zum Passwortfeld
        keyboard.write(password)
        keyboard.press_and_release('enter')  # Anmeldung

        logger.info("Automatische Anmeldung abgeschlossen.")
    except Exception as e:
        logger.error(f"Fehler bei der automatischen Anmeldung: {e}")

def hotkey_listener(ip, port):
    while True:
        # Warten auf die Tastenkombination "Strg + Alt + R"
        keyboard.wait('ctrl+alt+r')
        logger.info("Tastenkombination erkannt. Starte Token-Eingabe.")

        # Token-Eingabe und Authentifizierungsprozess
        client_socket = connect_to_server(ip, port)
        token = keyboard.read_event(suppress=False)  # Token-Eingabe über RFID-Lesegerät
        client_socket.send(token.name.encode())  # Sendet das Token an den Server

        data = client_socket.recv(1024).decode()
        if data:
            username, password = json.loads(data)
            automatic_login(username, password)
        else:
            logger.error("Keine Daten vom Server erhalten.")

if __name__ == "__main__":
    server_ip, server_port = load_config()
    threading.Thread(target=send_token_and_receive_data, args=(server_ip, server_port)).start()
    threading.Thread(target=hotkey_listener, args=(server_ip, server_port)).start()





# autohotkey_client


import socket

import os
import time
import json

import keyboard
import pynput
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
    # Ändern Sie die Verwendung des keyboard-Moduls in pynput_keyboard
    try:
        # Starting the login process
        subprocess.Popen(["T2med.exe"])
        time.sleep(2)  # Waiting for the program to open

        # Automatic input of username and password
        keyboard_controller = pynput_keyboard.Controller()
        keyboard_controller.type(username)
        keyboard_controller.press(pynput_keyboard.Key.tab)
        keyboard_controller.release(pynput_keyboard.Key.tab)
        keyboard_controller.type(password)
        keyboard_controller.press(pynput_keyboard.Key.enter)
        keyboard_controller.release(pynput_keyboard.Key.enter)

        logger.info("Automatische Anmeldung abgeschlossen.")
    except Exception as e:
        logger.error(f"Fehler bei der automatischen Anmeldung: {e}")

def read_token_from_device():
    # Placeholder function to simulate token reading from device
    # Replace this with actual token reading logic
    time.sleep(3)  # Simulate delay in reading token
    return "example_token"

def on_activate(ip, port):
    logger.info("Hotkey aktiviert. Warte auf Token...")
    client_socket = connect_to_server(ip, port)

    token = read_token_from_device()
    client_socket.send(token.encode())

    data = client_socket.recv(1024).decode()
    if data:
        username, password = json.loads(data)
        automatic_login(username, password)
    else:
        logger.error("Keine Daten vom Server erhalten.")

def hotkey_listener():
    def on_press(key):
        if key == keyboard.Key.esc:
            return False  # Stop listener
        if any([key == keyboard.Key.ctrl_l, key == keyboard.Key.alt_l]):
            current_keys.add(key)
        if key == keyboard.KeyCode.from_char('r'):
            if all(k in current_keys for k in [keyboard.Key.ctrl_l, keyboard.Key.alt_l]):
                on_activate(server_ip, server_port)

    def on_release(key):
        try:
            current_keys.remove(key)
        except KeyError:
            pass

    while True:
        keyboard.on_press(on_press)
        keyboard.on_release(on_release)

if __name__ == "__main__":
    server_ip, server_port = load_config()
    current_keys = set()

    listener_thread = threading.Thread(target=hotkey_listener)
    listener_thread.start()




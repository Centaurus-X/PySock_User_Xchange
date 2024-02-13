
# autohotkey_client

import os
import time
import json

import socket
import struct
import netifaces as ni

import concurrent.futures

#Port_Range 8798, 8800


def is_port_open(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((ip, port))
            return True
    except:
        return False

def find_server(subnet, start_port=8790, end_port=8800):
    subnet_base = '.'.join(subnet.split('.')[:-1])  # Entfernt das letzte Segment
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_ip_port = {executor.submit(is_port_open, f"{subnet_base}.{i}", port): (f"{subnet_base}.{i}", port) 
                             for i in range(1, 255) for port in range(start_port, end_port + 1)}

        for future in concurrent.futures.as_completed(future_to_ip_port):
            ip, port = future_to_ip_port[future]
            if future.result():
                print(f"Server gefunden: {ip} auf Port {port}")
                return ip, port
    return None, None


def connect_to_server(ip, port):
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))
            return client
        except Exception as e:
            print(f"Verbindungsfehler: {e}")
            time.sleep(5)  # Wartezeit vor dem erneuten Verbindungsversuch


def receive_data_from_server(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Daten empfangen:", data.decode())
            write_to_autohotkey_file(data.decode(), "./autohotkey_script.ahk")  #"C:\\autohotkey_script.ahk")
        except Exception as e:
            print(f"Fehler beim Empfangen der Daten: {e}")
            break
    client_socket.close()


def write_to_autohotkey_file(data, file_path):
    try:
        user_data = json.loads(data)

        # Liest den aktuellen Inhalt der Datei
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Bestimmt, welche Benutzernamen bereits existieren
        existing_user_lines = set(line for line in lines if line.startswith("user_name_"))

        # Aktualisiert existierende Benutzerdaten und fügt neue hinzu
        updated_content = []
        for i, user in enumerate(user_data, start=1):
            user_line = f"user_name_{i}: {user['user_name']}\n"
            pass_line = f"password_{i}: {user['password']}\n"
            if user_line in existing_user_lines:
                # Aktualisiert existierende Zeilen
                updated_content.extend([user_line, pass_line])
                existing_user_lines.remove(user_line)
            else:
                # Fügt neue Benutzerdaten hinzu
                updated_content.append(user_line)
                updated_content.append(pass_line)

        # Fügt den restlichen Code bei, ausgenommen der veralteten Benutzerdaten
        updated_content.extend(line for line in lines if not line.startswith(("user_name_", "password_")))

        # Schreibt den aktualisierten Inhalt zurück in die Datei
        with open(file_path, 'w') as file:
            file.writelines(updated_content)
    except Exception as e:
        print(f"Fehler beim Schreiben in die AutoHotkey-Datei: {e}")
        # Der Fehler führt nicht zum Abbruch des Programms



def get_subnet(interface='ens18'):
    ip_info = ni.ifaddresses(interface)
    ip = ip_info[ni.AF_INET][0]['addr']
    netmask = ip_info[ni.AF_INET][0]['netmask']

    # Berechnet das Subnetz
    ip_parts = list(map(int, ip.split('.')))
    netmask_parts = list(map(int, netmask.split('.')))
    subnet_parts = [str(ip_parts[i] & netmask_parts[i]) for i in range(4)]
    subnet = '.'.join(subnet_parts)

    return subnet


if __name__ == "__main__":
    subnet = get_subnet()
    print(f"Subnetz des Clients: {subnet}")
    server_ip, server_port = find_server(subnet)
    if server_ip and server_port:
        while True:
            client_socket = connect_to_server(server_ip, server_port)
            receive_data_from_server(client_socket)
            time.sleep(5)  # Wartezeit vor dem erneuten Verbindungsversuch
    else:
        print("Server nicht gefunden.")


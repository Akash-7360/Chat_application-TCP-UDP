# ==================================
# UDP SERVER BACKEND (for GUI)
# File: server_udp_backend.py
# ==================================

import socket
import threading


class UDPServerBackend:
    def __init__(self, gui_callback):
        """
        gui_callback: function to update GUI with new messages
        """
        self.gui_callback = gui_callback
        self.server_socket = None
        self.client_addr = None
        self.running = False

    def start_server(self, host="localhost", port=6060):
        """Start UDP server"""
        self.running = True

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.bind((host, port))

            self.gui_callback(f"[UDP] Server started on {host}:{port}\nWaiting for client...\n")

            threading.Thread(target=self.receive_messages, daemon=True).start()

        except Exception as e:
            self.gui_callback(f"[ERROR] Could not start UDP server: {e}\n")

    def receive_messages(self):
        """Receive messages + store client address"""
        while self.running:
            try:
                data, addr = self.server_socket.recvfrom(1024)

                if self.client_addr is None:
                    self.client_addr = addr
                    self.gui_callback(f"[UDP] Client connected: {addr}\n")

                msg = data.decode()
                self.gui_callback(f"Client: {msg}\n")

            except Exception:
                break

        self.gui_callback("[UDP] Server stopped receiving.\n")

    def send_message(self, message):
        """Send message to client (UDP needs client_addr first)"""
        if self.client_addr:
            try:
                self.server_socket.sendto(message.encode(), self.client_addr)
            except:
                self.gui_callback("[ERROR] Failed to send message.\n")
        else:
            self.gui_callback("[!] No client yet. Client must send a message first.\n")

    def stop_server(self):
        self.running = False
        try:
            if self.server_socket:
                self.server_socket.close()
        except:
            pass

        self.gui_callback("[UDP] Server stopped.\n")

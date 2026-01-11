# ================================
# TCP SERVER BACKEND (for GUI)
# File: server_tcp_backend.py
# ================================

import socket
import threading


class TCPServerBackend:
    def __init__(self, gui_callback):
        """
        gui_callback: function to update the GUI with new messages
        """
        self.gui_callback = gui_callback
        self.server_socket = None
        self.client_socket = None
        self.running = False

    def start_server(self, host="localhost", port=5050):
        """Start the TCP server"""
        self.running = True

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((host, port))
            self.server_socket.listen(1)
            self.gui_callback(f"[TCP] Server started on {host}:{port}\nWaiting for client...\n")

            threading.Thread(target=self.accept_connection, daemon=True).start()

        except Exception as e:
            self.gui_callback(f"[ERROR] Could not start TCP server: {e}\n")

    def accept_connection(self):
        """Wait for client to connect"""
        try:
            self.client_socket, addr = self.server_socket.accept()
            self.gui_callback(f"[TCP] Client connected: {addr}\n")

            threading.Thread(target=self.receive_messages, daemon=True).start()

        except Exception as e:
            self.gui_callback(f"[ERROR] Accept failed: {e}\n")

    def receive_messages(self):
        """Receive messages from client"""
        while self.running:
            try:
                msg = self.client_socket.recv(1024).decode()
                if not msg:
                    break
                self.gui_callback(f"Client: {msg}\n")
            except:
                break

        self.gui_callback("[TCP] Client disconnected.\n")

    def send_message(self, message):
        """Send message to connected client"""
        if self.client_socket:
            try:
                self.client_socket.send(message.encode())
            except:
                self.gui_callback("[ERROR] Failed to send message.\n")

    def stop_server(self):
        """Stop the server and close sockets"""
        self.running = False

        try:
            if self.client_socket:
                self.client_socket.close()
            if self.server_socket:
                self.server_socket.close()
        except:
            pass
        
        self.gui_callback("[TCP] Server stopped.\n")


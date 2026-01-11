# =============================
# CLIENT GUI (TCP + UDP)
# File: client_gui.py
# =============================

import tkinter as tk
from tkinter import ttk
import socket
import threading


class ClientGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Client Chat (TCP/UDP)")
        self.window.geometry("500x600")

        # chatbox
        self.chat_box = tk.Text(self.window, height=25, width=60, state="disabled")
        self.chat_box.pack(pady=10)

        # protocol
        tk.Label(self.window, text="Select Protocol:").pack()
        self.protocol = ttk.Combobox(self.window, values=["TCP", "UDP"], state="readonly")
        self.protocol.current(0)
        self.protocol.pack(pady=5)

        # connect button
        self.connect_btn = tk.Button(self.window, text="Connect", command=self.connect)
        self.connect_btn.pack(pady=5)

        # disconnect button
        self.disconnect_btn = tk.Button(self.window, text="Disconnect", command=self.disconnect)
        self.disconnect_btn.pack(pady=5)

        # Message input  
        tk.Label(self.window, text="Type your message below:").pack()

        self.input_frame = tk.Frame(self.window, bd=2, relief="groove")
        self.input_frame.pack(pady=5, fill="x")

        self.msg_entry = tk.Entry(self.input_frame, width=40)
        self.msg_entry.insert(0, "Enter your message...")
        self.msg_entry.pack(side="left", padx=5, pady=5)

        self.send_btn = tk.Button(self.input_frame, text="Send", bg="lightblue", command=self.send_message)
        self.send_btn.pack(side="right", padx=5)

        # connection vars
        self.tcp_socket = None
        self.udp_socket = None
        self.running = False

    def update_chat(self, msg):
        self.chat_box.config(state="normal")
        self.chat_box.insert("end", msg)
        self.chat_box.see("end")
        self.chat_box.config(state="disabled")

    def connect(self):
        proto = self.protocol.get()

        if proto == "TCP":
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.connect(("localhost", 5050))
            self.update_chat("[TCP] Connected to server.\n")

            self.running = True
            threading.Thread(target=self.receive_tcp, daemon=True).start()

        else:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.update_chat("[UDP] Ready. Send first message to create connection.\n")

            self.running = True
            threading.Thread(target=self.receive_udp, daemon=True).start()

    def send_message(self):
        msg = self.msg_entry.get()
        if not msg.strip():
            return

        proto = self.protocol.get()

        self.update_chat(f"You: {msg}\n")

        if proto == "TCP" and self.tcp_socket:
            self.tcp_socket.send(msg.encode())

        elif proto == "UDP" and self.udp_socket:
            self.udp_socket.sendto(msg.encode(), ("localhost", 6060))

        self.msg_entry.delete(0, "end")

    def receive_tcp(self):
        while self.running:
            try:
                data = self.tcp_socket.recv(1024).decode()
                if not data:
                    break
                self.update_chat(f"Server: {data}\n")
            except:
                break

    def receive_udp(self):
        while self.running:
            try:
                data, _ = self.udp_socket.recvfrom(1024)
                self.update_chat(f"Server: {data.decode()}\n")
            except:
                break

    def disconnect(self):
        self.running = False

        if self.tcp_socket:
            self.tcp_socket.close()
        if self.udp_socket:
            self.udp_socket.close()

        self.update_chat("[INFO] Disconnected.\n")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    ClientGUI().run()

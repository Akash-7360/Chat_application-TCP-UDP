# ============================
# SERVER GUI (TCP + UDP)
# File: server_gui.py
# ============================

import tkinter as tk
from tkinter import ttk
import threading

from server_tcp_backend import TCPServerBackend
from server_udp_backend import UDPServerBackend


class ServerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Server Chat (TCP/UDP)")
        self.window.geometry("500x600")

        # Message display
        self.chat_box = tk.Text(selfg.window, height=25, width=60, state="disabled")
        self.chat_box.pack(pady=10)

        # Protocol selection
        tk.Label(self.window, text="Select Protocol:").pack()
        self.protocol = ttk.Combobox(self.window, values=["TCP", "UDP"], state="readonly")
        self.protocol.current(0)
        self.protocol.pack(pady=5)

        # Buttons
        self.start_btn = tk.Button(self.window, text="Start Server", command=self.start_server)
        self.start_btn.pack(pady=5)

        self.stop_btn = tk.Button(self.window, text="Stop Server", command=self.stop_server)
        self.stop_btn.pack(pady=5)

        # Message area
        tk.Label(self.window, text="Type your message below:").pack()

        self.input_frame = tk.Frame(self.window, bd=2, relief="groove")
        self.input_frame.pack(pady=5, fill="x")

        self.msg_entry = tk.Entry(self.input_frame, width=40)
        self.msg_entry.insert(0, "Enter your message...")
        self.msg_entry.pack(side="left", padx=5, pady=5)

        self.send_btn = tk.Button(self.input_frame, text="Send", bg="lightblue", command=self.send_message)
        self.send_btn.pack(side="right", padx=5)

        # backend refs
        self.tcp_server = None
        self.udp_server = None

    def update_chat(self, message):
        self.chat_box.config(state="normal")
        self.chat_box.insert("end", message)
        self.chat_box.see("end")
        self.chat_box.config(state="disabled")

    def start_server(self):
        proto = self.protocol.get()

        if proto == "TCP":
            self.tcp_server = TCPServerBackend(self.update_chat)
            threading.Thread(target=self.tcp_server.start_server, daemon=True).start()

        else:
            self.udp_server = UDPServerBackend(self.update_chat)
            threading.Thread(target=self.udp_server.start_server, daemon=True).start()

        self.update_chat(f"[INFO] {proto} Server Started.\n")

    def send_message(self):
        message = self.msg_entry.get()
        if not message.strip():
            return

        proto = self.protocol.get()

        self.update_chat(f"Server: {message}\n")

        if proto == "TCP" and self.tcp_server:
            self.tcp_server.send_message(message)

        elif proto == "UDP" and self.udp_server:
            self.udp_server.send_message(message)

        self.msg_entry.delete(0, "end")

    def stop_server(self):
        proto = self.protocol.get()

        if proto == "TCP" and self.tcp_server:
            self.tcp_server.stop_server()

        elif proto == "UDP" and self.udp_server:
            self.udp_server.stop_server()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    ServerGUI().run()

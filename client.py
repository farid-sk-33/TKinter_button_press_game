import tkinter as tk
import socket
import threading
import time

def send_message():
    if client_socket:
        message = "Button pressed!"
        client_socket.send(message.encode())  # Send to host
        press_button_client.pack_forget()  # Hide the button after clicking
        response_label_client.config(text="Congratulations! You've won the game!", fg="green")  # Update client label
        send_message_to_server(message)  # Send to host
        
def send_message_to_server(message):
    if server_socket:
        server_socket.send(message.encode())

def handle_server_messages():
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            client_socket.close()
            print("Disconnected from the server")
            break
        if data == "Button pressed!":
            response_label_client.config(text="Oops! You've lost the game.", fg="red")
            press_button_client.pack_forget()
        elif data == "Game started!":
            countdown_on_client()

def countdown_on_client():
    press_button_client.config(state=tk.DISABLED)  # Disable the button during countdown
    for i in range(3, -1, -1):  # Include 0 in the countdown
        countdown_label_client.config(text=f"Time left: {i}")
        client_root.update()
        time.sleep(1)
    countdown_label_client.config(text="Press the 'Press Button' quickly!")
    press_button_client.config(state=tk.NORMAL)  # Enable the button after countdown

# Client configuration
host = '192.168.1.101'  # Host IP
port = 12345       # Port to connect to

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((host, port))
    print("Connected to the server")

    # Create the client window
    client_root = tk.Tk()
    client_root.title("Client Button")

    # Create the buttons and labels for the client
    press_button_client = tk.Button(client_root, text="Press Button", command=send_message, state=tk.DISABLED)
    countdown_label_client = tk.Label(client_root, text="", font=("Helvetica", 16))
    response_label_client = tk.Label(client_root, text="", font=("Helvetica", 16))

    # Pack the buttons and labels for the client
    press_button_client.pack()
    countdown_label_client.pack(pady=10)
    response_label_client.pack(pady=10)

    # Start the thread to handle server messages
    server_thread = threading.Thread(target=handle_server_messages)
    server_thread.start()

    # Start the main event loop for the client
    client_root.mainloop()

finally:
    # Close the client socket
    client_socket.close()
    print("Disconnected from the server")
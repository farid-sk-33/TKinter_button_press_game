import tkinter as tk
import threading
import socket
import time
# Global variables
client_connected = False
client_socket = None
game_started = False
def start_game():
    global client_connected, game_started
    if client_connected:
        send_message_to_client(&quot;Game started!&quot;)
        game_started = True
        countdown(3)  # Start countdown from 3
def press_button_action():
    press_button.config(state=tk.DISABLED)  # Disable the &quot;Press Button&quot; button
    response_label.config(text=&quot;Congratulations! You&#39;ve won the game!&quot;, fg=&quot;green&quot;)
    send_message_to_client(&quot;Button pressed!&quot;)
    press_button.pack_forget()
    start_button.pack_forget()
def countdown(seconds):
    for i in range(seconds, -1, -1):  # Include 0 in the countdown
        countdown_label.config(text=f&quot;Time left: {i}&quot;)
        root.update()
        time.sleep(1)
    countdown_label.config(text=&quot;Press the &#39;Press Button&#39; quickly!&quot;)
    press_button.config(state=tk.NORMAL)  # Enable the &quot;Press Button&quot; button
def send_message_to_client(message):
    global client_socket
    client_socket.send(message.encode())
def server_thread():
    global client_socket, client_connected
    # Server configuration
    host = &#39;0.0.0.0&#39;  # Your host IP
    port = 12345       # Port to listen on
    # Create a socket

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the host and port
    server_socket.bind((host, port))
    # Listen for incoming connections
    server_socket.listen()
    print(&quot;Server is listening for incoming connections...&quot;)
    while True:
        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()
        print(f&quot;Connection established with {client_address}&quot;)
        client_connected = True
        game_started_on_client()

        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                client_connected = False
                client_socket.close()
                print(&quot;Client disconnected&quot;)
                break
            if data == &quot;Button pressed!&quot;:
                response_label.config(text=&quot;Oops! You&#39;ve lost the game.&quot;, fg=&quot;red&quot;)
                press_button.pack_forget()
                start_button.pack_forget()
            elif data == &quot;Game started!&quot;:
                game_started_on_client()
# Start the server thread
server_thread = threading.Thread(target=server_thread)
server_thread.start()
def game_started_on_client():
    global game_started
    if not game_started:
        start_button.config(state=tk.NORMAL)
# Create the main window
root = tk.Tk()
root.title(&quot;Button &amp; Timer Example&quot;)
# Create the buttons
start_button = tk.Button(root, text=&quot;Start Game&quot;, command=start_game,
state=tk.NORMAL)  # Make it initially enabled

press_button = tk.Button(root, text=&quot;Press Button&quot;, command=press_button_action,
state=tk.DISABLED)
# Create labels
countdown_label = tk.Label(root, text=&quot;&quot;, font=(&quot;Helvetica&quot;, 16))
response_label = tk.Label(root, text=&quot;&quot;, font=(&quot;Helvetica&quot;, 16))
# Pack the buttons and labels into the window
start_button.pack(pady=10)
press_button.pack()
countdown_label.pack(pady=10)
response_label.pack(pady=10)

# Start the main event loop
root.mainloop()

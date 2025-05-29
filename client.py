import socket
import threading
HOST = '127.0.0.1'  # Localhost (same machine)
PORT = 8433

def receive_messages(client_socket):
    """Receive messages from server"""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\r{message}\nYou: ", end="")
        except:
            break

def main():
    # Create client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((HOST, PORT))
    except:
        print("Could not connect to server")
        return
    
    # Start thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()
    
    print("Connected to server. Type your messages (type 'quit' to exit):")
    
    while True:
        message = input("You: ")
        
        if message.lower() == 'quit':
            break
            
        try:
            client.send(message.encode('utf-8'))
        except:
            break
    
    client.close()
    
main()
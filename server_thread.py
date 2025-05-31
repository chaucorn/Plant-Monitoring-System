import socket
import threading
import time
import json

HOST = '0.0.0.0'
PORT = 8433
#esp32_addr = ''
#client_addr = ''


# List to store client connections
clients = []
clients_addr = []

def handle_client(client_socket, addr):
    """Handle individual client connection"""
    print(f"New connection from {addr}")
    
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024)
            if not message:
                break
            
            print(f"Received data: {message}")
            decoded_message = message.decode('utf-8')
            decoded_message = json.loads(decoded_message)
            if decoded_message["type"] ==  0:
                clients_addr[0] = addr
                print("Received message from ESP32")
            elif decoded_message["type"] == 1:
                clients_addr[1] = addr
                print("Received message from client.py")    
            print(f"Message from {addr}: {message}")
            
            # Broadcast message to all other clients
            broadcast(message, client_socket)
            
        except:
            break
    
    # Remove client and close connection
    clients.remove(client_socket)
    client_socket.close()
    print(f"Connection closed from {addr}")

def broadcast(message, sender_socket):
    """Send message to all clients except sender"""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)
                client.close()

def main():
    # Create server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    
    print(f"Server running on {HOST}:{PORT}")
    
    while True:
        # Accept new client connections
        client_socket, addr = server.accept()
        clients.append(client_socket)
        
        # Start new thread to handle client
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()


def handle_client2(conn, addr, clients):
    print(f"Connected by {addr}")
    clients.append(conn)
    esp32_addr = ''
    client_addr = ''
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            header = data[0]
            signal = data[1]
            print(f"Received data: {data}")
            if header == 0:
                print("Received message from ESP32")
                esp32_addr = addr
                if signal == 1:
                    print("Received 1 from ESP32")
                    conn.sendall("message from esp32", client_addr)

            elif header == 1:
                print("Received message from client.py")
                client_addr = addr
                if signal == 1:
                    print("Received 1 from client.py")
                    conn.sendall("message from client.py", esp32_addr)
            # Broadcast message to all other clients
            #for client in clients:
            #    if client != conn:
            #        try:
            #            client.sendall(data)
            #        except:
            #            clients.remove(client)
            #print(f"Received from {addr}: {data.decode()}")
    except:
        pass
    finally:
        clients.remove(conn)
        conn.close()
        print(f"Disconnected: {addr}")

if __name__ == "__main__":
    main()
import socket
import time

HOST = '0.0.0.0'  # Accept all incoming connections
PORT = 8433

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(2)
    print(f"Server listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        try:
            while True:
                print("Running...")
                time.sleep(2)
                data = conn.recv(1024)
                if not data:
                    break
                #msg_client = data.decode()
                header = data[0]
                signal = data[1]
                print(f"Received data: {data}")
                if header == 0:
                    print("Received message from ESP32")
                    if signal == 1:
                        print("Received 1 from ESP32")
                        conn.sendall(b"0")

                elif header == 1:
                    print("Received message from client.py")
                    if signal == 1:
                        print("Received 1 from client.py")
                        conn.sendall(b"1")
                
                #conn.sendall(b"ACK from PC")
        except KeyboardInterrupt:
            print("Program interrupted by user.")
        finally:
            print("Exiting program.")
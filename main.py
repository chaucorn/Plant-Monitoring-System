import network
import socket
import time

# ==== Wi-Fi Credentials ====
SSID = 'LAPTOP-Chau'
PASSWORD = 'baochau111'

# ==== Server Info ====
SERVER_IP = '192.168.137.1'  # Your PC's IP running the C server
SERVER_PORT = 8433
# === 2. Connect to Wi-Fi ===
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

if not sta_if.isconnected():
    print("Connecting to WiFi...")
    sta_if.connect(SSID, PASSWORD)
    retry = 0
    while not sta_if.isconnected() and retry < 10:
        time.sleep(1)
        retry += 1

if sta_if.isconnected():
    print("✅ Connected:", sta_if.ifconfig())
else:
    print("❌ Failed to connect to WiFi")
    raise SystemExit()

# === 3. Connect to PC socket server ===
HOST = '192.168.137.1'  # Your PC IP in hotspot network
PORT = 8433

try:
    s = socket.socket()
    print(f"Connecting to {HOST}:{PORT}...")
    s.connect((HOST, PORT))
    print("✅ Connected to server")

    # Send and receive data
    signal = 1
    header = 0
    message = bytes([header, signal])
    s.send(message)
    print("ESP32 sent message successfully")
    data = s.recv(1024)
    msg = data[1]
    print("📩 Received:", data)
    print(data[1])
    if msg == 0:
        print("closed")
    elif msg == 1:
        print("opened")
    else:
        print("unknown")
    #print("📩 Received:", data.decode())

    #s.close()

except Exception as e:
    print("❌ Socket error:", e)
except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    print("Exiting program.")

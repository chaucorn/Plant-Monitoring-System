import network
import socket
import time
import _thread
import json
import uasyncio as asyncio


async def read(lock,sock):
    """Thread to continuously receive messages from the server"""
    while True:
        try:
            
            data = await sock.recv(1024)
            if not data:
                print("❌ Disconnected from server.")
                break
            msg = data[1]
            print("📩 Received:", data)
            if msg == 0:
                print("closed")
            elif msg == 1:
                print("opened")
            else:
                print("unknown")
            await asyncio.sleep(1)
        except Exception as e:
            print("❌ Receive error:", e)
            break

async def send(lock,sock):
    while True:
        
        try:
            async with lock:
                
                t = time.localtime()
                message = {
                    "type" : "0",
                    "current_time" : f"{t[0]}{t[1]}{t[2]}{t[3]}{t[4]}{t[5]}"
                    
                    }
                # Send and receive data
                mess = json.dumps(message)
                #message = "hello"
                await sock.send(mess)
                
                await asyncio.sleep(1)
                print("ESP32 sent message successfully")
        except Exception as e:
            print("❌ send error:", e)
            break
# ==== Wi-Fi Credentials ====
SSID = 'LAPTOP-Chau'
PASSWORD = 'baochau111'

# ==== Server Info ====
HOST = '192.168.137.1'  # Your PC's IP running the C server
PORT = 8433
async def main():

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

    try:
        s = socket.socket()
        print(f"Connecting to {HOST}:{PORT}...")
        s.connect((HOST, PORT))
        print("✅ Connected to server")
        lock = asyncio.Lock()
        await asyncio.gather(send(lock,s), read(lock, s))

        
        
        #print("📩 Received:", data.decode())

        #s.close()

    except Exception as e:
        print("❌ Socket error:", e)
    except KeyboardInterrupt:
        print("Program interrupted by user.")

asyncio.run(main())


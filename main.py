import time
from libs.WebSocketClient import WebSocket

ws = WebSocket("192.168.0.23", 5050, "/websocket")
ws.connect()

while True:
    ws.send("Hello, WebSocket!")
    try:
        response = ws.receive()
        print(f"Received response: {response}")
    except Exception as e:
        print(f"Error receiving response: {e}")
    time.sleep(1)  # Espera 1 segundo antes de enviar el siguiente mensaje

ws.close()
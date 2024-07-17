# 🌐 MicroPython WebSocket Client

Este es un cliente WebSocket escrito en MicroPython, diseñado para funcionar en placas ESP32. La librería permite a los desarrolladores crear aplicaciones que se comuniquen con servidores WebSocket utilizando el protocolo WebSocket.

## ✨ Características

- 🔗 Conexión WebSocket a servidores
- 📤 Envío y recepción de datos WebSocket
- 🔄 Manejo de la desconexión
- 🤖 Compatible con MicroPython y ESP32

## 📋 Requisitos

- 🐍 MicroPython 1.19 o superior
- 🔌 Placa ESP32

## 📦 Instalación

1. Clona o descarga el repositorio de la librería.
2. Copia el archivo `WebSocketClient.py` a tu proyecto MicroPython.

## 🚀 Uso

Aquí tienes un ejemplo básico de cómo utilizar la librería:

```python
from WebSocketClient import WebSocket
import time

ws = WebSocket("192.168.0.23", 5050, "/websocket")
ws.connect()

while True:
    ws.send("Hello, WebSocket!")
    try:
        response = ws.receive()
        print(f"Received response: {response}")
    except Exception as e:
        print(f"Error receiving response: {e}")
    time.sleep(1)

ws.close()
```
En este ejemplo, se crea una instancia de la clase WebSocket con la dirección IP, el puerto y la ruta del servidor WebSocket. Luego, se establece la conexión y se entra en un bucle que envía un mensaje cada segundo y recibe la respuesta del servidor.

📖 Documentación
La librería proporciona las siguientes funciones:

connect(): Establece la conexión WebSocket con el servidor.
send(data): Envía un mensaje WebSocket al servidor.
receive(): Recibe un mensaje WebSocket del servidor.
close(): Cierra la conexión WebSocket.
Para más detalles y ejemplos, consulta el código fuente de la librería.

🤝 Contribución
Si encuentras algún problema o tienes sugerencias de mejora, no dudes en abrir un issue o enviar un pull request en el repositorio de GitHub.

📄 Licencia
Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo LICENSE para más información.

¡Espero que esto te sea útil para tu proyecto en GitHub!

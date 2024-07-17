import usocket as socket
import ustruct as struct
import urandom as random
import ubinascii

class WebSocket:
    def __init__(self, host, port, path):
        self.host = host
        self.port = port
        self.path = path
        self.sock = None
        self.connected = False

    def connect(self):
        addr = socket.getaddrinfo(self.host, self.port)[0][-1]
        self.sock = socket.socket()
        self.sock.settimeout(5)  # Espera 5 segundos antes de lanzar un error de tiempo de espera
        self.sock.connect(addr)

        key = ubinascii.b2a_base64(bytes([random.getrandbits(8) for _ in range(16)])).decode().strip()
        print(f"Sec-WebSocket-Key: {key}")

        request = b"GET %s HTTP/1.1\r\n" % self.path.encode()
        request += b"Host: %s:%d\r\n" % (self.host.encode(), self.port)
        request += b"Upgrade: websocket\r\n"
        request += b"Connection: Upgrade\r\n"
        request += b"Sec-WebSocket-Key: %s\r\n" % key.encode()
        request += b"Sec-WebSocket-Version: 13\r\n\r\n"

        print(request)  # Imprime la solicitud HTTP para depuración
        self.sock.send(request)
        response = self.sock.recv(1024)
        print(f"Response:\n{response}")

        if b"HTTP/1.1 101" not in response:
            print("WebSocket handshake failed")
            print(response)
            raise Exception("WebSocket handshake failed")

        self.connected = True

    def send(self, data):
        if not self.connected:
            raise Exception("WebSocket not connected")

        if isinstance(data, str):
            data = data.encode()

        mask_key = bytes([random.getrandbits(8) for _ in range(4)])
        masked_data = bytearray(len(data))
        for i in range(len(data)):
            masked_data[i] = data[i] ^ mask_key[i % 4]

        header = b"\x81"
        length = len(masked_data)
        if length < 126:
            header += struct.pack("B", length | 0x80)
        elif length < 65536:
            header += struct.pack("!BH", 126 | 0x80, length)
        else:
            header += struct.pack("!BQ", 127 | 0x80, length)
        header += mask_key

        self.sock.send(header + masked_data)

    def receive(self):
        if not self.connected:
            raise Exception("WebSocket not connected")

        header = self.sock.recv(2)
        header_data = memoryview(header)
        is_final_frame = (header_data[0] >> 7) & 0x1
        reserved = (header_data[0] >> 4) & 0x7
        opcode = header_data[0] & 0xF
        mask = (header_data[1] >> 7) & 0x1
        payload_length = header_data[1] & 0x7F

        if payload_length == 126:
            payload_length = ustruct.unpack_from("!H", header, 2)[0]
        elif payload_length == 127:
            payload_length = ustruct.unpack_from("!Q", header, 2)[0]

        mask_key = self.sock.recv(4) if mask else None
        payload = self.sock.recv(payload_length)
        if mask:
            payload = bytes(p ^ mask_key[i % 4] for i, p in enumerate(payload))

        try:
            return payload.decode()
        except UnicodeError:
            print(f"UnicodeError: Unable to decode payload: {payload}")
            return payload.hex()

    def close(self):
        if self.connected:
            self.sock.close()
            self.connected = False
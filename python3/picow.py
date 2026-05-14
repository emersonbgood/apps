import socket

# '0.0.0.0' listens on all available network interfaces
UDP_IP = "0.0.0.0"
UDP_PORT = 9000

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for data on port {UDP_PORT}...")
print("Waiting for Pico W to send a message...")

while True:
    # Receive up to 1024 bytes
    data, addr = sock.recvfrom(1024)
    
    # Decode and print the message
    message = data.decode('utf-8')
    print(f"Received from {addr}: {message}")

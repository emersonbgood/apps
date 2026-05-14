import serial
import time

# Opens the Bluetooth tunnel we built
try:
    ser = serial.Serial('/dev/rfcomm0', 9600, timeout=1)
    print("--- Connected to Pico 2 ---")
    print("Commands: 'on', 'off', or 'exit'")

    while True:
        cmd = input("Command: ").lower().strip()
        if cmd == "exit":
            break
        ser.write(f"{cmd}\n".encode())
        
except Exception as e:
    print(f"Error: {e}")
    print("Make sure 'sudo rfcomm bind 0 00:22:03:01:0F:83' was run!")

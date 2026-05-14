from machine import Pin, SPI, UART
from mfrc522 import MFRC522
import utime
led = Pin(25, Pin.OUT)
# Setup Bluetooth (GP0/GP1)
bt = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Setup SPI (GP2/GP3/GP4)
spi = SPI(0, baudrate=1000000, sck=Pin(2), mosi=Pin(3), miso=Pin(4))

# Initialize Reader (CS=GP5, RST=GP22)
reader = MFRC522(spi, 5, 22)

print("System Active - Scan Card")
bt.write("System Ready. Scan card now...\n")

while True:
    stat, tag_type = reader.request(reader.REQIDL)
    if stat == reader.OK:
        stat, uid = reader.SelectTagSN()
        if stat == reader.OK:
            # Format the UID properly
            card_id = "0x" + "".join(["%02X" % i for i in uid])
            msg = f"key card detected with data: {card_id}\n"
            led.value(1)
            print(msg.strip())
            bt.write(msg)
            utime.sleep(2)
            led.value(0)
    utime.sleep_ms(100) # Small delay to save CPU


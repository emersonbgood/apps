from machine import Pin, PWM
import utime
a=0
servo = PWM(Pin(15))
servo.freq(50)
def set_angle(angle):
    duty = int((angle / 180) * 6553 + 1638)
    servo.duty_u16(duty)
while True:
    set_angle(a)
    a=a+4
# pin 20 (GPIO14) for servo input, use 5V
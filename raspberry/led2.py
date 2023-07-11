from gpiozero import LED
from time import sleep
from config import LED_PIN, DELAY_LED

led = LED(LED_PIN)

while True:
    led.on()
    sleep(DELAY_LED)
    led.off()
    sleep(DELAY_LED)
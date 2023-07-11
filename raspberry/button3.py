from gpiozero import Button, LED
from config import BUTTON_PIN, LED_PIN

# button = Button(BUTTON_PIN)

# button.wait_for_press()
# print('You pushed me')

# from gpiozero import LED, Button
from signal import pause

led = LED(LED_PIN)
button = Button(BUTTON_PIN)

button.when_pressed = led.on
button.when_released = led.off

pause()
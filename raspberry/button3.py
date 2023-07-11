from gpiozero import Button
from config import BUTTON_PIN

button = Button(BUTTON_PIN)

button.wait_for_press()
print('You pushed me')
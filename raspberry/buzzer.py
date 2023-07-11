from gpiozero import Buzzer
from time import sleep
from config import BUZZER_PIN

buzzer = Buzzer(BUZZER_PIN)

while True:
    buzzer.beep()
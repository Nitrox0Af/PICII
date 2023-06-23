import RPi.GPIO as GPIO
import time

# Define os pinos TRIG e ECHO
TRIG_PIN = 12
ECHO_PIN = 16

# Configuração dos pinos GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def measure_distance():
    # Envia um pulso curto no pino TRIG
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)
    
    # Espera até que o pino ECHO esteja em nível alto
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()
    
    # Espera até que o pino ECHO volte para o nível baixo
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()
    
    # Calcula a duração do pulso do ECHO
    pulse_duration = pulse_end - pulse_start
    
    # Calcula a distância com base na velocidade do som (343m/s) e na duração do pulso
    distance = pulse_duration * 34300 / 2
    
    return distance

try:
    while True:
        dist = measure_distance()
        print("Distancia: {:.2f} cm".format(dist))
        time.sleep(1)
        
except KeyboardInterrupt:
    GPIO.cleanup()

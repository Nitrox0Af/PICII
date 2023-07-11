import RPi.GPIO as GPIO
import time

row_list = [26, 20, 19, 16]
col_list = [6, 13, 5]

GPIO.setmode(GPIO.BCM)

for x in range(0, 4):
    GPIO.setup(row_list[x], GPIO.OUT)
    GPIO.output(row_list[x], GPIO.HIGH)

for x in range(0, 3):
    GPIO.setup(col_list[x], GPIO.IN, pull_up_down=GPIO.PUD_UP)

key_list = [["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
            ["*", "0", "#"]]

def keypad(col, row):
    for r in row:
        GPIO.output(r, GPIO.LOW)
        result = [GPIO.input(col[0]), GPIO.input(col[1]), GPIO.input(col[2])]
        if min(result) == 0:
            key = key_list[int(row.index(r))][int(result.index(0))]
            GPIO.output(r, GPIO.HIGH)
            return key
        GPIO.output(r, GPIO.HIGH)

def main():
    try:
        while True:
            key = keypad(col_list, row_list)
            if key is not None:
                print("Key: " + key)
                return key
    except KeyboardInterrupt:
        GPIO.cleanup()

main()
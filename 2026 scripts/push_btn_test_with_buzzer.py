import RPi.GPIO as GPIO
from time import sleep

PUSH_BUTTON = 20
BUZZER_PIN = 16


def setup_gpio() -> None:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.setup(PUSH_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.cleanup()
setup_gpio()


notes = {
    "E7": 2637, "C7": 2093, "G7": 3136,
    "G6": 1568, "E6": 1319, "A6": 1760,
    "B6": 1976, "AS6": 1865, "A6": 1760,
    "G6": 1568
}

melody = [
    ("E7", 0.15), ("E7", 0.15), (None, 0.15),
    ("E7", 0.15), (None, 0.15),
    ("C7", 0.15), ("E7", 0.15), (None, 0.15),
    ("G7", 0.3), (None, 0.3),
    ("G6", 0.3)
]


def play_super_mario():
    for note, dur in melody:
        if note:
            pwm.ChangeFrequency(notes[note])
            pwm.ChangeDutyCycle(50)
        else:
            pwm.ChangeDutyCycle(0)
        sleep(dur)

try:
    while True:
        if(GPIO.input(PUSH_BUTTON) == 0):
            sleep(1)
            print("Start taking photos")
            pwm = GPIO.PWM(BUZZER_PIN, 440)
            pwm.start(0)
            play_super_mario()
            pwm.stop()
finally:
    GPIO.cleanup()

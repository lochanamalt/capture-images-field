"""
@author: Lochana Marasinghe
@date: 5/27/2026
@description: 
"""
import RPi.GPIO as GPIO
from time import sleep


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

class BUZZER:
    def __init__(self,
                 buzzer_pin):
        self.buzzer_pin = buzzer_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(buzzer_pin, GPIO.OUT)


    def play_super_mario(self):
        pwm = GPIO.PWM(self.buzzer_pin, 440)
        pwm.start(0)

        for note, dur in melody:
            if note:
                pwm.ChangeFrequency(notes[note])
                pwm.ChangeDutyCycle(50)
            else:
                pwm.ChangeDutyCycle(0)
            sleep(dur)

        pwm.stop()
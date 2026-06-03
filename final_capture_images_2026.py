"""
@author: Lochana Marasinghe
@date: 5/27/2026
@description: 
"""
from threading import Thread, Event
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO
import picamera

from buzzer import BUZZER
from lepton_thermal import LeptonThermalCamera

pi_camera_folder = '/home/pi/Documents/2026/pi_camera/'
thermal_img_folder = '2026/thermal_images'
cam_name = 'pi17_iso100'

# Photo session settings
total_photos = 3  # Total number of images to be taken
delay = 1  # Time interval between each photo (in seconds)

PUSH_BUTTON = 20
BUZZER_PIN = 16
LED_PIN = 21

def setup_gpio() -> None:
    print("Setting up GPIO")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(PUSH_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

setup_gpio()
buzzer = BUZZER(buzzer_pin=BUZZER_PIN)


def blink_worker(stop_flag):
    while True:
        stop_flag.wait()

        while stop_flag.is_set():
            GPIO.output(LED_PIN, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(LED_PIN, GPIO.LOW)
            sleep(0.5)

def destroy():
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()

def config_camera(cam):
    cam.sensor_mode = 2
    cam.resolution = (3280, 2464)

    cam.hflip = True
    cam.vflip = True
    sleep(1)
    cam.iso = 100
    sleep(2)
#     cam.shutter_speed = cam.exposure_speed
#     cam.exposure_mode ='off'
#     g = cam.awb_gains
#     print("Camera awb gains:" + str(g))
#     cam.awb_mode = "off"
#     cam.awb_gains = g
#     sleep(2)

blink_event = Event()
blink_thread = Thread(target=blink_worker, args=(blink_event,), daemon=True)
blink_thread.start()

try:
    while True:
        if(GPIO.input(PUSH_BUTTON) == 0):
            blink_event.set()
            sleep(1)

            t1 = datetime.now()
            print('Starting capturing at ' + 'date_' + str(t1.day) + '-' + str(t1.month) + '-' + str(t1.year) + '_' + str(
                t1.hour) + '.' + str(t1.minute) + '.' + str(t1.second))

            ##---------------------------------------Capturing RGB-NIR Images ----------------------------------------------------##
            for counter in range(total_photos):
                t2 = datetime.now()
                # NoIR
                with picamera.PiCamera(camera_num=0) as cam0:
                    config_camera(cam0)
                    filename = pi_camera_folder + cam_name + '_NoIR_date_' + str(t2.day) + '-' + str(t2.month) + '-' + str(
                        t2.year) + '_' + str(
                        t2.hour) + '.' + str(t2.minute) + '.' + str(t2.second) + '_' + str(counter + 1) + '.png'

                    print(' [' + str(counter + 1) + ' of ' + str(total_photos) + '] ' + filename)

                    #         cam0.capture(filename, bayer=True, use_video_port=False)
                    cam0.capture(filename, use_video_port=False)

                # Now switch to the other camera (RGB)
                with picamera.PiCamera(camera_num=1) as cam1:
                    config_camera(cam1)
                    filename = pi_camera_folder + cam_name + '_RGB_date_' + str(t2.day) + '-' + str(t2.month) + '-' + str(
                        t2.year) + '_' + str(
                        t2.hour) + '.' + str(t2.minute) + '.' + str(t2.second) + '_' + str(counter + 1) + '.png'

                    print(' [' + str(counter + 1) + ' of ' + str(total_photos) + '] ' + filename)
                    # cam1.capture(filename, bayer=True, use_video_port=False)
                    cam1.capture(filename, use_video_port=False)

                #     with picamera.PiCamera(stereo_mode='side-by-side') as camera:
                #         filename = pi_camera_folder + cam_name + '_side_by_side_date_' + str(t2.day) + '-' + str(t2.month) + '-' + str(t2.year) + '_' + str(
                #                 t2.hour) + '.' + str(t2.minute) + '.' + str(t2.second) + '_' + str(counter+1) + '.png'
                #         camera.resolution = (3280, 1232)
                # #         camera.framerate = 20
                #         camera.hflip = True
                #         camera.vflip = True
                #         sleep(2)
                #         camera.iso = 100
                #         sleep(2)
                #         camera.shutter_speed = camera.exposure_speed
                #         g = camera.awb_gains
                #         print("Camera awb gains:" + str(g))
                #         camera.awb_mode = "off"
                #         camera.awb_gains = g
                #         sleep(2)
                #
                #         print(' [' + str(counter+1) + ' of ' + str(total_photos) + '] ' + filename)
                #         #camera.capture(filename, bayer=True, use_video_port=False)
                #         camera.capture(filename, use_video_port=False)

                sleep(delay)


            ##---------------------------------------Capturing Thermal Images -----------------------------------------------------##

            thermal_cam = LeptonThermalCamera(
                    save_folder=thermal_img_folder,
                    time_interval_seconds=1,
                    save_celsius_images=True,
                    save_colored_image=True
                )

            thermal_cam.open()
            thermal_cam.capture_once()

            t2 = datetime.now()
            print('Capturing ended at ' + 'date_' + str(t2.day) + '-' + str(t2.month) + '-' + str(t2.year) + '_' + str(
                t2.hour) + '.' + str(t2.minute) + '.' + str(t2.second))

            buzzer.play_super_mario()
            blink_event.clear()
            sleep(1)
        sleep(0.1)
finally:
    destroy()
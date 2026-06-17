"""
@author: Lochana Marasinghe
@date: 5/27/2026
@description:
"""

import time
from datetime import datetime

import picamera

pi_camera_folder = '/home/pi/Documents/2026/'
cam_name = 'pi17_iso100'

t1 = datetime.now()

print('Camera_run.py begins at ' + 'date_' + str(t1.day) + '-' + str(t1.month) + '-' + str(t1.year) + '_' + str(
    t1.hour) + '.' + str(t1.minute) + '.' + str(t1.second))

# Photo session settings
total_photos = 3  # Total number of images to be taken
delay = 1  # Time interval between each photo (in seconds)


def config_camera(cam):
    cam.sensor_mode = 2
    cam.resolution = (3280, 2464)

    cam.hflip = True
    cam.vflip = True
    time.sleep(1)
    cam.iso = 100
    time.sleep(2)


#     cam.shutter_speed = cam.exposure_speed
#     cam.exposure_mode ='off'
#     g = cam.awb_gains
#     print("Camera awb gains:" + str(g))
#     cam.awb_mode = "off"
#     cam.awb_gains = g
#     time.sleep(2)

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
    #         time.sleep(2)
    #         camera.iso = 100
    #         time.sleep(2)
    #         camera.shutter_speed = camera.exposure_speed
    #         g = camera.awb_gains
    #         print("Camera awb gains:" + str(g))
    #         camera.awb_mode = "off"
    #         camera.awb_gains = g
    #         time.sleep(2)
    #
    #         print(' [' + str(counter+1) + ' of ' + str(total_photos) + '] ' + filename)
    #         #camera.capture(filename, bayer=True, use_video_port=False)
    #         camera.capture(filename, use_video_port=False)
    time.sleep(delay)

t2 = datetime.now()

print('Camera_run.py begins at ' + 'date_' + str(t2.day) + '-' + str(t2.month) + '-' + str(t2.year) + '_' + str(
    t2.hour) + '.' + str(t2.minute) + '.' + str(t2.second))


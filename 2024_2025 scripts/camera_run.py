"""
Created on Wed April 26 20:30:30 2023
@author: Adapted from kesevan.veloo modified by Lochana Marasinghe
"""
import os
from time import sleep
from datetime import datetime

import cv2
import numpy as np
import pithermalcam as ptc
from picamera import PiCamera

# MLX sensor image folder
mlx_folder = '/home/pi/Documents/data/mlx/'
# Lepton camera image folder
lepton_folder = '/home/pi/Documents/data/lepton/'
# Pi RGB+NoIR camera image folder
pi_camera_folder = '/home/pi/Documents/data/pi_camera/'


counter = 0
t2 = datetime.now()

print('Camera_run.py begins at ' + 'date_' + str(t2.day) + '-' + str(t2.month) + '-' + str(t2.year) + '_' + str(
                t2.hour) + '.' + str(t2.minute) + '.' + str(t2.second))

# Photo session settings
total_photos = 1  # Total number of images to be taken
countdown = 1  # Time interval between each photo (in seconds)
font = cv2.FONT_HERSHEY_SIMPLEX

# Camera settings 
cam_width = 1280  # Width setting for the camera sensor
cam_height = 928  # Height setting for the camera sensor

# Final image capture settings 
scale_ratio = 1  # Scale ratio for image capture

# Adjust camera resolution to be compatible with PiCamera requirements 
cam_width = int((cam_width + 31) / 32) * 32
cam_height = int((cam_height + 15) / 16) * 16
print("Camera resolution: " + str(cam_width) + " x " + str(cam_height))

# Buffer for captured image 
img_width = int(cam_width * scale_ratio)
img_height = int(cam_height * scale_ratio)
capture = np.zeros((img_height, img_width, 4), dtype=np.uint8)
print("Scaled image resolution: " + str(img_width) + " x " + str(img_height))

# Initialize the stereo camera (RGB + NoIR)
camera = PiCamera(stereo_mode='side-by-side', stereo_decimate=False)
camera.resolution = (cam_width, cam_height)
camera.framerate = 20
camera.hflip = True
camera.vflip = True

# For consistent images images: Ref: https://picamera.readthedocs.io/en/release-1.13/recipes1.html#capturing-consistent-images
print("Current ISO: " + str(camera.iso))
camera.iso = 100
sleep(2) #to automatic gain control to settle
print("Adjusted ISO: " + str(camera.iso))
camera.shutter_speed = camera.exposure_speed
g = camera.awb_gains
print("AWB gains:" + str(g))
print("Current AWB mode:" + str(camera.awb_mode))
camera.awb_mode = 'off'
print("Adjusted AWB mode:" + str(camera.awb_mode))
camera.awb_gains = g


# Initialize the Lepton 3.5 camera capture function
def thermal_capture(counter, t2):
    global lepton_filename, cap
    try:
        for i in range(5):

            print("testing the presence of camera #{}..".format(i))
            sleep(3)
            cap = cv2.VideoCapture(i, cv2.CAP_V4L2)

            if cap.isOpened() and (cap.get(3) == 160 or cap.get(3) == 80):
                break

        if not cap.isOpened():
            print("Lepton camera not found, skipping capture.")
            raise Exception("Lepton Camera Not Found")

        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"Y16 "))
        cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)

        ret, frame = cap.read()

        if not ret:
            print("Failed to capture image from Lepton camera, skipping capture.")
            cap.release()
            raise Exception("Failed to capture thermal camera image")

        # Save the image if capture was successful
        lepton_filename = lepton_folder + 'date_' + str(t2.day) + '-' + str(t2.month) + '-' + str(t2.year) + '_' + str(
            t2.hour) + '.' + str(t2.minute) + '.' + str(t2.second) + '_' + str(counter) + '.png'
        frame = frame[0:120, :]  # the captured frame is 160x122. It should be 160x120. So cropping the captured frame
        cv2.imwrite(lepton_filename, frame)

        print('Lepton Image Saved: ' + lepton_filename)

        frame_normalized = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        colored_image = cv2.applyColorMap(frame_normalized, cv2.COLORMAP_JET)

        colored_lepton_filename = lepton_folder + 'date_' + str(t2.day) + '-' + str(t2.month) + '-' + str(t2.year) + '_' + str(
            t2.hour) + '.' + str(t2.minute) + '.' + str(t2.second) + '_' + str(counter) + '_colored.png'
        cv2.imwrite(colored_lepton_filename, colored_image)
        print('Lepton Color Image Saved: ' + colored_lepton_filename)

    except Exception as e:
        print(e)
        lepton_filename = "N/A"
    finally:
        cap.release()
        return lepton_filename

def thermalcamwarmup():
    global cap
    try:
        for i in range(5):

            print("testing the presence of camera #{}..".format(i))
            sleep(3)
            cap = cv2.VideoCapture(i, cv2.CAP_V4L2)

            # cap.get(3) =  Width of the frame
            if cap.isOpened() and (cap.get(3) == 160 or cap.get(3) == 80):
                break

        if not cap.isOpened():
            print("Lepton camera not found, skipping capture.")
            return "N/A"

        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"Y16 "))
        cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)

        ret, frame = cap.read()

        if not ret:
            print("Failed to capture image from Lepton camera, skipping capture.")
            cap.release()

    except Exception as e:
        print(e)
    finally:
        cap.release()


# Initialize the MLX90640 sensor capture function

def mlx90640capture():
    global temp_f, temp_c, mlx_filename, mlx_values
    try:
        therm_cam = ptc.pithermalcam(output_folder=mlx_folder)

        mlx_values = therm_cam.get_raw_mlx_temp_values()
        mlx_filename = therm_cam.save_image()

        temp_c = np.mean(mlx_values)
        temp_f = therm_cam._c_to_f(temp_c)
    except Exception as e:
        print(e)
        temp_c, temp_f, mlx_filename, mlx_values = 'N/A', 'N/A', 'N/A', []
    finally:
        return temp_c, temp_f, mlx_filename, mlx_values

def mlx90640warmup():
    try:
        therm_cam = ptc.pithermalcam(output_folder=mlx_folder)
        therm_cam.get_raw_mlx_temp_values()
    except Exception as e:
        print("Error occurred in mlx sensor warmup: ")
        print(e)

# Start taking photos
print("Starting photo sequence")

# Continuous capture loop
try:
    for frame in camera.capture_continuous(capture, format="bgra", use_video_port=True, resize=(img_width, img_height)):

        t1 = datetime.now()

        countdown_timer = countdown - int((t1 - t2).total_seconds())

        # Capture from the stereo(RGB + NoIR) camera
        if countdown_timer == -1:
            counter += 1

            filename = pi_camera_folder + 'date_' + str(t2.day) + '-' + str(t2.month) + '-' + str(t2.year) + '_' + str(
                t2.hour) + '.' + str(t2.minute) + '.' + str(t2.second) + '_' + str(counter) + '.png'
            cv2.imwrite(filename, frame)

            print(' [' + str(counter) + ' of ' + str(total_photos) + '] ' + filename)

            t2 = datetime.now()
            t2_millis = t2.timestamp() * 1000

            # Capture from the Lepton 3.5 camera
            thermalcamwarmup()
            lepton_filename = thermal_capture(counter, t2)
            # lepton_filename = 'N/A'

            # Capture from the MLX90640 sensor
            mlx90640warmup() # avoid taking the 1st one
            temp_c, temp_f, mlx_filename, mlx_values = mlx90640capture()
            #temp_c, temp_f, mlx_filename, mlx_values = 'N/A', 'N/A', 'N/A', []

            # Write the multi spectral and Lepton 3.5 data to CombinedData.csv
            with open('/home/pi/Documents/data/CombinedData.csv', 'a') as file:
                file.write(
                    '{},{},{},{},{},{},{:.2f}\n\n'.format(filename, lepton_filename, mlx_filename, temp_c, temp_f,
                                                                 mlx_values, t2_millis))

            sleep(1)
            countdown_timer = 0  # Reset the countdown timer

        if counter == total_photos:
            break  # Exit loop after taking the set number of photos
except Exception as e:
    print(e)
finally: 
    print("Photo sequence finished")
    os.system("sudo shutdown -h now")

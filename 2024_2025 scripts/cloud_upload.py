import os
import time

try:
    os.system("rclone sync /home/pi/Documents/data/ othello_data:upload/pi<camera_number>")
    time.sleep(20)
finally:
    os.system("sudo shutdown -h now")
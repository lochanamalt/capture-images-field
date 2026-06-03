import time
from datetime import datetime
from pathlib import Path
import platform

import cv2

class LeptonThermalCamera:
    def __init__(
            self,
            save_folder: str = "thermal-images",
            time_interval_seconds: int = 60,
            save_celsius_images: bool = True,
            save_colored_image: bool = True):

        self.save_folder = Path(save_folder)
        self.save_folder.mkdir(parents=True, exist_ok=True)

        self.time_interval = time_interval_seconds
        self.save_celsius_images = save_celsius_images
        self.save_colored_image = save_colored_image

        self.cap = None
        self.camera_port = None


    def find_camera(self, max_ports: int = 5):
        """
        Scan through local camera ports to find Lepton camera.
        """
        for i in range(max_ports):
            print(f"Testing camera port #{i}...")
            time.sleep(3)
            cap = cv2.VideoCapture(i, cv2.CAP_V4L2)

            if cap.isOpened():
                width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                if width in (160, 80):
                    print(f"[Found] Lepton camera detected at port {i}")
                    cap.release()
                    self.camera_port = i
                    return i

            cap.release()

        print("[Error] No Lepton thermal camera found.")
        return None

    def open(self, camera_port = None):
        """
        Open the camera stream.
        """

        if camera_port is None:
            camera_port = self.find_camera()

        if camera_port is None:
            raise RuntimeError("Cannot open camera. No valid port.")

        self.camera_port = camera_port
        self.cap = cv2.VideoCapture(camera_port, cv2.CAP_V4L2)

        if not self.cap.isOpened():
            raise RuntimeError("Failed to open Lepton camera.")

        # Configure for 16-bit grayscale raw output
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"Y16 "))
        self.cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)

        print(f"Camera opened on port {camera_port}")



    def capture_frame(self):
        """
        Capture a single thermal frame. Returns raw frame and Celsius temp array.
        """
        if self.cap is None:
            raise RuntimeError("Camera not opened.")

        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to capture frame from camera.")

        # Fix the height (Lepton returns 160×122, correct to 160×120)
        frame = frame[0:120, :]

        # Convert centi-Kelvin values to Celsius
        temp_c = (frame - 27315) / 100.0

        return frame, temp_c

    def save_frame(self, frame, timestamp, isCelsius: bool =  False):
        """
        Save raw 16-bit thermal frame.
        """
        if isCelsius:
            filename = self.save_folder / f"lepton_{timestamp}_celsius.tiff"
        else:
            filename = self.save_folder / f"lepton_{timestamp}.png"
        cv2.imwrite(str(filename), frame)
        print(f"Saved {filename}")

        return filename

    def save_colored(self, frame, timestamp):
        """
        Save normalized + colormap version.
        """
        frame_normalized = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        colored_image = cv2.applyColorMap(frame_normalized, cv2.COLORMAP_JET)

        filename = self.save_folder / f"lepton_{timestamp}_colored.png"
        cv2.imwrite(str(filename), colored_image)
        print(f"Saved {filename}")

        return filename

    def capture_once(self):
        """
        Capture thermal image once
        """
        if self.cap is None:
            raise RuntimeError("Camera not opened. Call open() first.")

        print("Starting to capture thermal image...")

        try:
            timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

            frame, celsius_temp = self.capture_frame()

            if self.save_celsius_images:
                self.save_frame(celsius_temp, timestamp, True)

            if self.save_colored_image:
                self.save_colored(frame, timestamp)

        except Exception as e:
            print("[Error]", e)

        finally:
            self.close()

    def start_capture_loop(self):
        """
        Begin an infinite capture loop. Press Ctrl+C to exit.
        """
        if self.cap is None:
            raise RuntimeError("Camera not opened. Call open() first.")

        print("Starting capture loop...")

        try:
            while True:
                timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

                frame, celsius_temp = self.capture_frame()
                self.save_frame(frame, timestamp)

                if self.save_celsius_images:
                    self.save_frame(celsius_temp, timestamp, True)

                if self.save_colored_image:
                    self.save_colored(frame, timestamp)

                time.sleep(self.time_interval)

        except KeyboardInterrupt:
            print("\nCapturing Stopped.")

        except Exception as e:
            print("[Error]", e)

        finally:
            self.close()

    def close(self):
        if self.cap:
            self.cap.release()
            self.cap = None
            print("Camera capture released.")


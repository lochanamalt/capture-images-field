# Automated Field Camera Capture & Cloud Sync

![License](https://img.shields.io/badge/License-CC_BY--NC_4.0-blue.svg)
![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen.svg)
[![Python](https://img.shields.io/badge/Python-3.9+-navy.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi-red.svg)](https://raspberrypi.org)
![Research](https://img.shields.io/badge/By-WSU--Phenomics-yellow.svg)

This repository contains the configurations, image capturing scripts, automation scripts
, and deployment documentation for field-deployed imaging nodes.
The system captures daily, scheduled imagery collection
(RGB, NoIR, FLIR Lepton thermal camera and Melexis MLX90640 thermal array)
and synchronizes all raw assets directly to
remote cloud storage (Azure File Share).

---

## Repository Navigation Guide

### [Raspberry Pi Setup, Sensor Integrations, Image Capture Scheduling & Power Management](2024_2025%20scripts/GUIDE_SETUP_PI.md)

Navigate to the `GUIDE_SETUP_PI.md` inside the `2024_2025 scripts` folder for OS and sensor configurations, including:

* Flashing operating systems (`Raspbian Bullseye armv7l`).
* Activating system peripheral buses (`I2C`, `SPI`, `Camera`).
* Installing relevant drivers and libraries
* Integrating driver library modifications
* Configuring power on/off schedules
* Scheduling for automated image capture

The image capturing script can be found in **[camera_run.py](2024_2025%20scripts/camera_run.py)**

### [Azure Storage Sync](2024_2025%20scripts/GUIDE_CLOUD_SYNC.md)

* Uses `rclone` to bridge local data folders to a **Azure Storage File Share** using 
SMB/REST access keys.
* Automates uploads through timed synchronization process.



### [Sample Data Structure](2024_2025%20scripts/data%20sample/)


Review the [Sample Data Folder](2024_2025%20scripts/data%20sample/) to see how the daily field images are saved and formatted.

---


## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0). 

**Commercial sale, paid distribution, or monetization of this software is strictly prohibited.** It is freely available for educational, personal, and academic research purposes. See the [LICENSE](LICENSE) file for details.


# Azure Storage Integration & Client File Synchronization

This document outlines the configuration required
to sync stored images directly to the **Azure Storage File Share**.


## Creating the Storage Share

1. Sign in to the cloud subscription on the **Azure Portal**
2. Create a **Storage Account**
3. Create an Azure File Share inside the storage account and form the target directory structures (e.g., `upload/pi1`)

Refer: https://learn.microsoft.com/en-us/azure/storage/files/storage-how-to-use-files-portal?tabs=azure-portal

## Raspberry Pi Configuration and Sync

To sync local data directories on the Raspberry Pi to Azure SMB/REST backends, `rclone` is used.

### 1. Installing `rclone`
 Refer: https://pimylifeup.com/raspberry-pi-rclone

```bash
sudo su
wget https://downloads.rclone.org/v1.66.0/rclone-v1.66.0-linux-arm.zip
unzip -j -d rclone-temp rclone-v1.66.0-linux-arm.zip
```
---

### 2. Creating the Remote Cloud Connection Target
Refer: https://rclone.org/azurefiles

Initiate the interactive rclone remote provisioning walkthrough:

Remote name: `othello_data` (Give a name for the remote connection)

Storage: `Microsoft Azure Files Storage`

Account: (Enter the exact name of the Azure Storage Account)

Share name: (Enter the targeted destination File Share container name) 

Env auth: (Leave empty)

Key: (This is the access key you can find in the storage account.
Go to the Azure storage account. Select access keys in the left panel.
There are 2 keys. Click show and copy the first key and paste it here.)

SAS URL: (Leave empty)

Connection String: (This is available in the same location you copied the access key.
It’s below the key. Copy and paste it here.)

Accept the default empty values for all remaining prompts,
then confirm configuration save states by pressing **Yes**.

---

### 3. Sync Verification and Commands

Test the active cloud handshake using the terminal:

See the root files: 
```bash
rclone lsf othello_data:
```
Create a directory in remote: 
```bash
rclone mkdir othello_data:ndvi
```

Sync files from a directory in Raspberry Pi to a directory in remote:
```bash
rclone sync /home/pi/Documents/data/ othello_data:upload/pi1
```

---

## Scheduling Cloud Upload

To ensure all captured field imagery is synced to the cloud a cronjob is created.

Open the crontab:
```bash
sudo crontab -e
```

Add the following to the crontab to upload the captured data.
The cloud upload script can be found in [cloud_upload.py](cloud_upload.py)

```text
30 22 * * * python3 /home/pi/Documents/cloud_upload.py
```
Refer to the [power_and_cloud_upload_schedule_2024.txt](power_and_cloud_upload_schedule_2024.txt) to
see the schedules for each Raspberry Pi camera setup


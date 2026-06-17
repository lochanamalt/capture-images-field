##########################################################
####           Device tree file (dt-blob.bin)         ####
#### This file enables the two cameras support by the ####
#### Raspberry OS for the StereoPi boards             ####
##########################################################

This dt-blob.bin file is compatible with both CM3 and CM4.
You can use it for the StereoPi v1 and StereoPi v2.

Please put this file to the /BOOT folder on your micro SD card (or eMMC).


p.s. To enable USB ports for the StereoPi v2 (CM4-based) do not forget
to add this row to the config.txt file:
dtoverlay=dwc2,dr_mode=host

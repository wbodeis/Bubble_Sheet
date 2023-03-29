# ======================================================================================================================
# ScanSnap and iX500
# ----------------------------------------------------------------------------------------------------------------------
The software for the scanner for windows 10 is included with the zip file.  
If you have aonther OS, go to the link below, and select the one you are using.   
https://scansnap.fujitsu.com/global/dl/ix500/index-ix500.html  

Scan_Settings.PNG is a screenshot of the settings used for obtaining the best scans. 
Color mode: Color
Scanning side: Simplex
Image quality: Excellent
Rotation: Do not rotate
File format: JPEG (*.jpg)
Feed: Nomral scan

They must be placed top down, facing towards the scanner/tray.  
If that doens't make sense, scan a single page and you will understand how to feed the paper.


# ======================================================================================================================
# Folders
# ----------------------------------------------------------------------------------------------------------------------
key_pdf/
- save the pdf key files here
key_images/
- save the image key files here
scantron_pdf/
- save the pdf game sheet files here
scantron_images/
- save the image game sheet files here
results/
- .csv after gathering the data is saved here
poppler/
- required for converting pdf files into .jpeg or whatever your chosen image format may be.
- version 23.01.0 is what was included in the folder


# ======================================================================================================================
# Running the executable. 
# ----------------------------------------------------------------------------------------------------------------------
It is recommended to use powershell to run the script so you can see the readout if there are any errors that occur.
You can run it by clicking it as you norammlly would, but the console closes as soon as it gets done running.

Change the directory to where you have this folder located. The example below is for testing it on my own computer.

cd C:\Users\Administrator\Desktop\Bubble_Sheet_Portable

Then the name of the exe to run it. You need the beginning '.\' for it to run properly.
A shortcut is to begin typing its name, like bubb, then hit tab and it will autofill the rest for you. 

.\Bubble_Sheet_Portable_X.X.X.exe
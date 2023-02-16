# Bubble_Sheet
Project: OMR Scanrtron for FRC Team 5712
Author: William Bodeis <wdbodeis@gmail.com>

## Folders
You need the following folders:
- key/
- key_images/
- scantron/
- scantron_images/
- results/

keys/ and scantron/ are for .pdf files if that was how they were scanned in. The program will convert them to the specified image format. While it defaults to jpeg, which was done mostly as a way to save storage space depending on how many pages were getting converted. 
**See the note below pertaining to processing the pdf files.** 

keys_images/ and scantron_images/ are where the image files should be saved if those are being used instead of pdfs.

## PDF Processing.
If your input files are .pdf instead of an image format then you must download the folder at the link below. 
Download the most current version of poppler and save it to the root folder. 
https://github.com/oschwartz10612/poppler-windows

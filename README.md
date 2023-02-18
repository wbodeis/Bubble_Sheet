# Bubble_Sheet
Project: OMR Scanrtron for FRC Team 5712  
Author: William Bodeis <wdbodeis@gmail.com>  

## Environment
Poetry was used for creating and running the enviroment for this project.  
> [Poetry Homepage](https://python-poetry.org/)

# Dependencies
python = ">=3.10,<3.12"
numpy = "^1.24.1"
opencv-python = "^4.7.0.68"
pillow = "^9.4.0"
pdf2image = "^1.16.2"
pandas = "^1.5.3"

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
If your input files are .pdf instead of an image format, then you must download the folder at the link below.  
Download the most current version of poppler and save it to the root folder.  
> [GitHub Page](https://github.com/oschwartz10612/poppler-windows).
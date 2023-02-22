# Bubble_Sheet
Project: OMR Scantron for FRC Team 5712  
Author: William Bodeis <wdbodeis@gmail.com>  

This is to be used with the pdf included in this project (Game_Sheet.pdf) specific to the FIRST 2023 season "Charged Up."  
The folders are needed and the program will first check for those. If they are not there, it will create them before exiting to be sure all the files are in the correct folders.  
It will also close if there aren't any keys or game sheets to be read in and used, since there is no point in running the program without either available.  

## Environment
Poetry was used for creating and running the environment for this project.  
> [Poetry Homepage](https://python-poetry.org/)  

The pyproject.toml was also included to be used or the dependencies are listed below to use with whatever your preferred environment may be.  

### Dependencies
python = ">=3.10,<3.12"  
numpy = "^1.24.1"  
opencv-python = "^4.7.0.68"  
pillow = "^9.4.0"  
pdf2image = "^1.16.2"  
pandas = "^1.5.3"  
pyinstaller = "^5.8.0"  

## Folders
You need the following folders:  
- key/
- key_images/
- scantron/
- scantron_images/
- results/  
- poppler/

These will be created if they don't already exist when the program runs, causing FileNotFoundError because it is assumed the files are not in the correct locations.  
Once the folders are created and contain the necessary files, it will run all the way through.  
keys/ and scantron/ are for .pdf files if that was how they were scanned in. The program will convert them to the specified image format. While it defaults to jpeg, which was done mostly as a way to save storage space depending on how many pages were getting converted.  
**See the note below pertaining to processing the pdf files.** 

keys_images/ and scantron_images/ are where the image files should be saved if those are being used instead of pdfs.  

## PDF Processing.
If your input files are .pdf instead of an image format, then you must download the folder at the link below.  
Download the most current version of poppler and save it to the root folder.  
> [GitHub Page](https://github.com/oschwartz10612/poppler-windows).  

## Classes
### Bubble_Sheet
Highest level class for running and acquiring the game data.  
### OMR
Optical Mark Recognition (OMR)  
The class is used in doing the heavy lifting for manipulating and collating the data.  
It will convert pdf files to whatever file format you send, while defaulting to jpeg.  
It makes seperate lists of keys and game sheets so they can be compared to one another to get the marked bubbles.  
It is setup to be used with blue ballpoint pens, but pencils may work. I haven't tested them to say for certain that they will.  
It uses the HSV for determining the color spectrum to test against and the snippet is what was used for 'blue.'  
```
lower_range = np.array([110,50,50])
upper_range = np.array([130,255,255])
```
  
### Scantron
Class for creating an object of each game sheet scanned.  
The various methods were broken out in attempt to make it more readable, while it could have just been one large one with a bunch of nested if statements.  
Everything is determined against the pixel location of the averaged key value(s) that are gathered so the X and Y values fit with the given range of pixel_differential value.  
Everything is stored in the object and returned using _get_raw_data(). 


## Running the executable. 

It is recommended to use powershell to run the script so you can see the readout if there are any errors that occur.
You can run it by clicking it as you norammlly would, but the console closes as soon as it gets done running.

Change the directory to where you have this folder located. The example below is for testing it on my own computer.

cd C:\Users\Administrator\Desktop\Bubble_Sheet_Portable

Then the name of the exe to run it. You need the beginning '.\\' for it to run properly.
A shortcut is to begin typing its name, like bubb, then hit tab and it will autofill the rest for you. 

.\Bubble_Sheet_Portable_0.3.1.exe

key/
- save the pdf key files here  

key_images/
- save the image key files here  

scantron/
- save the pdf game sheet files here  

scantron_images/
- save the image game sheet files here  

results/
- .csv after gathering the data is saved here  

poppler/
- required for converting pdf files into .jpeg or whatever your chosen image format may be.
- version 23.01.0 is what was included in the folder
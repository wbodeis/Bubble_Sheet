# Bubble_Sheet
Project: OMR Scantron for FRC Team 5712  
Author: William Bodeis <wdbodeis@gmail.com>  

This is to be used with the pdf included in this project (Game_Sheet_Ver_XXX.pdf) specific to the FIRST 2023 season "Charged Up."  
The folders are needed, and the program will first check for those. If they are not there, it will create them before exiting to be sure all the files are in the correct folders.  
It will also close if there aren't any keys or game sheets to be read in and used, since there is no point in running the program without either available.  
Pyinstaller is a part of the dependencies to create the standalone executable, so more people are able to run it. The .spec sheet is also included for creating the .exe.
The only thing missing is poppler, which is talked about more below and how to download the folder you need.  

## Environment
Poetry was used for creating and running the environment for this project.  
> [Poetry Homepage](https://python-poetry.org/)  

The pyproject.toml was also included to be used or the dependencies are listed below to use with whatever your preferred program to create virtual environments.  

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
- key_images/
- key_pdf/
- scantron_images/
- scantron_pdf/
- results/  

These will be created if they don't already exist when the program runs, causing FileNotFoundError because it is assumed the files are not in the correct locations.  
Once the folders are created and contain the necessary files, it will run all the way through.  
keys/ and scantron/ are for .pdf files if that was how they were scanned in. The program will convert them to the specified image format. While it defaults to jpeg, which was done mostly to save storage space depending on how many pages were getting converted.  
**See the note below pertaining to processing the pdf files.** 

keys_images/ and scantron_images/ are where the image files should be saved if those are being used instead of pdfs.  

## PDF Processing.
If your input files are .pdf instead of an image format, then save them into the folders ending in _pdf. Poppler was previously required for running the program, which is no longer the case and incorporated into the executable.  

## Classes
### Bubble_Sheet
Highest level class for running and acquiring the game data.  
### OMR
Optical Mark Recognition (OMR)  
The class is used in doing the heavy lifting for manipulating and collating the data.  
It will convert pdf files to whatever file format you send, while defaulting to jpeg.  
It makes separate lists of keys and game sheets so they can be compared to one another to get the marked bubbles.  
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
It is recommended to use PowerShell to run the script so you can see the readout if there are any errors that occur.
You can run it by clicking it as you normally would, but the console closes as soon as it gets done running.

Change the directory to where you have this folder located. The example below is for testing it on my own computer.

cd C:\Users\Administrator\Desktop\Bubble_Sheet_Portable

Then the name of the exe to run it. You need the beginning '.\\' for it to run properly.
A shortcut is to begin typing its name, like bubb, then hit tab and it will autofill the rest for you. 

.\Bubble_Sheet_Portable_X.X.X.exe

key/
- Save the pdf key files here  

key_images/
- Save the image key files here  

scantron/
- Save the pdf game sheet files here  

scantron_images/
- Save the image game sheet files here  

results/
- .csv after gathering the data is saved here  

poppler/
- Now incorporated with the executable from pyinstaller so the folder no longer needs to be included.
- Required for converting pdf files into .jpg or whatever your chosen image format may be.
- Version 23.01.0 currently being used with the executable.  

## Known Issues  
### Memory Error
A computer running the program with an insufficient amount of ram will throw an error while trying to process the images. Some searching also seems to indicate that a lack of storage space may also lead to the issue when it tries to allocate the ROM due to the lack of ram. The example below, most of the ram was being used and there was only ~700mb of space left on the drive.  
The laptop had an AMD Ryzen 5 3550H, 8gb of ram, 256gb ssd, and running windows 11.  
An example that occurred while attempting to run:  
> OpenCV(4.7.0) D:\a\opencv-python\opencv-python\opencv\modules\core\src\alloc.cpp:73: error: (-4:Insufficient memory) Failed to allocate 33500544 bytes in function 'cv::OutOfMemoryError'  

### Divide by Zero
A random error would occur with 'ZeroDivisionError' while finding the contours of an image. The best advice found was to put an if-else to help catch the error and not break the program. That specific point will be skipped while trying to ensure all the other points are kept.  
The code snippet for this:  
```
for contour in contours:
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    else:
        continue
```
This is why it is recommended to have 3+ keys created and used for comparing the game sheets against. Later in the program, if a key file doesn't have the exact number of required marks, it will NOT be used in getting the average mark location. Potentially not having any available to check against and causing the program to exit without doing any of the work. 

### Popple Path
Not an issue that has cropped up yet, but wanted to put it here just in case something does happen. The poppler folder is apart of the exe and should not be an issue if you are processing pdf files. If there is an issue like the one below:  
> 'Unable to get page count. Is poppler installed and in PATH?'  

Download the most current version of poppler and save it to the root folder.  
> [GitHub Page](https://github.com/oschwartz10612/poppler-windows).  
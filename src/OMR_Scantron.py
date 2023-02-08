#======================================================================================================================+
# FIle:  Bubble_Sheet/src/main.py
# Project: OMR Scanrtron for FRC Team 5712
# Author:  William Bodeis <wdbodeis@gmail.com>
#-----------------------------------------------------------------------------------------------------------------------

import os, cv2, numpy as np
from pdf2image import convert_from_path

class OMR_Scantron():
    def __init__(self) -> None:
        self._PDF_directory: str = 'input/'
        self._image_directory: str = 'images/'
        self._results_directory: str = 'results/'
        self._pdf_names: list[str]
        self._scanned_values: dict = {}

        # Initializing functions.
        self._check_directories()
        self._get_pdf_names()

        if self._pdf_names == None:
            del self
            raise FileNotFoundError('No PDF files were found.')
        
        self._convert_pdf_to_jpeg()
        self._process_images()

        print(self._scanned_values)
        
#-----------------------------------------------------------------------------------------------------------------------
    def _check_directories(self):
        directories = [self._PDF_directory,
                       self._image_directory, 
                       self._results_directory]
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

#-----------------------------------------------------------------------------------------------------------------------
    def _get_pdf_names(self):
        self._pdf_names = [i for i in os.listdir(self._PDF_directory) if i.endswith('.pdf')]

#-----------------------------------------------------------------------------------------------------------------------
    def _convert_pdf_to_jpeg(self):
        for i in range(len(self._pdf_names)):
            image = convert_from_path(self._PDF_directory + self._pdf_names[i],
                                      poppler_path = 'poppler/Library/bin',
                                      dpi = 700,  
                                      last_page = 1,
                                      thread_count = 10)
            location = self._image_directory + str(i) + '.jpeg'
            image[0].save(fp = location,
                          bitmap_format = 'JPEG')


#-----------------------------------------------------------------------------------------------------------------------
    def _get_averages(self):
        # TODO Do this for the completely fileld out forms
        # Also try and figure out the RMS for all of them
        pass

#-----------------------------------------------------------------------------------------------------------------------
    def _process_images(self):
        for i in range(len(self._pdf_names)):
            marks = []
            img = cv2.imread('images/' + str(i) + '.jpeg')

            # Threshold for blue.
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower_range = np.array([110,50,50])
            upper_range = np.array([130,255,255])

            # Threshold for green.
            # lower_range = np.array([36, 25, 25])
            # upper_range = np.array([70, 255,255])

            # TODO Get the correct HSV color for the red
            # Threshold for red.
            # lower = np.array([155,25,0])
            # upper = np.array([179,255,255])

            thresh = cv2.inRange(src = hsv,
                                 lowerBound = lower_range, 
                                 upperbBound = upper_range)

            # Apply erosion.
            kernel = np.ones(shape = (5,5),
                             dtype = np.uint8)
            erode = cv2.erode(src = thresh,
                              kernel = kernel,
                              iterations = 1)

            # Apply morphology open.
            kernel = cv2.getStructuringElement(shape = cv2.MORPH_ELLIPSE, 
                                               ksize = (30,30))
            first_morph = cv2.morphologyEx(src = erode, 
                                           kernel = kernel, 
                                           op = cv2.MORPH_OPEN)

            # Apply morphology close.
            kernel = cv2.getStructuringElement(shape = cv2.MORPH_ELLIPSE,
                                               ksize = (10,10))
            second_morph = cv2.morphologyEx(src = first_morph,
                                            kernel = kernel, 
                                            op = cv2.MORPH_CLOSE)

            # Get contours
            contours = cv2.findContours(image = second_morph,
                                        mode = cv2.RETR_EXTERNAL,
                                        method= cv2.CHAIN_APPROX_NONE)
            contours = contours[0] if len(contours) == 2 else contours[1]
            for contour in contours:
                M = cv2.moments(contour)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                pt = (cx,cy)
                marks.append(pt)
            self._scanned_values[i] = tuple(marks)
            
#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        con = OMR_Scantron()
    except Exception as ex:
        print(ex)
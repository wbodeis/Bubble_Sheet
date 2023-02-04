#======================================================================================================================+
# FIle:  Bubble_Sheet/src/main.py
# Project: OMR Scanrtron for FRC Team 5712
# Author:  William Bodeis <wdbodeis@gmail.com>
#-----------------------------------------------------------------------------------------------------------------------

import os, cv2
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
        print(self._scanned_values[0])
        
#-----------------------------------------------------------------------------------------------------------------------
    def _check_directories(self):
        directories = [self._PDF_directory, self._image_directory, self._results_directory]
        for direct in directories:
            if not os.path.exists(direct):
                os.makedirs(direct)

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
    def _get_all_circles(self):
        # TODO Do this for the completely fileld out form?
        pass

#-----------------------------------------------------------------------------------------------------------------------
    def _process_images(self):
        for i in range(len(self._pdf_names)):
            marks = []
            img = cv2.imread('images/' + str(i) + '.jpeg')

            # threshold on white color
            lower=(225,225,225)
            upper=(255,255,255)
            thresh = cv2.inRange(img, lower, upper)
            thresh = 255 - thresh

            # apply morphology close
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30,30))
            morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
            morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)

            # get contours
            result = img.copy() 
            contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            contours = contours[0] if len(contours) == 2 else contours[1]
            for contour in contours:
                M = cv2.moments(contour)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(result, (cx, cy), 20, (0, 255, 0), -1)
                pt = (cx,cy)
                marks.append(pt)
            self._scanned_values[0] = tuple(marks)
            
#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        con = OMR_Scantron()
    except Exception as ex:
        print(ex)
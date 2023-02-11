#======================================================================================================================+
# FIle:  Bubble_Sheet/src/OMR.py
# Project: OMR Scanrtron for FRC Team 5712
# Author:  William Bodeis <wdbodeis@gmail.com>
#-----------------------------------------------------------------------------------------------------------------------

import os, cv2, numpy as np, pandas as pd
from pdf2image import convert_from_path
# from score_sheet import scoring_columns

class OMR():
    def __init__(self,
                 differential:int = 30,
                 image_type: str = '.jpeg',
                 save_image_overlay = False) -> None:
        
        self.differential:int = differential
        self.image_type: str = image_type
        self.save_image_overlay = save_image_overlay,
        self._directories: list[str] = []
        self._pdf_names: list[list[str]] = []
        self._image_names: list[str]
        self._key_names: list[str]
        self._scanned_values: list = []
        self._scanned_keys: list = []
        self._total_values: int = 155

        # self._score_sheet = pd.DataFrame(columns = scoring_columns)

        # Initializing functions.
        self._create_directories_list()
        self._check_directories()

        # Checking for and converting pdf files if those are used instead of pictures.
        self._get_keys_pdf_names()
        self._get_scantron_pdf_names()

        if not self._pdf_names[0]:
            print('No keys were found to convert from a pdf.')
        else:
            self._convert_pdf_to_image('keys')
        
        if not self._pdf_names[1]:
            print('No game sheets were found to convert from a pdf.')
        else:
            self._convert_pdf_to_image('scantrons')

        self._get_image_names()
        # TODO Uncomment once this is finalized. 
        # if not self._image_names:
        #     del self
        #     raise FileExistsError('No image files to process were found.')
        self._get_key_names()

        # Getting the marks for the scantron key(s) that are entered and the actual game sheets. 
        self._process_images('keys')
        self._process_images('scantron')

        self.print_scanned_keys()
        # self.print_scanned_values()
        # self.write_to_file()

#-----------------------------------------------------------------------------------------------------------------------
    def _create_directories_list(self):
        self._directories.append('input/')      # 0
        self._directories.append('images/')     # 1
        self._directories.append('results/')    # 2
        self._directories.append('keys/')       # 3

#-----------------------------------------------------------------------------------------------------------------------
    def _check_directories(self):
        for directory in self._directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

#-----------------------------------------------------------------------------------------------------------------------
    def _get_keys_pdf_names(self):
        self._pdf_names.append([i for i in os.listdir(self._directories[3]) if i.endswith('.pdf')])

#-----------------------------------------------------------------------------------------------------------------------
    def _get_scantron_pdf_names(self):
        self._pdf_names.append([i for i in os.listdir(self._directories[0]) if i.endswith('.pdf')])

#-----------------------------------------------------------------------------------------------------------------------
    def _get_image_names(self):
        self._image_names = [i for i in os.listdir(self._directories[0]) if (i.endswith('.jpeg') or i.endswith('.jpg') or i.endswith('.png'))]

#-----------------------------------------------------------------------------------------------------------------------
    def _get_key_names(self):
        self._key_names = [i for i in os.listdir(self._directories[3]) if (i.endswith('.jpeg') or i.endswith('.jpg') or i.endswith('.png'))]

#-----------------------------------------------------------------------------------------------------------------------
    # TODO Fix so that it works with the keys and scantrons.
    def _convert_pdf_to_image(self,
                              data: str):
        count: int
        path: int
        if data == 'keys':
            count = len(self._key_names)
            path = 3
        elif data == 'scantron':
            count = len(self._image_names)
            path = 1
        for i in range(count):
            images = convert_from_path(pdf_path = self._directories[path] + self._scantron_pdf_names[i],
                                       poppler_path = 'poppler/Library/bin',
                                       dpi = 700,
                                       thread_count = 12)

            for j in range(len(images)):
                if self.image_type == '.png':
                    location = self._directories[1] + str(i+1) + '-' + str(j+1) + '.png'
                    images[j].save(fp = location,
                                bitmap_format = 'PNG')
                else:
                    location = self._directories[1] + str(i+1) + '-' + str(j+1) + '.jpeg'
                    images[j].save(fp = location,
                                bitmap_format = 'JPEG')


#-----------------------------------------------------------------------------------------------------------------------
    def _get_averages(self):
        # TODO Do this for the completely filled out forms
        # Also try and figure out the RMS for all of them
        pass

#-----------------------------------------------------------------------------------------------------------------------
    def _process_images(self,
                        data: str):
        count: int
        if data == 'keys':
            count = len(self._key_names)
        elif data == 'scantron':
            count = len(self._image_names)

        for i in range(count):
            marks = []
            if data == 'keys':
                img = cv2.imread('keys/' + self._key_names[i])
            elif data == 'scantron':
                img = cv2.imread('images/' + self._image_names[i])

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Threshold for blue.
            lower_range = np.array([110,50,50])
            upper_range = np.array([130,255,255])

            # Threshold for green.
            # lower_range = np.array([36, 25, 25])
            # upper_range = np.array([70, 255,255])

            # TODO Get the correct HSV color for the red and yellow. 
            # Threshold for red.
            # lower = np.array([155,25,0])
            # upper = np.array([179,255,255])

            # Threshold for yellow.
            # lower = np.array([20,100,100])
            # upper = np.array([30,255,255])

            thresh = cv2.inRange(hsv, lower_range, upper_range)

            # Apply erosion.
            kernel = np.ones(shape = (5,5),
                             dtype = np.uint8)
            erode = cv2.erode(src = thresh,
                              kernel = kernel,
                              iterations = 1)

            # Apply morphology open.
            kernel = cv2.getStructuringElement(shape = cv2.MORPH_ELLIPSE, 
                                               ksize = (25,25))
            first_morph = cv2.morphologyEx(src = erode, 
                                           kernel = kernel, 
                                           op = cv2.MORPH_OPEN)

            # Apply morphology close.
            kernel = cv2.getStructuringElement(shape = cv2.MORPH_ELLIPSE,
                                               ksize = (7,7))
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
            if data == 'keys':
                self._scanned_keys.append(tuple(sorted(marks)))
                # cv2.imwrite(str('results/' + self._key_names[i]), second_morph)
            elif data == 'values':
                self._scanned_values.append(tuple(sorted(marks)))
                # cv2.imwrite(str('results/' + self._image_names[i]), second_morph)
            
#-----------------------------------------------------------------------------------------------------------------------
    def print_scanned_values(self):
        print(type(self._scanned_values))
        print(len(self._scanned_values))
        for i in range(len(self._scanned_values)):
            print(len(self._scanned_values[i]))

#-----------------------------------------------------------------------------------------------------------------------
    def print_scanned_keys(self):
        print(type(self._scanned_keys))
        print(len(self._scanned_keys))
        for i in range(len(self._scanned_keys)):
            print(len(self._scanned_keys[i]))

#-----------------------------------------------------------------------------------------------------------------------
    def write_to_file(self):
        try:
            print('here')
            with open("src/output.txt", "w") as f:
                for item in self._scanned_keys[0]:
                    f.write("%s %s \n" % (item[0], item[1]))
        except Exception as ex:
            print(ex)
#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    OMR()
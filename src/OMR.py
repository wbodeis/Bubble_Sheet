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
                 pixel_differential:int = 30,
                 image_type: str = 'jpeg',
                 save_image_overlay: bool = False) -> None:

        # Possible user inputs.
        self.pixel_differential:int = pixel_differential
        self.image_type: str = image_type
        self.save_image_overlay: bool = save_image_overlay

        # Created within and used by the class. 
        self._directories: list[str] = []
        self._keys_pdf_names: list[str] = []
        self._scantron_pdf_names: list[str] = []
        self._scantron_names: list[str]
        self._key_names: list[str]
        self._scanned_values: list = []
        self._scanned_keys: list = []
        self._sorted_keys: list = []
        self._scanned_keys_average: tuple
        self._key_column_index: tuple(int) = (0, 8, 18, 26, 31, 39, 60, 74, 80, 94, 110, 124, 130, 136, 142)
        self._total_key_values: int = 155
        self._cpu_threads: int

        # self._score_sheet = pd.DataFrame(columns = scoring_columns)

        # Initializing functions.
        self._create_directories_list()
        self._check_directories()

        # Checking for and converting pdf files if those are used instead of pictures.
        self._get_key_pdf_names()
        self._get_scantron_pdf_names()
        self._get_CPU_threads()

        if not self._keys_pdf_names:
            print('No keys were found to convert from a pdf.')
        else:
            self._convert_pdf_to_image(0, 1, self._keys_pdf_names)

        if not self._scantron_pdf_names:
            print('No game sheets were found to convert from a pdf.')
        else:
            self._convert_pdf_to_image(2, 3, self._scantron_pdf_names)
        
        # Getting the names of the images to run the data. 
        self._get_key_image_names()
        self._get_scantron_image_names()
        # TODO Uncomment once this is finalized. 
        # if not self._key_names:
        #     del self
        #     raise FileExistsError('No image for key(s) to process were found.')
        # if not self._scantron_names:
        #     del self
        #     raise FileExistsError('No image for game sheets(s) to process were found.')

        # Getting the marks for the scantron key(s) that are entered and the actual game sheets. 
        self._process_images(image_directory = 1, 
                             image_names = self._key_names, 
                             data = 'key')

        # Getting the values from the game sheets. 
        self._process_images(image_directory = 3,
                             image_names = self._scantron_names,
                             data = 'scantron')
        
        self._sort_key_values()
        # self._get_key_average()
        # Just for testing purposes. 
        # self.print_scanned_keys()
        # self.print_scanned_values()
        self.print_sorted_keys()
        # self.write_to_file()

#-----------------------------------------------------------------------------------------------------------------------
    def _create_directories_list(self):
        self._directories.append('key/')                # 0
        self._directories.append('key_images/')         # 1
        self._directories.append('scantron/')           # 2
        self._directories.append('scantron_images/')    # 3
        self._directories.append('results/')            # 4
        
#-----------------------------------------------------------------------------------------------------------------------
    def _check_directories(self):
        for directory in self._directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

#-----------------------------------------------------------------------------------------------------------------------
    def _get_key_pdf_names(self):
        self._keys_pdf_names = [i for i in os.listdir(self._directories[0]) if i.endswith('.pdf')]

#-----------------------------------------------------------------------------------------------------------------------
    def _get_key_image_names(self):
        self._key_names = [i for i in os.listdir(self._directories[1]) if (i.endswith('.jpeg') or i.endswith('.jpg') or i.endswith('.png'))]

#-----------------------------------------------------------------------------------------------------------------------
    def _get_scantron_pdf_names(self):
        self._scantron_pdf_names = [i for i in os.listdir(self._directories[2]) if i.endswith('.pdf')]

#-----------------------------------------------------------------------------------------------------------------------
    def _get_scantron_image_names(self):
        self._scantron_names = [i for i in os.listdir(self._directories[3]) if (i.endswith('.jpeg') or i.endswith('.jpg') or i.endswith('.png'))]

#-----------------------------------------------------------------------------------------------------------------------
    def _get_CPU_threads(self):
        temp_threads = 1
        try:
            temp_threads = os.cpu_count()
        except:
            self._cpu_threads = temp_threads
        self._cpu_threads = temp_threads

#-----------------------------------------------------------------------------------------------------------------------
    # TODO Fix so that it works with the keys and scantrons.
    def _convert_pdf_to_image(self, pdf_directory, image_directory, pdf_names):

        for i in range(len(pdf_names)):
                images = convert_from_path(pdf_path = self._directories[pdf_directory] + pdf_names[i],
                                           poppler_path = 'poppler/Library/bin',
                                           dpi = 700,
                                           thread_count = self._cpu_threads)

                for j in range(len(images)):
                    try:
                        location = self._directories[image_directory] + str(i+1) + '-' + str(j+1) + '.' + self.image_type
                        images[j].save(fp = location,
                                       bitmap_format = self.image_type.upper())
                    except:
                        location = self._directories[image_directory] + str(i+1) + '-' + str(j+1) + '.jpeg'
                        images[j].save(fp = location,
                                       bitmap_format = 'JPEG')

#-----------------------------------------------------------------------------------------------------------------------
    def _sort_key_values(self):
        temp_sorted_key_values = []
        for key in self._scanned_keys: # Looping through each key
            temp_key_sorted = []
            for i in range(len(self._key_column_index)): # Sorting out each 'column'
                if i == (len(self._key_column_index) - 1):
                    temp_column = key[self._key_column_index[i]: (self._total_key_values + 1)]
                else:
                    temp_column = key[self._key_column_index[i]: self._key_column_index[i+1]]
                temp_key_sorted += sorted(temp_column, key = lambda x: x[1]) # Sorting the column. TODO Move the\
            temp_sorted_key_values.append(temp_key_sorted) # Adding the list of each key to the mega list.
        self._sorted_keys = temp_sorted_key_values

#-----------------------------------------------------------------------------------------------------------------------
    def _get_key_average(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------
    # TODO Get the correct HSV color for the other colors and verify what was found for greem, red, and yellow.
    def _process_images(self, image_directory, image_names, data):
            for i in range(len(image_names)):
                try:
                    marks = []
                    img = cv2.imread(self._directories[image_directory] + image_names[i])
                    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

                    # Threshold for blue.
                    lower_range = np.array([110,50,50])
                    upper_range = np.array([130,255,255])

                    # Threshold for green.
                    # lower_range = np.array([36, 25, 25])
                    # upper_range = np.array([70, 255,255])

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
                    if self.save_image_overlay:
                        result = img.copy() 
                    for contour in contours:
                        M = cv2.moments(contour)
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        pt = (cx,cy)
                        marks.append(pt)
                        if self.save_image_overlay:
                            cv2.circle(result, (cx, cy), 25, (0, 255, 0), -1)
                    if data == 'key' and self.save_image_overlay:
                        self._scanned_keys.append(tuple(sorted(marks)))
                        cv2.imwrite(('results/' + 'key_overlay_' + str(i) + '.jpeg'), result)
                    elif data == 'key':
                        self._scanned_keys.append(tuple(sorted(marks)))
                    elif data == 'scantron' and self.save_image_overlay:
                        self._scanned_values.append(tuple(sorted(marks)))
                    elif data == 'scantron':
                        self._scanned_values.append(tuple(sorted(marks)))
                        cv2.imwrite(('results/' + 'scantron_overlay_' + str(i) + '.jpeg'), result)
                except Exception as ex:
                    print(ex)
            
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
    def print_sorted_keys(self):
        print(type(self._sorted_keys))
        print(len(self._sorted_keys))
        for i in range(len(self._sorted_keys)):
            print(len(self._sorted_keys[i]))

#-----------------------------------------------------------------------------------------------------------------------
    def write_to_file(self):
        try:
            count = 0
            with open("src/output.txt", "w") as f:
                # for item in self._scanned_keys[0]:
                for item in self._sorted_keys[0]:
                    # f.write("%s %s \n" % (item[0], item[1]))
                    # f.write("%d: ((%s, %s), ), \n" % (count, item[0], item[1]))
                    f.write("%d: (%s, %s)\n" % (count, item[0], item[1]))
                    count += 1
        except Exception as ex:
            print(ex)
        
#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    OMR()
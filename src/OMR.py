#======================================================================================================================+
# FIle:  Bubble_Sheet/src/OMR.py
# Project: OMR Scantron for FRC Team 5712
# Author:  William Bodeis <wdbodeis@gmail.com>
#-----------------------------------------------------------------------------------------------------------------------

# ======================================================================================================================
# Standard Imports
# ----------------------------------------------------------------------------------------------------------------------
import os
import cv2
import re
import numpy as np
from pdf2image import convert_from_path
from concurrent.futures import ProcessPoolExecutor as ppe
from itertools import repeat

# ======================================================================================================================
# OMR Class
# ----------------------------------------------------------------------------------------------------------------------
class OMR():
    """
    Optical Mark Recognition (OMR) \n
    The class is used in doing the heavy lifting for manipulating and collating the data. \n  
    It will convert pdf files to whatever file format you send, while defaulting to jpg. \n
    It makes seperate lists of keys and game sheets so they can be compared to one another to get the marked bubbles. \n
    """
    def __init__(self,
                 cpu_threads: int,
                 directories: list[str],
                 image_format: str = 'jpg',
                 save_image_overlay: bool = False,
                 mark_color: str = 'blue') -> None:
        """
        Everything as far as data collection and saving is ran in this guy. 

        Args:
            cpu_threads (int): Total CPU threads found and passed to it for converting the pdf files.
            directories (list[str]): All of the folders where the data can be retrieved and saved. 
            image_format (str, optional): The file type being saved from the pdf conversion.
                Defaults to 'jpg'.
            save_image_overlay (bool, optional): While processing the images, it can save a 'dot' on each of the spots it finds mark to be saved in 'results/'. 
                Defaults to False.
            mark_color (str, optional): You can use different colored pens or pencils for making the paper. Called with lower() so it matches the method call.
                Defaults to 'blue'.

        Raises:
            FileExistsError: If no keys were found in the folders. 
            FileExistsError: If no game sheets were found in the folders. 
        """

        # Class init values.
        self.cpu_threads: int = cpu_threads
        self.image_format: str = image_format
        self.save_image_overlay: bool = save_image_overlay
        self.mark_color: str = mark_color
        self.directories: list[str] = directories

        # Created within and used by the class. 
        self._keys_pdf_names: list[str]
        self._scantron_pdf_names: list[str]
        self._scantron_names: list[str]
        self._key_names: list[str]
        self._scanned_values: list[tuple] = []
        self._scanned_keys: list = []
        self._sorted_key_values: list = []
        self._scanned_keys_average: tuple
        self._key_column_index: tuple(int) = (0, 8, 18, 26, 31, 39, 60, 74, 80, 94, 110, 124, 130, 136, 142)
        self._total_key_values: int = 155
        self._bubble_location: dict = {
                                       # Column 1
                                       0: [(905, 2335), 'Auton HP TL'],
                                       1: [(903, 2497), 'Auton HP ML'],
                                       2: [(903, 2658), 'Auton HP LLCone'],
                                       3: [(903, 2818), 'Auton HP LLCube'],
                                       4: [(897, 3949), 'Tele HP TL'],
                                       5: [(896, 4110), 'Tele HP ML'],
                                       6: [(896, 4271), 'Tele HP LLCone'],
                                       7: [(896, 4433), 'Tele HP LLCube'],
                                       # Column 2
                                       8: [(1158, 1368), 'Blue Alliance'],
                                       9: [(1157, 1529), 'Red Alliance'],
                                       10: [(1154, 2336), 'Auton HP TM'],
                                       11: [(1154, 2497), 'Auton HP MM'],
                                       12: [(1153, 2658), 'Auton HP MLCone'],
                                       13: [(1153, 2819), 'Auton HP MLCube'],
                                       14: [(1147, 3949), 'Tele HP TM'],
                                       15: [(1146, 4111), 'Tele HP MM'],
                                       16: [(1146, 4272), 'Tele HP MLCone'],
                                       17: [(1145, 4433), 'Tele HP MLCube'],
                                       # Column 3
                                       18: [(1408, 2337), 'Auton HP TR'],
                                       19: [(1407, 2498), 'Auton HP MR'],
                                       20: [(1406, 2658), 'Auton HP LRCone'],
                                       21: [(1404, 2818), 'Auton HP LRCube'],
                                       22: [(1400, 3950), 'Tele HP TR'],
                                       23: [(1401, 4111), 'Tele HP MR'],
                                       24: [(1399, 4271), 'Tele HP LRCone'],
                                       25: [(1399, 4433), 'Tele HP LRCube'],
                                       # Column 4
                                       26: [(1651, 4918), 'Floor Yes'],
                                       27: [(1651, 5076), 'Single Sub Yes'],
                                       28: [(1650, 5234), 'Double Sub Slider Yes'],
                                       29: [(1650, 5393), 'Double Sub Chute Yes'],
                                       30: [(1648, 6353), 'Parked Yes'],
                                       # Column 5
                                       31: [(1913, 2338), 'Auton M TL'],
                                       32: [(1912, 2498), 'Auton M ML'],
                                       33: [(1912, 2660), 'Auton M LLCone'],
                                       34: [(1911, 2819), 'Auton M LLCube'],
                                       35: [(1906, 3950), 'Tele M TL'],
                                       36: [(1905, 4111), 'Tele M ML'],
                                       37: [(1905, 4272), 'Tele M LLCone'],
                                       38: [(1905, 4434), 'Tele M LLCube'],
                                       # Column 6
                                       39: [(2175, 405), 'Match Deca Zero'],
                                       40: [(2174, 569), 'Match Zero'],
                                       41: [(2172, 1053), 'Team Kilo Zero'],
                                       42: [(2170, 1211), 'Team Hecto Zero'],
                                       43: [(2169, 1370), 'Team Deca Zero'],
                                       44: [(2169, 1532), 'Team Zero'],
                                       45: [(2166, 2338), 'Auton M TM'],
                                       46: [(2165, 2499), 'Auton M MM'],
                                       47: [(2165, 2660), 'Auton M MLCone'],
                                       48: [(2164, 2820), 'Auton M MLCube'],
                                       49: [(2163, 3142), 'Auton Charge Station On'],
                                       50: [(2159, 3951), 'Tele M TM'],
                                       51: [(2158, 4112), 'Tele M MM'],
                                       52: [(2158, 4273), 'Tele M MLCone'],
                                       53: [(2158, 4435), 'Tele M MLCube'],
                                       54: [(2157, 4918), 'Floor No'],
                                       55: [(2156, 5076), 'Single Sub No'],
                                       56: [(2156, 5235), 'Double Sub Slider No'],
                                       57: [(2155, 5393), 'Parked No'],
                                       58: [(2154, 6031), 'End Game Charge Station On'],
                                       59: [(2152, 6353), 'Parked No'],
                                       # Column 7
                                       60: [(2425, 406), 'Match Deca One'],
                                       61: [(2425, 569), 'Match One'],
                                       62: [(2422, 1053), 'Team Kilo One'],
                                       63: [(2420, 1211), 'Team Hecto One'],
                                       64: [(2419, 1371), 'Team Deca One'],
                                       65: [(2419, 1532), 'Team One'],
                                       66: [(2416, 2339), 'Auton M TR'],
                                       67: [(2416, 2500), 'Auton M MR'],
                                       68: [(2415, 2661), 'Auton M LRCone'],
                                       69: [(2414, 2821), 'Auton M LRCube'],
                                       70: [(2409, 3951), 'Tele M TR'],
                                       71: [(2409, 4113), 'Tele M MR'],
                                       72: [(2409, 4274), 'Tele M LRCone'],
                                       73: [(2408, 4435), 'Tele M LRCube'],
                                       # Column 8
                                       74: [(2677, 406), 'Match Deca Two'],
                                       75: [(2675, 570), 'Match Two'],
                                       76: [(2673, 1054), 'Team Kilo Two'],
                                       77: [(2671, 1213), 'Team Hecto Two'],
                                       78: [(2671, 1372), 'Team Deca Two'],
                                       79: [(2671, 1533), 'Team Two'],
                                       # Column 9
                                       80: [(2927, 409), 'Match Deca Three'],
                                       81: [(2927, 573), 'Match Three'],
                                       82: [(2923, 1056), 'Team Kilo Three'],
                                       83: [(2922, 1214), 'Team Hecto Three'],
                                       84: [(2921, 1374), 'Team Deca Three'],
                                       85: [(2921, 1535), 'Team Three'],
                                       86: [(2918, 2341), 'Auton ST TL'],
                                       87: [(2916, 2503), 'Auton ST ML'],
                                       88: [(2916, 2664), 'Auton ST LLCone'],
                                       89: [(2915, 2824), 'Auton ST LLCube'],
                                       90: [(2910, 3954), 'Tele ST TL'],
                                       91: [(2910, 4114), 'Tele ST ML'],
                                       92: [(2909, 4275), 'Tele ST LLCone'],
                                       93: [(2909, 4437), 'Tele ST LLCube'],
                                       # Column 10
                                       94: [(3178, 410), 'Match Deca Four'],
                                       95: [(3178, 573), 'Match Four'],
                                       96: [(3175, 1057), 'Team Kilo Four'],
                                       97: [(3174, 1216), 'Team Hecto Four'],
                                       98: [(3173, 1375), 'Team Deca Four'],
                                       99: [(3173, 1536), 'Team Four'],
                                       100: [(3169, 2342), 'Auton ST TM'],
                                       101: [(3169, 2504), 'Auton ST MM'],
                                       102: [(3168, 2665), 'Auton ST MLCone'],
                                       103: [(3168, 2823), 'Auton ST MLCube'],
                                       104: [(3166, 3145), 'Auton Charge Station Balanced'],
                                       105: [(3163, 3955), 'Tele ST TM'],
                                       106: [(3162, 4115), 'Tele ST MM'],
                                       107: [(3161, 4276), 'Tele ST MLCone'],
                                       108: [(3161, 4439), 'Tele ST MLCube'],
                                       109: [(3156, 6034), 'End Game Charge Station Balanced'],
                                       # Column 11
                                       110: [(3431, 410), 'Match Deca Five'],
                                       111: [(3430, 574), 'Match Five'],
                                       112: [(3427, 1058), 'Team Kilo Five'],
                                       113: [(3426, 1217), 'Team Hecto Five'],
                                       114: [(3426, 1376), 'Team Deca Five'],
                                       115: [(3426, 1538), 'Team Five'],
                                       116: [(3422, 2343), 'Auton ST TR'],
                                       117: [(3422, 2505), 'Auton ST MR'],
                                       118: [(3421, 2665), 'Auton ST LRCone'],
                                       119: [(3420, 2825), 'Auton ST LRCube'],
                                       120: [(3415, 3955), 'Tele ST TR'],
                                       121: [(3415, 4116), 'Tele ST MR'],
                                       122: [(3415, 4277), 'Tele ST LRCone'],
                                       123: [(3415, 4438), 'Tele ST LRCube'],
                                       # Column 12
                                       124: [(3684, 412), 'Match Deca Six'],
                                       125: [(3683, 576), 'Match Six'],
                                       126: [(3680, 1060), 'Team Kilo Six'],
                                       127: [(3679, 1217), 'Team Hecto Six'],
                                       128: [(3679, 1377), 'Team Deca Six'],
                                       129: [(3678, 1538), 'Team Six'],
                                       # Column 13
                                       130: [(3937, 412), 'Match Deca Seven'],
                                       131: [(3936, 577), 'Match Seven'],
                                       132: [(3933, 1061), 'Team Kilo Seven'],
                                       133: [(3932, 1219), 'Team Hecto Seven'],
                                       134: [(3931, 1379), 'Team Deca Seven'],
                                       135: [(3931, 1539), 'Team Seven'],
                                       # Column 14
                                       136: [(4187, 414), 'Match Deca Eight'],
                                       137: [(4187, 577), 'Match Eight'],
                                       138: [(4184, 1061), 'Team Kilo Eight'],
                                       139: [(4182, 1220), 'Team Hecto Eight'],
                                       140: [(4182, 1379), 'Team Deca Eight'],
                                       141: [(4182, 1540), 'Team Eight'],
                                       # Column 15
                                       142: [(4438, 415), 'Match Deca Nine'],
                                       143: [(4437, 578), 'Match Nine'],
                                       144: [(4434, 1063), 'Team Kilo Nine'],
                                       145: [(4433, 1221), 'Team Hecto Nine'],
                                       146: [(4433, 1381), 'Team Deca Nine'],
                                       147: [(4433, 1541), 'Team Nine'],
                                       148: [(4429, 2346), 'Left Community Yes'],
                                       149: [(4428, 2508), 'Left Community No'],
                                       150: [(4425, 3150), 'Auton Charge Station Not Attempted'],
                                       151: [(4419, 4925), 'Travel Between HP and CS'],
                                       152: [(4418, 5082), 'Travel Over Charge'],
                                       153: [(4417, 5241), 'Travel Between ST and CS'],
                                       154: [(4414, 6037), 'End Game Charge Station Not Attempted']
                                       }

        # Initializing functions.
        # Checking for and converting pdf files if those are used instead of pictures.
        # First the keys. 
        if not os.listdir(self.directories[0]):
            print('No keys were found to convert from a pdf. Looking for {} image format.'.format(self.image_format))
        else:
            self._change_names(directory = self.directories[0],
                               data = 'Key',
                               file_type='.pdf')
            self._get_key_pdf_names()
            self._convert_pdf_to_image(pdf_directory = 0, 
                                       image_directory = 1,
                                       data = 'Key',
                                       pdf_names = self._keys_pdf_names)
        
        # Now the game sheets.
        if not os.listdir(self.directories[2]):
            print('No game sheets were found to convert from a pdf. Looking for {} image format.'.format(self.image_format))
        else:
            self._change_names(directory = self.directories[2],
                               data = 'Scantron',
                               file_type='.pdf')
            self._get_scantron_pdf_names()
            self._convert_pdf_to_image(pdf_directory = 2,
                                       image_directory = 3,
                                       data = 'Scantron',
                                       pdf_names = self._scantron_pdf_names)
        
        # Changing the name(s) of the key image(s)
        self._change_names(directory = self.directories[1],
                           data = 'Key',
                           file_type = '.' + self.image_format)
        
        # Changing the name(s) of the scantron image(s)
        self._change_names(directory = self.directories[3],
                           data = 'Scantron',
                           file_type = '.' + self.image_format)
        # Getting the names of the images to run the data. 
        self._get_key_image_names()
        self._get_scantron_image_names()
        if not self._key_names:
            # TODO Ask if the Constants._bubble_location should be used if none were found? 
            del self
            raise FileNotFoundError('No image(s) for key(s) to process were found.')
        if not self._scantron_names:
            del self
            raise FileNotFoundError('No image(s) for game sheets(s) to process were found.')
        
        # Getting the marks for the scantron key(s) that are entered and the actual game sheets. 
        with ppe(max_workers = cpu_threads) as executor:
            executor_keys = executor.map(self._process_images_executor,
                                         repeat(1),
                                         self._key_names,
                                         repeat('key'),
                                         repeat(self.mark_color),
                                         repeat(self.save_image_overlay))

        self._scanned_keys = tuple(executor_keys)

        # Getting the values from the game sheets. 
        with ppe(max_workers = cpu_threads) as executor:
            executor_scantron = executor.map(self._process_images_executor,
                                             repeat(3),
                                             self._scantron_names,
                                             repeat('scantron'),
                                             repeat(self.mark_color),
                                             repeat(self.save_image_overlay))

        self._scanned_values = tuple(executor_scantron)

        self._sort_key_values()
        if not self._sorted_key_values:
            del self
            raise IndexError('No keys of appropriate length were found.')
        self._get_key_average()
        self._update_scantron_bubbles()

# ======================================================================================================================
# Low Level Private Functions
# ----------------------------------------------------------------------------------------------------------------------
    def _get_key_pdf_names(self) -> None:
        """ Creating list of strings from the pdf files of keys. """
        self._keys_pdf_names = [i for i in os.listdir(self.directories[0]) if i.endswith('.pdf')]

#-----------------------------------------------------------------------------------------------------------------------
    def _get_key_image_names(self) -> None:
        """ Creating list of strings from the image files of keys. """
        self._key_names = [i for i in os.listdir(self.directories[1]) if (i.endswith('.' + self.image_format))]

#-----------------------------------------------------------------------------------------------------------------------
    def _get_scantron_pdf_names(self) -> None:
        """ Creating list of strings from the pdf files of game sheets. """
        self._scantron_pdf_names = [i for i in os.listdir(self.directories[2]) if i.endswith('.pdf')]

#-----------------------------------------------------------------------------------------------------------------------
    def _get_scantron_image_names(self) -> None:
        """ Creating list of strings from the image files of game sheets. """
        self._scantron_names = [i for i in os.listdir(self.directories[3]) if (i.endswith('.' + self.image_format))]

#-----------------------------------------------------------------------------------------------------------------------    
    def _change_names(self,
                      directory: str,
                      data: str,
                      file_type: str):
        """
        Going through the given directory and changing the names of the files for each of the ones it finds. \n
        enum_list is an iterable (nt.ScandirIterator) of all the files of the given type in that location. \n
        Those are then enumerated such that each name of them is a tuple with their given number (1, file_name). \n
        The files gets renamed as Key_1 or Scantron_1, and so on, depending on which is being checked. \n
        It can't save a file with the same name that already exists so its enum value is stepped by 1 until it can be saved.
        
        Args:
            directory (str): Folder where the files need to be changed. 
            data (str): Mostly for renaming and differentiating between keys and game sheets. 
            file_type (str): The file type that each  will be renamed. 
        """
        enum_list: list = [i for i in enumerate(os.scandir(directory), 1) if i[1].name.endswith(file_type)]
        for name in enum_list:
            offset: int = 1
            source = directory + name[1].name
            destination = directory + data + '_' + str(name[0]) + file_type
            while True:
                try:
                    os.rename(source, destination)
                except:
                    destination = directory + data + '_' + str(name[0] + offset) + file_type
                    offset += 1
                    continue
                break
#-----------------------------------------------------------------------------------------------------------------------    
    def _sub_name(self,
                  name: str) -> str:
        """
        CURRENTLY UNUSED. \n
        Taking a string and removing everything but alphanumerics, dashes, and underscores. \n

        Args:
            name (str): Name to be changed. 

        Returns:
            str: New name meeting the substitution criteria. 
        """
        return re.sub('[^0-9A-Za-z_-]', '', name)

#-----------------------------------------------------------------------------------------------------------------------
    def _convert_pdf_to_image(self,
                              pdf_directory: int,
                              image_directory: int,
                              data: str, 
                              pdf_names: list[str]) -> None:
        """
        Taking the various pdf files and converting them to an image of the specified file type from the class init. \n
        Outter loop is used for each pdf file that is found in the location. \n
        Inner loop is for each page within the pdf. \n

        Args:
            pdf_directory (int): Index for the list of folder names.
            image_directory (int): Index for the list of folder names.
            data (str): Whethere it is a key or scantron. 
            pdf_names (list[str]): Names of the files to be converted from pdf. 
        """
        for i in range(len(pdf_names)):  # Each pdf
        # for file in os.scandir(self.directories[pdf_directory]):
                images = convert_from_path(pdf_path = self.directories[pdf_directory] + pdf_names[i],
                # images = convert_from_path(pdf_path = self.directories[pdf_directory] + file.name,
                                           poppler_path = 'poppler/Library/bin',
                                           dpi = 700,
                                           thread_count = self.cpu_threads)

                for j in range(len(images)):  # Each page of the pdf
                    try:
                        location = self.directories[image_directory] + data + '_' + str(i+1) + '-' + str(j+1) + '.' + self.image_format
                        images[j].save(fp = location,
                                       bitmap_format = self.image_format)
                    except:
                        location = self.directories[image_directory] + data + '_' + str(i+1) + '-' + str(j+1) + '.jpg'
                        images[j].save(fp = location,
                                       bitmap_format = 'jpg')

#-----------------------------------------------------------------------------------------------------------------------
    def _sort_key_values(self) -> None:
        """
        Taking each of the keys and sorting them by their column and Y (ascending) values. \n
        OMR searches first by X then their Y pixel location so the order in the columns become mismatched. \n
        For example, the second tuple should be first as far as we are concerned, but it's X value is higher and moved further down. \n
            (10, 5) \n
            (11, 2) \n
        _bubble_location has each of them split off into their respective chunks and then get sorted that way.
        """
        temp_sorted_key_values: list = []
        for key in self._scanned_keys:  # Looping through each key.
            if len(key) != self._total_key_values:  # Making sure the key is the correct length. 
                continue
            temp_key_sorted = []
            for i in range(len(self._key_column_index)):  # Sorting out each 'column.'
                if i == (len(self._key_column_index) - 1):
                    temp_column = key[self._key_column_index[i]: (self._total_key_values + 1)]
                else:
                    temp_column = key[self._key_column_index[i]: self._key_column_index[i+1]]
                temp_key_sorted += sorted(temp_column, key = lambda x: x[1])  # Sorting the column.
            temp_sorted_key_values.append(temp_key_sorted)  # Adding the list of each key to the mega list.
        self._sorted_key_values = temp_sorted_key_values

#-----------------------------------------------------------------------------------------------------------------------
    def _get_key_average(self) -> None:
        """
        Taking all of the keys that were found and averaging their values together. \n
        Since they are going to be printed off and scanned, it will give a more realistic value versus creating it from filling in the blanks on a saved image. 
        """
        temp_key_average: list = []
        for i in range(self._total_key_values):  # Each of the possible mark locations 
            temp_x_sum, temp_y_sum, temp_x_average, temp_y_average = 0, 0, 0, 0
            for j in range(len(self._sorted_key_values)):  # Each of the keys and their identical spots. 
                temp_x_sum += self._sorted_key_values[j][i][0]
                temp_y_sum += self._sorted_key_values[j][i][1]
            temp_x_average = int(temp_x_sum / len(self._sorted_key_values))
            temp_y_average = int(temp_y_sum / len(self._sorted_key_values))
            temp_key_average.append(tuple((temp_x_average, temp_y_average)))
        self._scanned_keys_average = tuple(temp_key_average)

#-----------------------------------------------------------------------------------------------------------------------
    def _update_scantron_bubbles(self):
        """
        Taking the new values from _get_key_average() and updating the dict. \n
        These are to be used in Bubble_Sheet when it is passed to the game sheets to determine what was selected.
        """
        for key in self._bubble_location:
            self._bubble_location[key][0] = self._scanned_keys_average[key]

#-----------------------------------------------------------------------------------------------------------------------
    def _process_images_executor(self,
                                 image_directory: int,
                                 image_name: str,
                                 data: str,
                                 color: str,
                                 save_image_overlay: bool) -> tuple:
        """
        Method for gathering all of the spots where the paper is marked. \n
        Changed over to work with multithreading to help speed up the processing time. 

        Args:
            image_directory (int): Index for the list of folder names.
            image_names (list[str]): Names of the files to be read in and marked locations saved. 
            data (str): Where the image is a key or game sheet.
            color (str): The color range that the opencv tries to match.

        Returns:
            tuple: Tuple of tuples that contain the X and Y coordinates of every mark that was detected on the sheet.
        """
        try:
            omr_marks = []
            img = cv2.imread(self.directories[image_directory] + image_name)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Threshold for blue.
            if color == 'blue':
                lower_range = np.array([110,50,50])
                upper_range = np.array([130,255,255])
            # Threshold for green.
            # elif color == 'green':
            #     lower_range = np.array([36, 25, 25])
            #     upper_range = np.array([70, 255,255])
            # # Threshold for red.
            # elif color == 'red':
            #     lower_range = np.array([155,25,0])
            #     upper_range = np.array([179,255,255])
            # # Threshold for yellow.
            # elif color == 'yellow':
            #     lower_range = np.array([20,100,100])
            #     upper_range = np.array([30,255,255])
            else:
                lower_range = np.array([110,50,50])
                upper_range = np.array([130,255,255])

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
            if save_image_overlay:
                result = img.copy() 
            for contour in contours:
                M = cv2.moments(contour)
                if M["m00"] != 0:  # For divide by zero erros the popped up a few times. 
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                else:
                    continue
                pt = (cx,cy)
                omr_marks.append(pt)
                if self.save_image_overlay:
                    cv2.circle(result, (cx, cy), 25, (0, 255, 0), -1)
            if data == 'key' and save_image_overlay:
                omr_marks = tuple(sorted(omr_marks))
                cv2.imwrite(('results/' + 'key_overlay_' + image_name), result)
            elif data == 'key':
                omr_marks = tuple(sorted(omr_marks))
            elif data == 'scantron' and self.save_image_overlay:
                omr_marks = tuple(sorted(omr_marks))
                cv2.imwrite(('results/' + 'scantron_overlay_' + image_name), result)
            elif data == 'scantron':
                omr_marks = tuple(sorted(omr_marks))
        except Exception as ex:
            print('A problem occured with, ' + image_name)
            print(ex)
        return omr_marks

# ======================================================================================================================
# Public Functions
# ----------------------------------------------------------------------------------------------------------------------
    def get_key_values(self) -> dict:
        """
        Method for getting the key values. \n
        Returns:
            dict: Averaged values for the location of all the bubble locations on the scantron sheet.
        """
        return self._bubble_location

#-----------------------------------------------------------------------------------------------------------------------
    def get_game_sheet_values(self) -> list[tuple]:
        """
        Method for getting the game sheet values. \n
        Returns:
            list[tuple]: List of tuples containing the values for each of the game sheets that was read into it.
        """
        return self._scanned_values

# ======================================================================================================================
# Main
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    OMR()

# End of file.
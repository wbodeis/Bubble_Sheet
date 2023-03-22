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
# Custom Class Imports
# ----------------------------------------------------------------------------------------------------------------------
from Constants import Constants

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
        self._key_column_index: tuple(int) = Constants.KEY_COLUMN_INDEX
        self._total_key_values: int = Constants.TOTAL_KEY_VALUES
        self._bubble_location: dict = Constants.BUBBLE_LOCATION

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
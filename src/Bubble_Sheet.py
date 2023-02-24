#======================================================================================================================+
# FIle:  Bubble_Sheet/src/Bubble_Sheet.py
# Project: OMR Scantron for FRC Team 5712
# Author:  William Bodeis <wdbodeis@gmail.com>
#-----------------------------------------------------------------------------------------------------------------------

# ======================================================================================================================
# Standard Imports
# ----------------------------------------------------------------------------------------------------------------------
import os, pandas as pd, re, sys, multiprocessing
from datetime import datetime

# ======================================================================================================================
# Custom Class Imports
# ----------------------------------------------------------------------------------------------------------------------
from OMR import OMR
from Scantron import Scantron

class Bubble_Sheet():
    """
    Highest level class for running and acquiring the game data. 
    TODO Maybe get the arguments for OMR and Scantron as inputs for the init.
    """
    def __init__(self,
                 pixel_differential: int = 50) -> None:
        """_summary_

        Args:
            pixel_differential (int, optional): The plus or minus that it will look for a corresponding mark in the bubble_location dictionary.
                                                Defaults to 50.

        Raises:
            FileNotFoundError: Raised if the needed folders do NOT exist when running the program. 
        """

        self.pixel_differential = pixel_differential

        self._cpu_threads: int
        self._directories: list[str] = []
        self._directory_check: bool = False
        self._OMR_data: OMR
        self._bubble_location: dict = {}
        self._game_sheets: list = []
        self._processed_game_sheets: list[Scantron] = []
        self._game_sheet_data: list[dict] = []
        self._df: pd.DataFrame

        # Initializing methods.
        self._get_CPU_threads()
        self._create_directories_list()
        self._check_directories()
        if self._directory_check:
            del self
            raise FileNotFoundError('One or more of the required directories was not found. They were created so please double check and rerun the program.')

# ======================================================================================================================
# Public Functions
# ----------------------------------------------------------------------------------------------------------------------
    def main(self):
        """
        For running all the data processing. It invokes all of the classes and methods to then save the data as a csv.
        TODO Figure out the processing pool to multithread the processing. 
        TODO Nest try-excepts? They're all needed one after another, or maybe seperat method calls?
        """
        try:
            self._OMR_data = OMR(cpu_threads = self._cpu_threads,
                                 directories = self._directories,
                                 image_format = 'jpeg',
                                 save_image_overlay = False,
                                 mark_color = 'blue')
        except Exception as ex:
            print('An error occured:')
            print(ex)
            return None
        
        try:
            self._bubble_location = self._OMR_data.get_key_values()
            self._game_sheets = self._OMR_data.get_game_sheet_values()
        except Exception as ex:
            print('An error occured:')
            print(ex)
            return None
        
        for sheet in self._game_sheets:
            self._processed_game_sheets.append(Scantron(scantron_data = sheet,
                                                        bubble_location = self._bubble_location, 
                                                        pixel_differential = self.pixel_differential))
        for sheet in self._processed_game_sheets:
            self._game_sheet_data.append(sheet._get_raw_data())
        
        self._df = pd.DataFrame.from_dict(self._game_sheet_data)
        # print(self._df)
        self._save_file()
# ======================================================================================================================
# Low Level Private Functions
# ----------------------------------------------------------------------------------------------------------------------
    def _create_directories_list(self):
        """
        List of the folder locations used for reading and writing the data.
        Used as a method call to have a more visual appearance of what was needed by the program.
        """
        self._directories.append('key/')                # 0
        self._directories.append('key_images/')         # 1
        self._directories.append('scantron/')           # 2
        self._directories.append('scantron_images/')    # 3
        self._directories.append('results/')            # 4
        
#-----------------------------------------------------------------------------------------------------------------------
    def _check_directories(self) -> None:
        """
        Checking to make sure all of the required folders exist in the root location. 
        If it must create a folder, it changes the bool to False. 
        """
        for directory in self._directories:
            if not os.path.exists(directory):
                self._directory_check = True
                os.makedirs(directory)
#-----------------------------------------------------------------------------------------------------------------------
    def _get_CPU_threads(self):
        """ CPU Threads available on the current system. """
        try:
            self._cpu_threads = os.cpu_count()
        except:
            self._cpu_threads = 1

#-----------------------------------------------------------------------------------------------------------------------
    def _save_file(self):
        """ Saving the data as a csv with a the current time as it's name so nothing saves over previous datasets. """
        time_now: datetime = datetime.now()
        file_name: str = re.sub('-|:|\.|\s', '_', str(time_now)) + '.csv'
        path: str = 'results/' + file_name
        self._df.to_csv(path_or_buf = path,
                        index = False)
#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    if sys.platform.startswith('win'):
        # On Windows calling this function is necessary.
        multiprocessing.freeze_support()
    Bubble_Sheet().main()
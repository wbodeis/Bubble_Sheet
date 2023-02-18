#======================================================================================================================+
# FIle:  Bubble_Sheet/src/Bubble_Sheet.py
# Project: OMR Scanrtron for FRC Team 5712
# Author:  William Bodeis <wdbodeis@gmail.com>
#-----------------------------------------------------------------------------------------------------------------------
import os, pandas as pd
from OMR import OMR
from Scantron import Scantron

class Bubble_Sheet():
    def __init__(self,
                 pixel_differential: int = 50) -> None:
                 
        self.pixel_differential = pixel_differential
        self._cpu_threads: int
        self._total_data: OMR
        self._key_values: dict
        self._game_sheets: list
        self._processed_game_sheets: list[Scantron] = []
        self._game_sheet_data: list[dict] = []
        self._df: pd.DataFrame = pd.DataFrame

        # Initializing methods.
        self._get_CPU_threads()

#-----------------------------------------------------------------------------------------------------------------------
    def main(self):
        self._total_data = OMR(cpu_threads = self._cpu_threads)
        self._key_values = self._total_data.get_key_values()
        self._game_sheets = self._total_data.get_scantron_values()

        # TODO Figure out the processing pool to multithread the processing. 
        for i in range(len(self._game_sheets)):
            self._processed_game_sheets.append(Scantron(scantron_data = self._game_sheets[i],
                                                        bubble_location = self._key_values, 
                                                        pixel_differential = self.pixel_differential)
            )
        for sheet in self._processed_game_sheets:
            self._game_sheet_data.append(sheet._get_raw_data())
        
        self._df = pd.DataFrame(self._game_sheet_data)
        print(self._df)
        # print(self._game_sheets[1])
        # print(self._processed_game_sheets[1]._raw_data['u'])

#-----------------------------------------------------------------------------------------------------------------------
    def _get_CPU_threads(self):
        try:
            self._cpu_threads = os.cpu_count()
        except:
            self._cpu_threads = 1

#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    Bubble_Sheet().main()
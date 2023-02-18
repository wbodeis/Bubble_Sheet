#======================================================================================================================+
# FIle:  Bubble_Sheet/src/Bubble_Sheet.py
# Project: OMR Scanrtron for FRC Team 5712
# Author:  William Bodeis <wdbodeis@gmail.com>
#-----------------------------------------------------------------------------------------------------------------------
import os
from OMR import OMR
from Scantron import Scantron

class Bubble_Sheet():
    def __init__(self,
                 pixel_differential: int = 30) -> None:
        self._cpu_threads: int
        self._total_data: OMR
        self._key_values: dict
        self._game_sheets: list
        self._get_CPU_threads()

#-----------------------------------------------------------------------------------------------------------------------
    def main(self):
        self._total_data = OMR(cpu_threads = self._cpu_threads)
        self._key_values = self._total_data.get_key_values()
        self._game_sheets = self._total_data.get_scantron_values()

#-----------------------------------------------------------------------------------------------------------------------
    def _get_CPU_threads(self):
        try:
            self._cpu_threads = os.cpu_count()
        except:
            self._cpu_threads = 1

#-----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    Bubble_Sheet()
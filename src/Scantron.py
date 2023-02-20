#======================================================================================================================+
# FIle:  Bubble_Sheet/src/Scantron.py
# Project: OMR Scantron for FRC Team 5712
# Author:  William Bodeis <wdbodeis@gmail.com>
#-----------------------------------------------------------------------------------------------------------------------

class Scantron():
    """
    Class for creating an object of each game sheet scanned.
    The various methods were broken out in attempt to make it more readable, while it could have just been one large one with a bunch of nested if statements.
    Everything is determined against the pixel location of the averaged key value(s) that are gathered so the X and Y values fit with the given range of pixel_differential value. 
    Everything is stored in the object and returned using _get_raw_data().
    """
    def __init__(self,
                 scantron_data: tuple,
                 bubble_location: dict,
                 pixel_differential: int) -> None:
        """_summary_

        Args:
            scantron_data (tuple): The data of the specific key or game sheet that the OMR class determined. 
            bubble_location (dict): The location of every bubble from the key(s).
            pixel_differential (int): The plus or minus that it will look for a corresponding mark in the bubble_location dictionary.  
        """

        # Class init values. 
        self.scantron_data = scantron_data
        self.bubble_location = bubble_location
        self.pixel_differential = pixel_differential

        # Dictionaries for storing the various results. 
        self._raw_data: dict = {
                                'Team': [0, 0],
                                'Match': [1, 0],
                                'Alliance': [2, 0],
                                'Auton HP TL': [3, 0],
                                'Auton HP ML': [4, 0],
                                'Auton HP LLCube': [5, 0],
                                'Auton HP LLCone': [6, 0],
                                'Auton HP TM': [7, 0],
                                'Auton HP MM': [8, 0],
                                'Auton HP MLCube': [9, 0],
                                'Auton HP MLCone': [10, 0],
                                'Auton HP TR': [11, 0],
                                'Auton HP MR': [12, 0],
                                'Auton HP LRCube': [13, 0],
                                'Auton HP LRCone': [14, 0],
                                'Auton M TL': [15, 0],
                                'Auton M ML': [16, 0],
                                'Auton M LLCube': [17, 0],
                                'Auton M LLCone': [18, 0],
                                'Auton M TM': [19, 0],
                                'Auton M MM': [20, 0],
                                'Auton M MLCube': [21, 0],
                                'Auton M MLCone': [22, 0],
                                'Auton M TR': [23, 0],
                                'Auton M MR': [24, 0],
                                'Auton M LRCube': [25, 0],
                                'Auton M LRCone': [26, 0],
                                'Auton ST TL': [27, 0],
                                'Auton ST ML': [28, 0],
                                'Auton ST LLCube': [29, 0],
                                'Auton ST LLCone': [30, 0],
                                'Auton ST TM': [31, 0],
                                'Auton ST MM': [32, 0],
                                'Auton ST MLCube': [33, 0],
                                'Auton ST MLCone': [34, 0],
                                'Auton ST TR': [35, 0],
                                'Auton ST MR': [36, 0],
                                'Auton ST LRCube': [37, 0],
                                'Auton ST LRCone': [38, 0],
                                'Tele HP TL': [39, 0],
                                'Tele HP ML': [40, 0],
                                'Tele HP LLCube': [41, 0],
                                'Tele HP LLCone': [42, 0],
                                'Tele HP TM': [43, 0],
                                'Tele HP MM': [44, 0],
                                'Tele HP MLCube': [45, 0],
                                'Tele HP MLCone': [46, 0],
                                'Tele HP TR': [47, 0],
                                'Tele HP MR': [48, 0],
                                'Tele HP LRCube': [49, 0],
                                'Tele HP LRCone': [50, 0],
                                'Tele M TL': [51, 0],
                                'Tele M ML': [52, 0],
                                'Tele M LLCube': [53, 0],
                                'Tele M LLCone': [54, 0],
                                'Tele M TM': [55, 0],
                                'Tele M MM': [56, 0],
                                'Tele M MLCube': [57, 0],
                                'Tele M MLCone': [58, 0],
                                'Tele M TR': [59, 0],
                                'Tele M MR': [60, 0],
                                'Tele M LRCube': [61, 0],
                                'Tele M LRCone': [62, 0],
                                'Tele ST TL': [63, 0],
                                'Tele ST ML': [64, 0],
                                'Tele ST LLCube': [65, 0],
                                'Tele ST LLCone': [66, 0],
                                'Tele ST TM': [67, 0],
                                'Tele ST MM': [68, 0],
                                'Tele ST MLCube': [69, 0],
                                'Tele ST MLCone': [70, 0],
                                'Tele ST TR': [71, 0],
                                'Tele ST MR': [72, 0],
                                'Tele ST LRCube': [73, 0],
                                'Tele ST LRCone': [74, 0],
                                'Community': [75, 0],
                                'Auton Charge Station': [76, 0],
                                'Floor': [77, 0],
                                'Single Sub': [78, 0],
                                'Slider': [79, 0],
                                'Chute': [80, 0],
                                'HP & CS': [81, 0],
                                'Over Charge': [82, 0],
                                'ST & CS': [83, 0],
                                'Tele Charge Station': [84, 0],
                                'Parked': [85, 0]
                                }
        self._team_number_location: dict = {
                                            41: [0, 0],
                                            42: [0, 1],
                                            43: [0, 2],
                                            44: [0, 3],
                                            62: [1, 0],
                                            63: [1, 1],
                                            64: [1, 2],
                                            65: [1, 3],
                                            76: [2, 0],
                                            77: [2, 1],
                                            78: [2, 2],
                                            79: [2, 3],
                                            82: [3, 0],
                                            83: [3, 1],
                                            84: [3, 2],
                                            85: [3, 3],
                                            96: [4, 0],
                                            97: [4, 1],
                                            98: [4, 2],
                                            99: [4, 3],
                                            112: [5, 0],
                                            113: [5, 1],
                                            114: [5, 2],
                                            115: [5, 3],
                                            126: [6, 0],
                                            127: [6, 1],
                                            128: [6, 2],
                                            129: [6, 3],
                                            132: [7, 0],
                                            133: [7, 1],
                                            134: [7, 2],
                                            135: [7, 3],
                                            138: [8, 0],
                                            139: [8, 1],
                                            140: [8, 2],
                                            141: [8, 3],
                                            144: [9, 0],
                                            145: [9, 1],
                                            146: [9, 2],
                                            147: [9, 3],
                                            }
        self._match_number_location: dict = {
                                            39: [0, 0],
                                            40: [0, 1],
                                            60: [1, 0],
                                            61: [1, 1],
                                            74: [2, 0],
                                            75: [2, 1],
                                            80: [3, 0],
                                            81: [3, 1],
                                            94: [4, 0],
                                            95: [4, 1],
                                            110: [5, 0],
                                            111: [5, 1],
                                            124: [6, 0],
                                            125: [6, 1],
                                            130: [7, 0],
                                            131: [7, 1],
                                            136: [8, 0],
                                            137: [8, 1],
                                            142: [9, 0],
                                            143: [9, 1],
                                            }
        self._alliance_location: dict = {
                                        8: [0],
                                        9: [1],
                                        }
        self._game_results_locations: dict = {
                                            0: 'Auton HP TL',
                                            1: 'Auton HP ML',
                                            2: 'Auton HP LLCone',
                                            3: 'Auton HP LLCube',
                                            4: 'Tele HP TL',
                                            5: 'Tele HP ML',
                                            6: 'Tele HP LLCone',
                                            7: 'Tele HP LLCube',
                                            10: 'Auton HP TM',
                                            11: 'Auton HP MM',
                                            12: 'Auton HP MLCone',
                                            13: 'Auton HP MLCube',
                                            14: 'Tele HP TM',
                                            15: 'Tele HP MM',
                                            16: 'Tele HP MLCone',
                                            17: 'Tele HP MLCube',
                                            18: 'Auton HP TR',
                                            19: 'Auton HP MR',
                                            20: 'Auton HP LRCone',
                                            21: 'Auton HP LRCube',
                                            22: 'Tele HP TR',
                                            23: 'Tele HP MR',
                                            24: 'Tele HP LRCone',
                                            25: 'Tele HP LRCube',
                                            31: 'Auton M TL',
                                            32: 'Auton M ML',
                                            33: 'Auton M LLCone',
                                            34: 'Auton M LLCube',
                                            35: 'Tele M TL',
                                            36: 'Tele M ML',
                                            37: 'Tele M LLCone',
                                            38: 'Tele M LLCube',
                                            45: 'Auton M TM',
                                            46: 'Auton M MM',
                                            47: 'Auton M MLCone',
                                            48: 'Auton M MLCube',
                                            50: 'Tele M TM',
                                            51: 'Tele M MM',
                                            52: 'Tele M MLCone',
                                            53: 'Tele M MLCube',
                                            66: 'Auton M TR',
                                            67: 'Auton M MR',
                                            68: 'Auton M LRCone',
                                            69: 'Auton M LRCube',
                                            70: 'Tele M TR',
                                            71: 'Tele M MR',
                                            72: 'Tele M LRCone',
                                            73: 'Tele M LRCube',
                                            86: 'Auton ST TL',
                                            87: 'Auton ST ML',
                                            88: 'Auton ST LLCone',
                                            89: 'Auton ST LLCube',
                                            90: 'Tele ST TL',
                                            91: 'Tele ST ML',
                                            92: 'Tele ST LLCone',
                                            93: 'Tele ST LLCube',
                                            100: 'Auton ST TM',
                                            101: 'Auton ST MM',
                                            102: 'Auton ST MLCone',
                                            103: 'Auton ST MLCube',
                                            105: 'Tele ST TM',
                                            106: 'Tele ST MM',
                                            107: 'Tele ST MLCone',
                                            108: 'Tele ST MLCube',
                                            116: 'Auton ST TR',
                                            117: 'Auton ST MR',
                                            118: 'Auton ST LRCone',
                                            119: 'Auton ST LRCube',
                                            120: 'Tele ST TR',
                                            121: 'Tele ST MR',
                                            122: 'Tele ST LRCone',
                                            123: 'Tele ST LRCube'
                                            }
        self._play_style_location: dict = {
                                26: 'Floor Yes',
                                27: 'Single Sub Yes',
                                28: 'Double Sub Slider Yes',
                                29: 'Double Sub Chute Yes',
                                30: 'Parked Yes',
                                49: 'Auton Charge Station On',
                                54: 'Floor No',
                                55: 'Single Sub No',
                                56: 'Double Sub Slider No',
                                57: 'Parked No',
                                58: 'End Game Charge Station On',
                                59: 'Parked No',
                                104: 'Auton Charge Station Balanced',
                                109: 'End Game Charge Station Balanced',
                                148: 'Left Community Yes',
                                149: 'Left Community No',
                                150: 'Auton Charge Station Not Attempted',
                                151: 'Travel Between HP and CS',
                                152: 'Travel Over Charge',
                                153: 'Travel Between ST and CS',
                                154: 'End Game Charge Station Not Attempted'
                                }

        # Function calls to collate the data.
        self._determine_team_number()
        self._determine_match_numbner()
        self._determine_alliance()
        self._determine_game_results()
        self._determine_play_style()

#-----------------------------------------------------------------------------------------------------------------------
    def _determine_team_number(self) -> None:
        """ 
        Determinging the team's number. 
        Defaults to 0000 if nothing was entered or detected. 
        """
        temp_team_number: list = [0,0,0,0]
        count: int = 0
        for i in range(len(self.scantron_data)):
            temp_x_upper = self.scantron_data[i][0] + self.pixel_differential
            temp_x_lower = self.scantron_data[i][0] - self.pixel_differential
            temp_y_upper = self.scantron_data[i][1] + self.pixel_differential
            temp_y_lower = self.scantron_data[i][1] - self.pixel_differential

            for key, value in self.bubble_location.items():
                temp_key_x = value[0][0]
                temp_key_y = value[0][1]

                if ((temp_key_x <= temp_x_upper  
                    and temp_key_x >= temp_x_lower
                    and temp_key_y <= temp_y_upper
                    and temp_key_y >= temp_y_lower)
                    and key in self._team_number_location):

                        temp_team_number[self._team_number_location[key][1]] = self._team_number_location[key][0]
                        count += 1
                        continue
            if count == 4:
                break
        self._raw_data['Team'][1] = ''.join(str(e) for e in temp_team_number)

#-----------------------------------------------------------------------------------------------------------------------
    def _determine_match_numbner(self) -> None:
        """ 
        Determinging the match the team played in. 
        Defaults to 00 if nothing was entered or detected. 
        """
        temp_match_number: list = [0,0]
        count: int = 0
        for i in range(len(self.scantron_data)):
            temp_x_upper = self.scantron_data[i][0] + self.pixel_differential
            temp_x_lower = self.scantron_data[i][0] - self.pixel_differential
            temp_y_upper = self.scantron_data[i][1] + self.pixel_differential
            temp_y_lower = self.scantron_data[i][1] - self.pixel_differential

            for key, value in self.bubble_location.items():
                temp_key_x = value[0][0]
                temp_key_y = value[0][1]

                if ((temp_key_x <= temp_x_upper  
                     and  temp_key_x >= temp_x_lower
                     and temp_key_y <= temp_y_upper
                     and temp_key_y >= temp_y_lower)
                     and key in self._match_number_location):

                        temp_match_number[self._match_number_location[key][1]] = self._match_number_location[key][0]
                        count += 1
                        continue
            if count == 2:
                break
        self._raw_data['Match'][1] = ''.join(str(e) for e in temp_match_number)

#-----------------------------------------------------------------------------------------------------------------------
    def _determine_alliance(self) -> None:
        """ Red or Blue alliance. """
        for i in range(len(self.scantron_data)):
            temp_x_upper = self.scantron_data[i][0] + self.pixel_differential
            temp_x_lower = self.scantron_data[i][0] - self.pixel_differential
            temp_y_upper = self.scantron_data[i][1] + self.pixel_differential
            temp_y_lower = self.scantron_data[i][1] - self.pixel_differential

            for key, value in self.bubble_location.items():
                temp_key_x = value[0][0]
                temp_key_y = value[0][1]

                if ((temp_key_x <= temp_x_upper  
                     and  temp_key_x >= temp_x_lower
                     and temp_key_y <= temp_y_upper
                     and temp_key_y >= temp_y_lower)
                     and key in self._alliance_location):

                     if key == 8:
                        self._raw_data['Alliance'][1] = 0
                        return

                     elif key == 9:
                        self._raw_data['Alliance'][1] = 1
                        return

#-----------------------------------------------------------------------------------------------------------------------
    def _determine_game_results(self) -> None:
        """
        The majority of the work is done in here for getting the results of where the team played their cones and cubes. 
        """
        for i in range(len(self.scantron_data)):
            temp_x_upper = self.scantron_data[i][0] + self.pixel_differential
            temp_x_lower = self.scantron_data[i][0] - self.pixel_differential
            temp_y_upper = self.scantron_data[i][1] + self.pixel_differential
            temp_y_lower = self.scantron_data[i][1] - self.pixel_differential

            for key, value in self.bubble_location.items():
                temp_key_x = value[0][0]
                temp_key_y = value[0][1]

                if ((temp_key_x <= temp_x_upper  
                     and  temp_key_x >= temp_x_lower
                     and temp_key_y <= temp_y_upper
                     and temp_key_y >= temp_y_lower)
                     and key in self._game_results_locations):
                        self._raw_data[self._game_results_locations[key]][1] = 1

#-----------------------------------------------------------------------------------------------------------------------
    def _determine_play_style(self) -> None:
        """
        For the last of the sundried pertaining to the game itself. 
        Set as a bunch of ifs to make sure it works. 
        TODO Change later once it is known to be working correctly. 
        """
        for i in range(len(self.scantron_data)):
            temp_x_upper = self.scantron_data[i][0] + self.pixel_differential
            temp_x_lower = self.scantron_data[i][0] - self.pixel_differential
            temp_y_upper = self.scantron_data[i][1] + self.pixel_differential
            temp_y_lower = self.scantron_data[i][1] - self.pixel_differential

            for key, value in self.bubble_location.items():
                temp_key_x = value[0][0]
                temp_key_y = value[0][1]

                if ((temp_key_x <= temp_x_upper  
                     and  temp_key_x >= temp_x_lower
                     and temp_key_y <= temp_y_upper
                     and temp_key_y >= temp_y_lower)
                     and key in self._play_style_location):
                        if key == 26:
                            self._raw_data['Floor'][1] = 1
                        elif key == 27:
                            self._raw_data['Single Sub'][1] = 1
                        elif key == 28:
                            self._raw_data['Single Sub'][1] = 1
                        elif key == 29:
                            self._raw_data['Chute'][1] = 1
                        elif key == 30:
                            self._raw_data['Parked'][1] = 0
                        elif key == 49:
                            self._raw_data['Auton Charge Station'][1] = 0
                        elif key == 54:
                            self._raw_data['Floor'][1] = 0
                        elif key == 55:
                            self._raw_data['Single Sub'][1] = 0
                        elif key == 56:
                            self._raw_data['Single Sub'][1] = 0
                        elif key == 57:
                            self._raw_data['Chute'][1] = 0
                        elif key == 58:
                            self._raw_data['Tele Charge Station'][1] = 0
                        elif key == 59:
                            self._raw_data['Parked'][1] = 1
                        elif key == 104:
                            self._raw_data['Auton Charge Station'][1] = 1
                        elif key == 109:
                            self._raw_data['Tele Charge Station'][1] = 1
                        elif key == 148:
                            self._raw_data['Community'][1] = 1
                        elif key == 149:
                            self._raw_data['Community'][1] = 0
                        elif key == 150:
                            self._raw_data['Auton Charge Station'][1] = 2
                        elif key == 154:
                            self._raw_data['Tele Charge Station'][1] = 2

#-----------------------------------------------------------------------------------------------------------------------
    def _get_raw_data(self) -> dict:
        """ 
        Taking the key and true value of the key. The first value is it's place in the google sheet in case the dict starts to get sorted for some reason, so there will be a way to know their positions. 
        
        Returns:
            dict: Data that was collected and collated for each game sheet. 
                  Each key should correlate directly the column in the raw data section of the gooogle sheet. 
        """
        temp_raw_data: dict = {}
        for key, values in self._raw_data.items():
            try:
                temp_raw_data[key] = values[1]
            except Exception as ex:
                print(ex)
        return temp_raw_data
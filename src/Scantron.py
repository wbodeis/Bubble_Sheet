#======================================================================================================================+
# FIle:  Bubble_Sheet/src/Scantron.py
# Project: OMR Scanrtron for FRC Team 5712
# Author:  William Bodeis <wdbodeis@gmail.com>
#-----------------------------------------------------------------------------------------------------------------------

class Scantron():
    def __init__(self,
                 scantron_data: tuple,
                 bubble_location: dict,
                 pixel_differential: int) -> None:

        self._scantron_data = scantron_data
        self._bubble_location = bubble_location
        self.pixel_differential = pixel_differential

        # 
        self._raw_data: dict = {
                                'Team': [0, 0],
                                'Match': [1, 0],
                                'Alliance': [2, 0],
                                'Auton HP TL': [3, 0],
                                'Auton HP ML': [4, 0],
                                'Auton HP LLCube': [5, 0],
                                'Auton HP LLCone': [6, 0],
                                'Auton HP TM ': [7, 0],
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
                                'Auton M TM ': [19, 0],
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
                                'Auton ST TM ': [31, 0],
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
                                'Tele HP TM ': [43, 0],
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
                                'Tele M TM ': [55, 0],
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
                                'Tele ST TM ': [67, 0],
                                'Tele ST MM': [68, 0],
                                'Tele ST MLCube': [69, 0],
                                'Tele ST MLCone': [70, 0],
                                'Tele ST TR': [71, 0],
                                'Tele ST MR': [72, 0],
                                'Tele ST LRCube': [73, 0],
                                'Tele ST LRCone': [74, 0],
                                'Community': [75, 0],
                                'Charge Station': [76, 0],
                                'Floor': [77, 0],
                                'Single Sub': [78, 0],
                                'Slider': [79, 0],
                                'Chute': [80, 0],
                                'HP & CS': [81, 0],
                                'Over Charge': [82, 0],
                                'ST & CS': [83, 0],
                                'Charge Station': [84, 0],
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

#-----------------------------------------------------------------------------------------------------------------------
    def _determine_team_number(self):
        temp_team_name: list = [0,0,0,0]
        count: int = 0
        for i in range(len(self._scantron_data)):
            temp_x_upper = self._scantron_data[i][0] + self.pixel_differential
            temp_x_lower = self._scantron_data[i][0] - self.pixel_differential
            temp_y_upper = self._scantron_data[i][1] + self.pixel_differential
            temp_y_lower = self._scantron_data[i][1] - self.pixel_differential
            
            for j in range(len(self._bubble_location)):
                temp_key_x = self._bubble_location[j][0][0]
                temp_key_y = self._bubble_location[j][0][1]

                if ((temp_key_x <= temp_x_upper  
                    and temp_key_x >= temp_x_lower
                    and temp_key_y <= temp_y_upper
                    and temp_key_y >= temp_y_lower)
                    and j in self._team_number_location):
                        temp_team_name[self._team_number_location[j][1]] = self._team_number_location[j][0]
                        continue
            if count == 4:
                break
        self._raw_data['Team'][1] = ''.join(str(e) for e in temp_team_name)

#-----------------------------------------------------------------------------------------------------------------------
    def _determine_match_numbner(self):
        temp_match: list = [0,0]
        count: int = 0
        for i in range(len(self._scantron_data)):
            temp_x_upper = self._scantron_data[i][0] + self.pixel_differential
            temp_x_lower = self._scantron_data[i][0] - self.pixel_differential
            temp_y_upper = self._scantron_data[i][1] + self.pixel_differential
            temp_y_lower = self._scantron_data[i][1] - self.pixel_differential

            for j in range(len(self._bubble_location)):
                temp_key_x = self._bubble_location[j][0][0]
                temp_key_y = self._bubble_location[j][0][1]

                if ((temp_key_x <= temp_x_upper  
                     and  temp_key_x >= temp_x_lower
                     and temp_key_y <= temp_y_upper
                     and temp_key_y >= temp_y_lower)
                     and j in self._match_number_location):
                        temp_match[self._match_number_location[j][1]] = self._match_number_location[j][0]
                        count += 1
                        continue
            if count == 2:
                break
        self._raw_data['Match'][1] = ''.join(str(e) for e in temp_match)

#-----------------------------------------------------------------------------------------------------------------------
    def _determine_alliance(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------
    def _determine_game_results(self):
        pass
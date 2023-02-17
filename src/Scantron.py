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
                                'HP TL': [3, 0],
                                'HP ML': [4, 0],
                                'HP LLCube': [5, 0],
                                'HP LLCone': [6, 0],
                                'HP TM ': [7, 0],
                                'HP MM': [8, 0],
                                'HP MLCube': [9, 0],
                                'HP MLCone': [10, 0],
                                'HP TR': [11, 0],
                                'HP MR': [12, 0],
                                'HP LRCube': [13, 0],
                                'HP LRCone': [14, 0],
                                'M TL': [15, 0],
                                'M ML': [16, 0],
                                'M LLCube': [17, 0],
                                'M LLCone': [18, 0],
                                'M TM ': [19, 0],
                                'M MM': [20, 0],
                                'M MLCube': [21, 0],
                                'M MLCone': [22, 0],
                                'M TR': [23, 0],
                                'M MR': [24, 0],
                                'M LRCube': [25, 0],
                                'M LRCone': [26, 0],
                                'ST TL': [27, 0],
                                'ST ML': [28, 0],
                                'ST LLCube': [29, 0],
                                'ST LLCone': [30, 0],
                                'ST TM ': [31, 0],
                                'ST MM': [32, 0],
                                'ST MLCube': [33, 0],
                                'ST MLCone': [34, 0],
                                'ST TR': [35, 0],
                                'ST MR': [36, 0],
                                'ST LRCube': [37, 0],
                                'ST LRCone': [38, 0],
                                'HP TL': [39, 0],
                                'HP ML': [40, 0],
                                'HP LLCube': [41, 0],
                                'HP LLCone': [42, 0],
                                'HP TM ': [43, 0],
                                'HP MM': [44, 0],
                                'HP MLCube': [45, 0],
                                'HP MLCone': [46, 0],
                                'HP TR': [47, 0],
                                'HP MR': [48, 0],
                                'HP LRCube': [49, 0],
                                'HP LRCone': [50, 0],
                                'M TL': [51, 0],
                                'M ML': [52, 0],
                                'M LLCube': [53, 0],
                                'M LLCone': [54, 0],
                                'M TM ': [55, 0],
                                'M MM': [56, 0],
                                'M MLCube': [57, 0],
                                'M MLCone': [58, 0],
                                'M TR': [59, 0],
                                'M MR': [60, 0],
                                'M LRCube': [61, 0],
                                'M LRCone': [62, 0],
                                'ST TL': [63, 0],
                                'ST ML': [64, 0],
                                'ST LLCube': [65, 0],
                                'ST LLCone': [66, 0],
                                'ST TM ': [67, 0],
                                'ST MM': [68, 0],
                                'ST MLCube': [69, 0],
                                'ST MLCone': [70, 0],
                                'ST TR': [71, 0],
                                'ST MR': [72, 0],
                                'ST LRCube': [73, 0],
                                'ST LRCone': [74, 0],
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

        for i in range(len(self._scantron_data)):
            temp_x_upper = self._scantron_data[i][0] + self.pixel_differential
            temp_x_lower = self._scantron_data[i][0] - self.pixel_differential
            temp_y_upper = self._scantron_data[i][1] + self.pixel_differential
            temp_y_lower = self._scantron_data[i][1] - self.pixel_differential
            
            for j in range(len(self._bubble_location)):
                temp_key_x = self._bubble_location[j][0][0]
                temp_key_y = self._bubble_location[j][0][1]

                if (temp_key_x <= temp_x_upper  
                    and  temp_key_x >= temp_x_lower
                    and temp_key_y <= temp_y_upper
                    and temp_key_y >= temp_y_lower):
                    temp_team_name[self._team_number_location[j][1]] = self._team_number_location[j][0]
                    continue
        self._raw_data['Team'][1] = ''.join(str(e) for e in temp_team_name)

#-----------------------------------------------------------------------------------------------------------------------
    def _determine_match_numbner(self):
        temp_match: list = [0,0]

        for i in range(len(self._scantron_data)):
            temp_x_upper = self._scantron_data[i][0] + self.pixel_differential
            temp_x_lower = self._scantron_data[i][0] - self.pixel_differential
            temp_y_upper = self._scantron_data[i][1] + self.pixel_differential
            temp_y_lower = self._scantron_data[i][1] - self.pixel_differential

            for j in range(len(self._bubble_location)):
                temp_key_x = self._bubble_location[j][0][0]
                temp_key_y = self._bubble_location[j][0][1]

                if (temp_key_x <= temp_x_upper  
                        and  temp_key_x >= temp_x_lower
                        and temp_key_y <= temp_y_upper
                        and temp_key_y >= temp_y_lower):
                        temp_team_name[self._team_number_location[j][1]] = self._team_number_location[j][0]
                        continue

        self._raw_data['Match'][1] = ''.join(str(e) for e in temp_match)

#-----------------------------------------------------------------------------------------------------------------------
    def _determine_alliance(self):
        pass

#-----------------------------------------------------------------------------------------------------------------------
    def _determine_game_results(self):
        pass
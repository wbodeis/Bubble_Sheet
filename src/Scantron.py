#======================================================================================================================+
# FIle:  Bubble_Sheet/src/Scantron.py
# Project: OMR Scantron for FRC Team 5712
# Author:  William Bodeis <wdbodeis@gmail.com>
#-----------------------------------------------------------------------------------------------------------------------

# ======================================================================================================================
# Custom Class Imports
# ----------------------------------------------------------------------------------------------------------------------
from Constants import Constants

class Scantron():
    """
    Class for creating an object of each game sheet scanned. \n
    The various methods were broken out in attempt to make it more readable, while it could have just been one large one with a bunch of nested if statements. \n
    Everything is determined against the pixel location of the averaged key value(s) that are gathered so the X and Y values fit with the given range of pixel_differential value. \n
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
        self._raw_data: dict = Constants.RAW_DATA
        self._team_number_location: dict = Constants.TEAM_NUMBER_LOCATION
        self._match_number_location: dict = Constants.MATCH_NUMBER_LOCATION
        self._alliance_location: dict = Constants.ALLIANCE_LOCATION
        self._game_red_results_locations: dict = Constants.GAME_RED_RESULTS_LOCATIONS
        self._game_blue_results_locations: dict = Constants.GAME_BLUE_RESULTS_LOCATIONS
        self._play_style_location: dict = Constants.PLAY_STYLE_LOCATION

        # Function calls to collate the data.
        self._determine_team_number()
        self._determine_match_numbner()
        self._determine_alliance()
        self._determine_game_results()
        self._determine_play_style()

# ======================================================================================================================
# Low Level Private Functions
# ----------------------------------------------------------------------------------------------------------------------
    def _determine_team_number(self) -> None:
        """ 
        Determinging the team's number. \n
        Previously had a break once the 4th value was found. That was removed in case there is a double/triple finding from a poor marking. \n
        Defaults to 0000 if nothing was entered or detected. 
        """
        temp_team_number: list[int] = [0,0,0,0]
        temp_team_num_filled: list[bool] = [False, False, False, False]
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

                    if not temp_team_num_filled[self._team_number_location[key][1]]:
                        temp_team_number[self._team_number_location[key][1]] = self._team_number_location[key][0]
                        temp_team_num_filled[self._team_number_location[key][1]] = True
                        count += 1
            if count == 4:
                break

        self._raw_data['Team'][1] = ''.join(str(e) for e in temp_team_number)

#-----------------------------------------------------------------------------------------------------------------------
    def _determine_match_numbner(self) -> None:
        """ 
        Determinging the match the team played in. \n
        Previously had a break once the 2nd value was found. That was removed in case there is a double/triple finding from a poor marking. \n
        Defaults to 00 if nothing was entered or detected. 
        """
        temp_match_number: list[int] = [0,0]
        temp_match_num_filled: list[bool] = [False, False]
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
                     and key in self._match_number_location):

                     if not temp_match_num_filled[self._match_number_location[key][1]]:
                        temp_match_number[self._match_number_location[key][1]] = self._match_number_location[key][0]
                        temp_match_num_filled[self._match_number_location[key][1]] = True
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
                     and temp_key_x >= temp_x_lower
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

                if (temp_key_x <= temp_x_upper  
                    and temp_key_x >= temp_x_lower
                    and temp_key_y <= temp_y_upper
                    and temp_key_y >= temp_y_lower):
                    if (self._raw_data['Alliance'][1] == 0) and (key in self._game_blue_results_locations): # Blue alliance 
                        self._raw_data[self._game_blue_results_locations[key]][1] = 1
                    elif (self._raw_data['Alliance'][1] == 1) and (key in self._game_red_results_locations): # Red alliance 
                        self._raw_data[self._game_red_results_locations[key]][1] = 1

#-----------------------------------------------------------------------------------------------------------------------
    def _determine_play_style(self) -> None:
        """
        For the last of the sundried pertaining to the game itself. \n
        Set as a bunch of ifs to make sure it works. \n
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
                     and temp_key_x >= temp_x_lower
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
                            self._raw_data['Community'][1] = 0
                        elif key == 149:
                            self._raw_data['Community'][1] = 1
                        elif key == 150:
                            self._raw_data['Auton Charge Station'][1] = 2
                        elif key == 151: 
                            self._raw_data['HP & CS'][1] = 1
                        elif key == 152: 
                            self._raw_data['Over Charge'][1] = 1
                        elif key == 153: 
                            self._raw_data['ST & CS'][1] = 1
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
        return {k: v[1] for k,v in self._raw_data.items()}

# ======================================================================================================================
# Main
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    Scantron()
#======================================================================================================================+
# FIle:  Bubble_Sheet/src/OMR.py
# Project: OMR Scanrtron for FRC Team 5712
# Author:  William Bodeis <wdbodeis@gmail.com>
#-----------------------------------------------------------------------------------------------------------------------

import os, cv2, numpy as np
from pdf2image import convert_from_path

class OMR():
    def __init__(self,
                 cpu_threads: int,
                 image_format: str = 'jpeg',
                 save_image_overlay: bool = False,
                 mark_color: str = 'blue') -> None:

        # Possible user inputs.
        self.cpu_threads: int = cpu_threads
        self.image_format: str = image_format
        self.save_image_overlay: bool = save_image_overlay
        self.mark_color: str = mark_color

        # Created within and used by the class. 
        self._directories: list[str] = []
        self._keys_pdf_names: list[str]
        self._scantron_pdf_names: list[str]
        self._scantron_names: list[str]
        self._key_names: list[str]
        self._scanned_values: list = []
        self._scanned_keys: list = []
        self._sorted_key_values: list = []
        self._scanned_keys_average: tuple
        self._key_column_index: tuple(int) = (0, 8, 18, 26, 31, 39, 60, 74, 80, 94, 110, 124, 130, 136, 142)
        self._total_key_values: int = 155
        self._bubble_location: dict = {
                                        # Column 1
                                        0: [(1027, 2578), 'Auton HP TL'],
                                        1: [(1027, 2758), 'Auton HP ML'],
                                        2: [(1027, 2937), 'Auton HP LLCone'],
                                        3: [(1027, 3117), 'Auton HP LLCube)'],
                                        4: [(1028, 4381), 'Tele HP TL'],
                                        5: [(1028, 4562), 'Tele HP ML'],
                                        6: [(1028, 4743), 'Tele HP LLCone'],
                                        7: [(1028, 4924), 'Tele HP LLCube'],
                                        # Column 2
                                        8: [(1314, 1501), 'Blue Alliance'],
                                        9: [(1315, 1680), 'Red Alliance'],
                                        10: [(1316, 2576), 'Auton HP TM'],
                                        11: [(1316, 2756), 'Auton HP MM'],
                                        12: [(1316, 2937), 'Auton HP MLCone'],
                                        13: [(1317, 3117), 'Auton HP MLCube'],
                                        14: [(1316, 4380), 'Tele HP TM'],
                                        15: [(1317, 4561), 'Tele HP MM'],
                                        16: [(1316, 4743), 'Tele HP MLCone'],
                                        17: [(1317, 4923), 'Tele HP MLCube'],
                                        # Column 3
                                        18: [(1605, 2576), 'Auton M TR'],
                                        19: [(1605, 2757), 'Auton M MR'],
                                        20: [(1605, 2936), 'Auton M LRCone'], 
                                        21: [(1606, 3116), 'Auton M LRCube'],
                                        22: [(1606, 4379), 'Tele HP TR'],
                                        23: [(1607, 4561), 'Tele HP MR'],
                                        24: [(1606, 4743), 'Tele HP LRCone'],
                                        25: [(1606, 4923), 'Tele HP LRCube'],
                                        # Column 4
                                        26: [(1894, 5464), 'Floor Yes'],
                                        27: [(1896, 5642), 'Single Sub Yes'], 
                                        28: [(1895, 5826), 'Double Sub Slider Yes'],
                                        29: [(1894, 6005), 'Double Sub Chute Yes'],
                                        30: [(1893, 7088), 'Parked Yes'],
                                        # Column 5
                                        31: [(2184, 2576), 'Auton M TL'],
                                        32: [(2184, 2756), 'Auton M ML'],
                                        33: [(2184, 2937), 'Auton M LLCone'],
                                        34: [(2184, 3117), 'Auton M LLCube'],
                                        35: [(2184, 4380), 'Tele M TL'],
                                        36: [(2184, 4561), 'Tele M ML'],
                                        37: [(2184, 4742), 'Tele M LLCone'],
                                        38: [(2184, 4923), 'Tele M LLCube'],
                                        # Column 6
                                        39: [(2472, 429), 'Match Deca Zero'],
                                        40: [(2471, 608), 'Match Zero'],
                                        41: [(2472, 1143), 'Team Kilo Zero'],
                                        42: [(2472, 1321), 'Team Hecto Zero'],
                                        43: [(2472, 1502), 'Team Deca Zero'],
                                        44: [(2472, 1678), 'Team Zero'],
                                        45: [(2473, 2576), 'Auton M TM'],
                                        46: [(2473, 2756), 'Auton M MM'],
                                        47: [(2474, 2936), 'Auton M MLCone'],
                                        48: [(2474, 3117), 'Auton M MLCube'],
                                        49: [(2474, 3479), 'Auton Charge Station On'],
                                        50: [(2474, 4380), 'Tele M TM'],
                                        51: [(2475, 4563), 'Tele M MM'],
                                        52: [(2473, 4740), 'Tele M MLCone'],
                                        53: [(2474, 4923), 'Tele M MLCube'],
                                        54: [(2474, 5464), 'Floor No'],
                                        55: [(2474, 5644), 'Single Sub No'],
                                        56: [(2473, 5824), 'Double Sub Slider No'],
                                        57: [(2473, 6004), 'Parked No'],
                                        58: [(2473, 6547), 'End Game Charge Station On'],
                                        59: [(2472, 7087), 'Parked No'],
                                        # Column 7
                                        60: [(2763, 430), 'Match Deca One'],
                                        61: [(2763, 608), 'Match One'],
                                        62: [(2762, 1144), 'Team Kilo One'],
                                        63: [(2763, 1321), 'Team Hecto One'],
                                        64: [(2762, 1500), 'Team Deca One'],
                                        65: [(2763, 1679), 'Team One'],
                                        66: [(2763, 2574), 'Auton M TR'],
                                        67: [(2763, 2756), 'Auton M MR'],
                                        68: [(2764, 2936), 'Auton M LRCone'],
                                        69: [(2764, 3117), 'Auton M LRCube'],
                                        70: [(2764, 4380), 'Tele M TR'],
                                        71: [(2764, 4561), 'Tele M MR'],
                                        72: [(2764, 4742), 'Tele M LRCone'],
                                        73: [(2763, 4919), 'Tele M LRCube'],
                                        # Column 8
                                        74: [(3052, 430), 'Match Deca Two'],
                                        75: [(3052, 609), 'Match Two'],
                                        76: [(3052, 1143), 'Team Kilo Two'],
                                        77: [(3052, 1322), 'Team Hecto Two'],
                                        78: [(3053, 1501), 'Team Deca Two'],
                                        79: [(3053, 1679), 'Team Two'],
                                        # Column 9
                                        80: [(3343, 429), 'Match Deca Three'],
                                        81: [(3343, 608), 'Match Three'],
                                        82: [(3342, 1143), 'Team Kilo Three'],
                                        83: [(3343, 1321), 'Team Hecto Three'],
                                        84: [(3343, 1500), 'Team Deca Three'],
                                        85: [(3344, 1679), 'Team Three'],
                                        86: [(3344, 2576), 'Auton ST TL'],
                                        87: [(3344, 2756), 'Auton ST ML'],
                                        88: [(3345, 2936), 'Auton ST LLCone'],
                                        89: [(3345, 3116), 'Auton ST LLCube'],
                                        90: [(3343, 4378), 'Tele ST TL'],
                                        91: [(3344, 4561), 'Tele ST ML'],
                                        92: [(3344, 4922), 'Tele ST LLCone'],
                                        93: [(3345, 4741), 'Tele ST LLCube'],
                                        # Column 10
                                        94: [(3633, 429), 'Match Deca Four'],
                                        95: [(3633, 607), 'Match Four'],
                                        96: [(3633, 1142), 'Team Kilo Four'],
                                        97: [(3633, 1321), 'Team Hecto Four'],
                                        98: [(3634, 1499), 'Team Deca Four'],
                                        99: [(3634, 1678), 'Team Four'],
                                        100: [(3634, 2574), 'Auton ST TM'],
                                        101: [(3635, 2755), 'Auton ST MM'],
                                        102: [(3635, 2935), 'Auton ST MLCone'],
                                        103: [(3635, 3115), 'Auton ST MLCube'],
                                        104: [(3635, 3476), 'Auton Charge Station Balanced'],
                                        105: [(3635, 4379), 'Tele ST TM'],
                                        106: [(3635, 4560), 'Tele ST MM'],
                                        107: [(3635, 4740), 'Tele ST MLCone'],
                                        108: [(3635, 4921), 'Tele ST MLCube'],
                                        109: [(3634, 6545), 'End Game Charge Station Balanced'],
                                        # Column 11
                                        110: [(3921, 428), 'Match Deca Five'],
                                        111: [(3921, 607), 'Match Five'],
                                        112: [(3921, 1141), 'Team Kilo Five'],
                                        113: [(3921, 1319), 'Team Hecto Five'],
                                        114: [(3922, 1498), 'Team Deca Five'],
                                        115: [(3922, 1677), 'Team Five'],
                                        116: [(3922, 2574), 'Auton ST TR'],
                                        117: [(3923, 2754), 'Auton ST MR'],
                                        118: [(3924, 2934), 'Auton ST LRCone'],
                                        119: [(3923, 3114), 'Auton ST LRCube'],
                                        120: [(3922, 4558), 'Tele ST TR'],
                                        121: [(3923, 4378), 'Tele ST MR'],
                                        122: [(3923, 4739), 'Tele ST LRCone'],
                                        123: [(3923, 4921), 'Tele ST LRCube'],
                                        # Column 12
                                        124: [(4211, 427), 'Match Deca Six'],
                                        125: [(4211, 606), 'Match Six'],
                                        126: [(4211, 1140), 'Team Kilo Six'],
                                        127: [(4211, 1319), 'Team Hecto Six'],
                                        128: [(4211, 1497), 'Team Deca Six'],
                                        129: [(4212, 1676), 'Team Six'],
                                        # Column 13
                                        130: [(4500, 426), 'Match Deca Seven'],
                                        131: [(4500, 605), 'Match Seven'],
                                        132: [(4500, 1139), 'Team Kilo Seven'],
                                        133: [(4501, 1318), 'Team Hecto Seven'],
                                        134: [(4501, 1497), 'Team Deca Seven'],
                                        135: [(4501, 1676), 'Team Seven'],
                                        # Column 14
                                        136: [(4790, 604), 'Match Deca Eight'],
                                        137: [(4791, 425), 'Match Eight'],
                                        138: [(4791, 1139), 'Team Kilo Eight'],
                                        139: [(4791, 1317), 'Team Hecto Eight'],
                                        140: [(4791, 1494), 'Team Deca Eight'],
                                        141: [(4791, 1674), 'Team Eight'],
                                        # Column 15
                                        142: [(5080, 424), 'Match Deca Nine'],
                                        143: [(5080, 603), 'Match Nine'],
                                        144: [(5080, 1138), 'Team Kilo Nine'],
                                        145: [(5080, 1316), 'Team Hecto Nine'],
                                        146: [(5080, 1494), 'Team Deca Nine'],
                                        147: [(5079, 1673), 'Team Nine'],
                                        148: [(5081, 2569), 'Left Community Yes'],
                                        149: [(5081, 2750), 'Left Community No'],
                                        150: [(5082, 3472), 'Auton Charge Station Not Attempted'],
                                        151: [(5081, 5458), 'Travel Between HP and CS'],
                                        152: [(5081, 5637), 'Travel Over Charge'],
                                        153: [(5080, 5818), 'Travel Between ST and CS'],
                                        154: [(5080, 6540), 'End Game Charge Station Not Attempted']
                                        }

        # Initializing functions.
        self._create_directories_list()
        self._check_directories()

        # Checking for and converting pdf files if those are used instead of pictures.
        self._get_key_pdf_names()
        self._get_scantron_pdf_names()
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
        if not self._key_names:
            del self
            raise FileExistsError('No image for key(s) to process were found.')
        if not self._scantron_names:
            del self
            raise FileExistsError('No image for game sheets(s) to process were found.')
        
        # Getting the marks for the scantron key(s) that are entered and the actual game sheets. 
        self._process_images(image_directory = 1, 
                             image_names = self._key_names, 
                             data = 'key',
                             color = self.mark_color
                             )

        # Getting the values from the game sheets. 
        self._process_images(image_directory = 3,
                             image_names = self._scantron_names,
                             data = 'scantron',
                             color = self.mark_color
                             )
        
        self._sort_key_values()
        self._get_key_average()
        self._update_scantron_bubbles()

#-----------------------------------------------------------------------------------------------------------------------
    def _create_directories_list(self):
        self._directories.append('key/')                # 0
        self._directories.append('key_images/')         # 1
        self._directories.append('scantron/')           # 2
        self._directories.append('scantron_images/')    # 3
        self._directories.append('results/')            # 4
        
#-----------------------------------------------------------------------------------------------------------------------
    def _check_directories(self) -> None:
        for directory in self._directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

#-----------------------------------------------------------------------------------------------------------------------
    def _get_key_pdf_names(self) -> None:
        self._keys_pdf_names = [i for i in os.listdir(self._directories[0]) if i.endswith('.pdf')]

#-----------------------------------------------------------------------------------------------------------------------
    def _get_key_image_names(self) -> None:
        self._key_names = [i for i in os.listdir(self._directories[1]) if (i.endswith('.' + self.image_format))]

#-----------------------------------------------------------------------------------------------------------------------
    def _get_scantron_pdf_names(self) -> None:
        self._scantron_pdf_names = [i for i in os.listdir(self._directories[2]) if i.endswith('.pdf')]

#-----------------------------------------------------------------------------------------------------------------------
    def _get_scantron_image_names(self) -> None:
        self._scantron_names = [i for i in os.listdir(self._directories[3]) if (i.endswith('.' + self.image_format))]

#-----------------------------------------------------------------------------------------------------------------------
    def _convert_pdf_to_image(self, pdf_directory, image_directory, pdf_names) -> None:

        for i in range(len(pdf_names)):
                images = convert_from_path(pdf_path = self._directories[pdf_directory] + pdf_names[i],
                                           poppler_path = 'poppler/Library/bin',
                                           dpi = 700,
                                           thread_count = self.cpu_threads)

                for j in range(len(images)):
                    try:
                        location = self._directories[image_directory] + str(i+1) + '-' + str(j+1) + '.' + self.image_format
                        images[j].save(fp = location,
                                       bitmap_format = self.image_format)
                    except:
                        location = self._directories[image_directory] + str(i+1) + '-' + str(j+1) + '.jpeg'
                        images[j].save(fp = location,
                                       bitmap_format = 'jpeg')

#-----------------------------------------------------------------------------------------------------------------------
    def _sort_key_values(self) -> None:
        temp_sorted_key_values: list = []
        for key in self._scanned_keys: # Looping through each key
            temp_key_sorted = []
            for i in range(len(self._key_column_index)): # Sorting out each 'column'
                if i == (len(self._key_column_index) - 1):
                    temp_column = key[self._key_column_index[i]: (self._total_key_values + 1)]
                else:
                    temp_column = key[self._key_column_index[i]: self._key_column_index[i+1]]
                temp_key_sorted += sorted(temp_column, key = lambda x: x[1]) # Sorting the column.
            temp_sorted_key_values.append(temp_key_sorted) # Adding the list of each key to the mega list.
        self._sorted_key_values = temp_sorted_key_values

#-----------------------------------------------------------------------------------------------------------------------
    def _get_key_average(self) -> None:
        # TODO Try-except for if the keys don't have the total (155) marks/indicated values. 
        temp_key_average: list = []
        for i in range(self._total_key_values):
            temp_x_sum: int = 0
            temp_y_sum: int = 0
            temp_average_x: int = 0
            temp_average_y: int = 0
            for j in range(len(self._sorted_key_values)):
                temp_x_sum += self._sorted_key_values[j][i][0]
                temp_y_sum += self._sorted_key_values[j][i][1]
            temp_average_x = int(temp_x_sum / len(self._sorted_key_values))
            temp_average_y = int(temp_y_sum / len(self._sorted_key_values))
            temp_key_average.append(tuple((temp_average_x, temp_average_y)))
        self._scanned_keys_average = tuple(temp_key_average)

#-----------------------------------------------------------------------------------------------------------------------
    def _update_scantron_bubbles(self):
        for key in self._bubble_location:
            self._bubble_location[key][0] = self._scanned_keys_average[key]

#-----------------------------------------------------------------------------------------------------------------------
    # TODO Get the correct HSV color for the other colors and verify what was found for greem, red, and yellow.
    def _process_images(self, image_directory, image_names, data, color) -> None:
            for i in range(len(image_names)):
                try:
                    marks = []
                    img = cv2.imread(self._directories[image_directory] + image_names[i])
                    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

                    # Threshold for blue.
                    if color == 'blue':
                        lower_range = np.array([110,50,50])
                        upper_range = np.array([130,255,255])
                    else:
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
                        cv2.imwrite(('results/' + 'scantron_overlay_' + str(i) + '.jpeg'), result)
                    elif data == 'scantron':
                        self._scanned_values.append(tuple(sorted(marks)))
                except Exception as ex:
                    print(ex)
            
#-----------------------------------------------------------------------------------------------------------------------
    def print_scanned_values(self):
        print()
        print('Scanned Values')
        print('----------')
        print('Type:', type(self._scanned_values))
        print('Sheets scanned:', len(self._scanned_values))
        for i in range(len(self._scanned_values)):
            print('Marks in sheet {}: {}'.format(i+1, len(self._scanned_values[i])))

#-----------------------------------------------------------------------------------------------------------------------
    def print_scanned_keys(self):
        print()
        print('Scanned Keys')
        print('----------')
        print('Type:', type(self._scanned_keys))
        print('Keys scanned:', len(self._scanned_keys))
        for i in range(len(self._scanned_keys)):
            print(len(self._scanned_keys[i]))

#-----------------------------------------------------------------------------------------------------------------------
    def print_sorted_keys(self):
        print()
        print('Sorted Keys')
        print('----------')
        print('Type:', type(self._sorted_key_values))
        print('Sorted Key Values:', len(self._sorted_key_values))
        for i in range(len(self._sorted_key_values)):
            print(len(self._sorted_key_values[i]))

#-----------------------------------------------------------------------------------------------------------------------
    def print_averaged_key(self):
        print()
        print('Sorted Keys')
        print('----------')
        print('Type:', type(self._scanned_keys_average))
        print('Averaged Key Values:', len(self._scanned_keys_average))
        print(self._scanned_keys_average)

#-----------------------------------------------------------------------------------------------------------------------
    def get_key_values(self) -> dict:
        return self._bubble_location

#-----------------------------------------------------------------------------------------------------------------------
    def get_scantron_values(self) -> list:
        return self._scanned_values
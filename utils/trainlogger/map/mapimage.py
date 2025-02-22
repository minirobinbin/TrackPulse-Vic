from PIL import Image, ImageDraw
import tkinter as tk
from PIL import ImageTk
from matplotlib.pylab import f

x_offset = 10600
y_offset = 6300
dpi = 32/96

class MapImageHandler:
    def __init__(self, map_image_path, station_order_dictionary):
        self.station_coordinates = {
            "Parliament": (3618 + x_offset, 1264 + y_offset,  4134 + x_offset,  1393 + y_offset),
            "Flinders Street": (2616 + x_offset, 2732 + y_offset,  3325 + x_offset,  2832 + y_offset),
            "Southern Cross": (431 + x_offset, 1264 + y_offset, 1162 + x_offset, 1378 + y_offset),
            "Melbourne Central": (2716 + x_offset, 376 + y_offset, 3217 + x_offset, 619 + y_offset),
            "Flagstaff": (2351 + x_offset, 168 + y_offset, 2494 + x_offset, 619 + y_offset),
            "Richmond": (4327 + x_offset, 2632 + y_offset, 4807 + x_offset, 2732 + y_offset),
            "East Richmond": (5250 + x_offset, 1750 + y_offset, 6000 + x_offset, 1900 + y_offset),
            "Burnley": (6050 + x_offset, 1700 + y_offset, 6450 + x_offset, 1950 + y_offset),
            "Heyington": (6600 + x_offset, 2100 + y_offset, 7100 + x_offset, 2250 + y_offset),
            "Kooyong": (7100 + x_offset, 2100 + y_offset, 7550 + x_offset, 2250 + y_offset),
            "Tooronga": (7600 + x_offset, 2100 + y_offset, 8100 + x_offset, 2300 + y_offset),
            "Gardiner": (8100 + x_offset, 2100 + y_offset, 8550 + x_offset, 2250 + y_offset),
            "Glen Iris": (8550 + x_offset, 2100 + y_offset, 9000 + x_offset, 2250 + y_offset),
            "Darling": (9000 + x_offset, 2100 + y_offset, 9400 + x_offset, 2250 + y_offset),
            "East Malvern": (9450 + x_offset, 2100 + y_offset, 10050 + x_offset, 2250 + y_offset),
            "Holmesglen": (10050 + x_offset, 2100 + y_offset, 10700 + x_offset, 2300 + y_offset),
            "Jordanville": (10700 + x_offset, 2100 + y_offset, 11250 + x_offset, 2250 + y_offset),
            "Mount Waverley": (11300 + x_offset, 2100 + y_offset, 12100 + x_offset, 2250 + y_offset),
            "Syndal": (12150 + x_offset, 2100 + y_offset, 12500 + x_offset, 2250 + y_offset),
            "Glen Waverley": (12600 + x_offset, 1900 + y_offset, 13300 + x_offset, 2100 + y_offset),
            "Hawthorn": (6650 + x_offset, 1750 + y_offset, 7100 + x_offset, 1900 + y_offset),
            "Glenferrie": (6600 + x_offset, 1550 + y_offset, 7150 + x_offset, 1700 + y_offset),
            "Auburn": (6600 + x_offset, 1300 + y_offset, 7000 + x_offset, 1500 + y_offset),
            "Camberwell": (6650 + x_offset, 1100 + y_offset, 7250 + x_offset, 1300 + y_offset),
            "Riversdale": (7250 + x_offset, 1150 + y_offset, 7800 + x_offset, 1350 + y_offset),
            "Willison": (7800 + x_offset, 1150 + y_offset, 8200 + x_offset, 1350 + y_offset),
            "Hartwell": (8200 + x_offset, 1150 + y_offset, 8650 + x_offset, 1300 + y_offset),
            "Burwood": (8650 + x_offset, 1200 + y_offset, 9150 + x_offset, 1350 + y_offset),
            "Ashburton": (9100 + x_offset, 1200 + y_offset, 9650 + x_offset, 1300 + y_offset),
            "Alamein": (9750 + x_offset, 950 + y_offset, 10200 + x_offset, 1200 + y_offset),
            "East Camberwell": (6650 + x_offset, 750 + y_offset, 7450 + x_offset, 950 + y_offset),
            "Canterbury": (6650 + x_offset, 550 + y_offset, 7150 + x_offset, 750 + y_offset),
            "Chatham": (6600 + x_offset, 350 + y_offset, 7050 + x_offset, 550 + y_offset),
            "Union": (6600 + x_offset, 150 + y_offset, 6950 + x_offset, 350 + y_offset),
            "Box Hill": (6600 + x_offset, -50 + y_offset, 7000 + x_offset, 200 + y_offset),
            "Laburnum": (6650 + x_offset, -200 + y_offset, 7150 + x_offset, -50 + y_offset),
            "Blackburn": (6600 + x_offset, -400 + y_offset, 7100 + x_offset, -250 + y_offset),
            "Nunawading": (6600 + x_offset, -600 + y_offset, 7200 + x_offset, -450 + y_offset),
            "Mitcham": (6600 + x_offset, -850 + y_offset, 7050 + x_offset, -650 + y_offset),
            "Heatherdale": (6600 + x_offset, -1000 + y_offset, 7250 + x_offset, -850 + y_offset),
            "Ringwood": (6650 + x_offset, -1200 + y_offset, 7150 + x_offset, -1050 + y_offset),
            "Heathmont": (7150 + x_offset, -1200 + y_offset, 7750 + x_offset, -1050 + y_offset),
            "Bayswater": (7700 + x_offset, -1200 + y_offset, 8250 + x_offset, -1000 + y_offset),
            "Boronia": (8300 + x_offset, -1200 + y_offset, 8700 + x_offset, -1050 + y_offset),
            "Ferntree Gully": (8700 + x_offset, -1200 + y_offset, 9400 + x_offset, -1050 + y_offset),
            "Upper Ferntree Gully": (9400 + x_offset, -1200 + y_offset, 10400 + x_offset, -1000 + y_offset),
            "Upwey": (10400 + x_offset, -1200 + y_offset, 10800 + x_offset, -1050 + y_offset),
            "Tecoma": (10800 + x_offset, -1200 + y_offset, 11250 + x_offset, -1000 + y_offset),
            "Belgrave": (11300 + x_offset, -1400 + y_offset, 11750 + x_offset, -1200 + y_offset),
            "Ringwood East": (6600 + x_offset, -1550 + y_offset, 7400 + x_offset, -1450 + y_offset),
            "Croydon": (6600 + x_offset, -1800 + y_offset, 7050 + x_offset, -1600 + y_offset),
            "Mooroolbark": (6600 + x_offset, -2000 + y_offset, 7250 + x_offset, -1750 + y_offset),
            "Lilydale": (6300 + x_offset, -2300 + y_offset, 6700 + x_offset, -2150 + y_offset),
            "South Yarra": (4150 + x_offset, 2750 + y_offset, 4750 + x_offset, 2950 + y_offset),
            "Hawksburn": (4300 + x_offset, 3150 + y_offset, 4850 + x_offset, 3300 + y_offset),
            "Toorak": (4450 + x_offset, 3350 + y_offset, 4850 + x_offset, 3500 + y_offset),
            "Armadale": (4350 + x_offset, 3500 + y_offset, 4850 + x_offset, 3700 + y_offset),
            "Malvern": (4400 + x_offset, 3750 + y_offset, 4850 + x_offset, 3900 + y_offset),
            "Caulfield": (4400 + x_offset, 3950 + y_offset, 4850 + x_offset, 4100 + y_offset),
            "Jolimont": (4277 + x_offset, 1715 + y_offset, 4700 + x_offset, 1837 + y_offset),
            "West Richmond": (4280 + x_offset, 1514 + y_offset, 5010 + x_offset, 1631 + y_offset),
            "North Richmond": (4280 + x_offset, 1321 + y_offset, 5010 + x_offset, 1438 + y_offset),
            "Collingwood": (4273 + x_offset, 1100 + y_offset, 4852 + x_offset, 1224 + y_offset),
            "Victoria Park": (4273 + x_offset, 914 + y_offset, 4886 + x_offset, 1031 + y_offset),
            "Clifton Hill": (4266 + x_offset, 708 + y_offset, 4769 + x_offset, 839 + y_offset),
            "Rushall": (4250 + x_offset, 350 + y_offset, 4599 + x_offset, 499 + y_offset),
            "Merri": (4250 + x_offset, 150 + y_offset, 4549 + x_offset, 299 + y_offset),
            "Northcote": (4250 + x_offset, -50 + y_offset, 4749 + x_offset, 99 + y_offset),
            "Croxton": (4250 + x_offset, -250 + y_offset, 4799 + x_offset, -51 + y_offset),
            "Thornbury": (4300 + x_offset, -450 + y_offset, 4799 + x_offset, -251 + y_offset),
            "Bell": (4250 + x_offset, -650 + y_offset, 4599 + x_offset, -501 + y_offset),
            "Preston": (4250 + x_offset, -850 + y_offset, 4699 + x_offset, -651 + y_offset),
            "Regent": (4250 + x_offset, -1050 + y_offset, 4649 + x_offset, -901 + y_offset),
            "Reservoir": (4250 + x_offset, -1250 + y_offset, 4749 + x_offset, -1101 + y_offset),
            "Ruthven": (4250 + x_offset, -1450 + y_offset, 4649 + x_offset, -1301 + y_offset),
            "Keon Park": (4250 + x_offset, -1700 + y_offset, 4799 + x_offset, -1501 + y_offset),
            "Thomastown": (4250 + x_offset, -1850 + y_offset, 4899 + x_offset, -1701 + y_offset),
            "Lalor": (4250 + x_offset, -2100 + y_offset, 4549 + x_offset, -1901 + y_offset),
            "Epping": (4250 + x_offset, -2250 + y_offset, 4699 + x_offset, -2101 + y_offset),
            "South Morang": (4250 + x_offset, -2500 + y_offset, 4949 + x_offset, -2301 + y_offset),
            "Middle Gorge": (4250 + x_offset, -2700 + y_offset, 4899 + x_offset, -2501 + y_offset),
            "Hawkstowe": (4250 + x_offset, -2850 + y_offset, 4849 + x_offset, -2701 + y_offset),
            "Mernda": (3950 + x_offset, -3200 + y_offset, 4349 + x_offset, -3051 + y_offset),
            'Westgarth': (5400 + x_offset, 450 + y_offset, 5849 + x_offset, 599 + y_offset),
            'Dennis': (5400 + x_offset, 300 + y_offset, 5699 + x_offset, 449 + y_offset),
            'Fairfield': (5400 + x_offset, 0 + y_offset, 5849 + x_offset, 149 + y_offset),
            'Alphington': (5400 + x_offset, -150 + y_offset, 5849 + x_offset, -1 + y_offset),
            'Darebin': (5400 + x_offset, -300 + y_offset, 5699 + x_offset, -151 + y_offset),
            'Ivanhoe': (5400 + x_offset, -600 + y_offset, 5699 + x_offset, -451 + y_offset),
            'Eaglemont': (5400 + x_offset, -750 + y_offset, 5999 + x_offset, -601 + y_offset),
            'Heidelberg': (5400 + x_offset, -900 + y_offset, 5849 + x_offset, -751 + y_offset),
            'Rosanna': (5400 + x_offset, -1200 + y_offset, 5849 + x_offset, -1051 + y_offset),
            'Macleod': (5400 + x_offset, -1350 + y_offset, 5849 + x_offset, -1201 + y_offset),
            'Watsonia': (5400 + x_offset, -1650 + y_offset, 5849 + x_offset, -1351 + y_offset),
            'Greensborough': (5400 + x_offset, -1800 + y_offset, 6149 + x_offset, -1651 + y_offset),
            'Montmorency': (5400 + x_offset, -1950 + y_offset, 5999 + x_offset, -1801 + y_offset),
            'Eltham': (5400 + x_offset, -2100 + y_offset, 5699 + x_offset, -1951 + y_offset),
            'Diamond Creek': (5400 + x_offset, -2400 + y_offset, 6149 + x_offset, -2251 + y_offset),
            'Wattle Glen': (5400 + x_offset, -2550 + y_offset, 5999 + x_offset, -2401 + y_offset),
            'Hurstbridge': (4950 + x_offset, -2850 + y_offset, 5549 + x_offset, -2701 + y_offset),
            "Richmond": [(4327 + x_offset, 2632 + y_offset, 4807 + x_offset, 2732 + y_offset), (4500 + x_offset, 1946 + y_offset, 4651 + x_offset, 2622 + y_offset)],
            "North Melbourne": (360 + x_offset, 361 + y_offset, 1155 + x_offset, 490 + y_offset),
            "South Kensington": (-213 + x_offset, 383 + y_offset, 331 + x_offset, 641 + y_offset),
            "Footscray": (-765 + x_offset, -369 + y_offset, -299 + x_offset, -233 + y_offset),
            "Seddon": (-1183 + x_offset, 303 + y_offset, -779 + x_offset, 433 + y_offset),
            "Yarraville": (-1248 + x_offset, 511 + y_offset, -792 + x_offset, 629 + y_offset),
            "Spotswood": (-1365 + x_offset, 694 + y_offset, -779 + x_offset, 850 + y_offset),
            "Newport":(-597 + x_offset, 863 + y_offset, -154 + x_offset, 1045 + y_offset),
            "North Williamstown": (-581 + x_offset, 1215 + y_offset, 341 + x_offset, 1423 + y_offset),
            "Williamstown Beach": (-584 + x_offset, 1462 + y_offset, 367 + x_offset, 1592 + y_offset),
            "Williamstown": (-1014 + x_offset, 1761 + y_offset, -336 + x_offset, 1918 + y_offset),
            "Aircraft": (-2737 + x_offset, 889 + y_offset, -2333 + x_offset, 1019 + y_offset),
            "Williams Landing": (-3531 + x_offset, 850 + y_offset, -2724 + x_offset, 1019 + y_offset),
            "Hoppers Crossing": (-4404 + x_offset, 876 + y_offset, -3557 + x_offset, 1006 + y_offset),
            "Werribee": (-4924 + x_offset, 1045 + y_offset, -4495 + x_offset, 1202 + y_offset),
            "Seaholme": (-1261 + x_offset, 1306 + y_offset, -740 + x_offset, 1436 + y_offset),
            "Altona": (-1599 + x_offset, 1306 + y_offset, -1261 + x_offset, 1436 + y_offset),
            "Westona": (-2042 + x_offset, 1306 + y_offset, -1612 + x_offset, 1462 + y_offset),
            "Laverton": (-2316 + x_offset, 863 + y_offset, -1847 + x_offset, 1006 + y_offset),
            "Middle Footscray": (-1394 + x_offset, -522 + y_offset, -878 + x_offset, -232 + y_offset),
            "West Footscray": (-1994 + x_offset, -535 + y_offset, -1498 + x_offset, -246 + y_offset),
            "Tottenham": (-2600 + x_offset, -363 + y_offset, -2069 + x_offset, -219 + y_offset),
            "Sunshine": (-3200 + x_offset, 600 + y_offset, -2751 + x_offset, 749 + y_offset),
            "Albion": (-2980 + x_offset, -538 + y_offset, -2664 + x_offset, -435 + y_offset),
            "Ginifer": (-2974 + x_offset, -824 + y_offset, -2657 + x_offset, -735 + y_offset),
            "St Albans": (-2974 + x_offset, -1031 + y_offset, -2512 + x_offset, -907 + y_offset),
            "Keilor Plains": (-2974 + x_offset, -1231 + y_offset, -2409 + x_offset, -1114 + y_offset),
            "Watergardens": (-2974 + x_offset, -1437 + y_offset, -2306 + x_offset, -1320 + y_offset),
            "Diggers Rest": (-2967 + x_offset, -1637 + y_offset, -2361 + x_offset, -1484 + y_offset),
            "Sunbury": (-2974 + x_offset, -1844 + y_offset, -2574 + x_offset, -1713 + y_offset),
            "Clarkefield": (-3150 + x_offset, -2100 + y_offset, -2551 + x_offset, -1951 + y_offset),
            "Riddells Creek": (-3150 + x_offset, -2100 + y_offset, -2551 + x_offset, -1951 + y_offset),
            "Gisborne": (-3150 + x_offset, -2550 + y_offset, -2701 + x_offset, -2251 + y_offset),
            "Macedon": (-3150 + x_offset, -2700 + y_offset, -2701 + x_offset, -2551 + y_offset),
            "Woodend": (-3150 + x_offset, -2850 + y_offset, -2551 + x_offset, -2701 + y_offset),
            "Kyneton": (-3150 + x_offset, -3000 + y_offset, -2701 + x_offset, -2851 + y_offset),
            "Malmsbury": (-3150 + x_offset, -3300 + y_offset, -2551 + x_offset, -3151 + y_offset),
            "Castlemaine": (-3150 + x_offset, -3450 + y_offset, -2401 + x_offset, -3301 + y_offset),
            "Kangaroo Flat": (-3150 + x_offset, -3600 + y_offset, -2401 + x_offset, -3451 + y_offset),
            "Bendigo": (-3150 + x_offset, -3900 + y_offset, -2701 + x_offset, -3751 + y_offset),
            "Epsom": (-2250 + x_offset, -3900 + y_offset, -1801 + x_offset, -3751 + y_offset),
            "Huntly": (-1800 + x_offset, -3900 + y_offset, -1501 + x_offset, -3751 + y_offset),
            "Goornong": (-1500 + x_offset, -3900 + y_offset, -1051 + x_offset, -3751 + y_offset),
            "Elmore": (-900 + x_offset, -3900 + y_offset, -601 + x_offset, -3751 + y_offset),
            "Rochester": (-600 + x_offset, -3900 + y_offset, -151 + x_offset, -3751 + y_offset),
            "Echuca": (0 + x_offset, -4050 + y_offset, 449 + x_offset, -3901 + y_offset),
            "Eaglehawk": (-3000 + x_offset, -4350 + y_offset, -2551 + x_offset, -4201 + y_offset),
            "Raywood": (-3150 + x_offset, -4500 + y_offset, -2701 + x_offset, -4351 + y_offset),
            "Dingee": (-3150 + x_offset, -4650 + y_offset, -2851 + x_offset, -4651 + y_offset),
            "Pyramid": (-3150 + x_offset, -4950 + y_offset, -2851 + x_offset, -4801 + y_offset),
            "Kerang": (-3150 + x_offset, -5100 + y_offset, -2851 + x_offset, -4951 + y_offset),
            "Swan Hill": (-3600 + x_offset, -5400 + y_offset, -3001 + x_offset, -5251 + y_offset),
            "Ardeer": (-4100 + x_offset, 0 + y_offset, -3801 + x_offset, 149 + y_offset),
            "Deer Park": (-5150 + x_offset, 0 + y_offset, -4701 + x_offset, 149 + y_offset),
            "Tarneit": (-5650 + x_offset, 550 + y_offset, -5200 + x_offset, 650 + y_offset),
            "Wyndham Vale": (-5950 + x_offset, 750 + y_offset, -5250 + x_offset, 900 + y_offset),
            "Little River": (-5800 + x_offset, 950 + y_offset, -5650 + x_offset, 700 + y_offset),
            "Lara": (-5550 + x_offset, 1100 + y_offset, -5200 + x_offset, 1300 + y_offset),
            "Corio": (-5550 + x_offset, 1350 + y_offset, -5250 + x_offset, 1500 + y_offset),
            "North Shore": (-5800 + x_offset, 1550 + y_offset, -5250 + x_offset, 1700 + y_offset),
            "North Geelong": (-5950 + x_offset, 1750 + y_offset, -5200 + x_offset, 1900 + y_offset),
            "Geelong": (-5700 + x_offset, 1900 + y_offset, -5250 + x_offset, 2100 + y_offset),
            "South Geelong": (-5950 + x_offset, 2150 + y_offset, -5250 + x_offset, 2300 + y_offset),
            "Marshall": (-5650 + x_offset, 2350 + y_offset, -5200 + x_offset, 2500 + y_offset),
            "Waurn Ponds": (-5900 + x_offset, 2550 + y_offset, -5250 + x_offset, 2700 + y_offset),
            "Winchelsea": (-5700 + x_offset, 2750 + y_offset, -5150 + x_offset, 2900 + y_offset),
            "Birregurra": (-5650 + x_offset, 2900 + y_offset, -5150 + x_offset, 3100 + y_offset),
            "Colac": (-5400 + x_offset, 3100 + y_offset, -5150 + x_offset, 3300 + y_offset),
            "Camperdown": (-5800 + x_offset, 3300 + y_offset, -5150 + x_offset, 3500 + y_offset),
            "Terang": (-5500 + x_offset, 3550 + y_offset, -5150 + x_offset, 3700 + y_offset),
            "Sherwood Park": (-5850 + x_offset, 3750 + y_offset, -5150 + x_offset, 3900 + y_offset),
            "Warrnambool": (-5400 + x_offset, 4050 + y_offset, -4700 + x_offset, 4200 + y_offset),
            "Caronline Springs": (-6050 + x_offset, 0 + y_offset, -5250 + x_offset, 150 + y_offset),
            "Rockbank": (-6550 + x_offset, 50 + y_offset, -6050 + x_offset, 150 + y_offset),
            "Cobblebank": (-7150 + x_offset, 50 + y_offset, -6500 + x_offset, 150 + y_offset),
            "Melton": (-7500 + x_offset, 50 + y_offset, -7150 + x_offset, 200 + y_offset),
            "Bacchus Marsh": (-8250 + x_offset, 50 + y_offset, -7550 + x_offset, 200 + y_offset),
            "Ballan": (-8600 + x_offset, 50 + y_offset, -8300 + x_offset, 150 + y_offset),
            "Ballarat": (-9050 + x_offset, 50 + y_offset, -8650 + x_offset, 200 + y_offset),
            "Wendouree": (-9800 + x_offset, 50 + y_offset, -9200 + x_offset, 200 + y_offset),
            "Beaufort": (-10250 + x_offset, 150 + y_offset, -9750 + x_offset, 250 + y_offset),
            "Ararat": (-10600 + x_offset, 300 + y_offset, -10300 + x_offset, 450 + y_offset),
            "Creswick": (-9000 + x_offset, -200 + y_offset, -8500 + x_offset, -50 + y_offset),
            "Clunes": (-8950 + x_offset, -400 + y_offset, -8600 + x_offset, -250 + y_offset),
            "Talbot": (-9000 + x_offset, -600 + y_offset, -8650 + x_offset, -450 + y_offset),
            "Maryborough": (-9400 + x_offset, -950 + y_offset, -8750 + x_offset, -800 + y_offset),
            "Macaulay": (3074 + x_offset, -648 + y_offset, 3518 + x_offset, -512 + y_offset),
            "Flemington Bridge": (3050 + x_offset, -850 + y_offset, 3999 + x_offset, -701 + y_offset),
            "Royal Park": (3071 + x_offset, -1035 + y_offset, 3582 + x_offset, -911 + y_offset),
            "Jewell": (3064 + x_offset, -1246 + y_offset, 3414 + x_offset, -1108 + y_offset),
            "Brunswick": (3071 + x_offset, -1429 + y_offset, 3567 + x_offset, -1334 + y_offset),
            "Anstey": (3086 + x_offset, -1640 + y_offset, 3421 + x_offset, -1523 + y_offset),
            "Moreland": (3071 + x_offset, -1837 + y_offset, 3516 + x_offset, -1713 + y_offset),
            "Coburg": (3071 + x_offset, -2056 + y_offset, 3436 + x_offset, -1917 + y_offset),
            "Batman": (3086 + x_offset, -2223 + y_offset, 3429 + x_offset, -2129 + y_offset),
            "Merlynston": (3057 + x_offset, -2435 + y_offset, 3596 + x_offset, -2311 + y_offset),
            "Fawkner": (3064 + x_offset, -2632 + y_offset, 3487 + x_offset, -2522 + y_offset),
            "Gowrie": (3071 + x_offset, -2836 + y_offset, 3436 + x_offset, -2712 + y_offset),
            "Upfield": (2780 + x_offset, -3171 + y_offset, 3144 + x_offset, -3033 + y_offset),
            "Kensington": (2074 + x_offset, -749 + y_offset, 2620 + x_offset, -619 + y_offset),
            "Newmarket": (2083 + x_offset, -943 + y_offset, 2620 + x_offset, -823 + y_offset),
            "Showgrounds": (990 + x_offset, -1221 + y_offset, 1629 + x_offset, -1091 + y_offset),
            "Flemington Racecourse": (287 + x_offset, -1101 + y_offset, 870 + x_offset, -860 + y_offset),
            "Ascot Vale": (2083 + x_offset, -1128 + y_offset, 2601 + x_offset, -1008 + y_offset),
            "Moonee Ponds": (2064 + x_offset, -1332 + y_offset, 2768 + x_offset, -1212 + y_offset),
            "Essendon": (2083 + x_offset, -1526 + y_offset, 2537 + x_offset, -1406 + y_offset),
            "Glenbervie": (2074 + x_offset, -1730 + y_offset, 2583 + x_offset, -1610 + y_offset),
            "Strathmore": (2083 + x_offset, -1934 + y_offset, 2629 + x_offset, -1795 + y_offset),
            "Pascoe Vale": (2064 + x_offset, -2138 + y_offset, 2666 + x_offset, -2008 + y_offset),
            "Oak Park": (2083 + x_offset, -2341 + y_offset, 2499 + x_offset, -2202 + y_offset),
            "Glenroy": (2074 + x_offset, -2536 + y_offset, 2453 + x_offset, -2406 + y_offset),
            "Jacana": (2074 + x_offset, -2721 + y_offset, 2435 + x_offset, -2610 + y_offset),
            "Broadmeadows":(2050 + x_offset, -3000 + y_offset, 2799 + x_offset, -2851 + y_offset),
            "Coolaroo": (2050 + x_offset, -3150 + y_offset, 2499 + x_offset, -3001 + y_offset),
            "Roxburgh Park": (2050 + x_offset, -3450 + y_offset, 2499 + x_offset, -3151 + y_offset),
            "Craigieburn": (2064 + x_offset, -3593 + y_offset, 2629 + x_offset, -3473 + y_offset),
            "Donnybrook": (1981 + x_offset, -3797 + y_offset, 2546 + x_offset, -3658 + y_offset),
            "Wallan": (1981 + x_offset, -3991 + y_offset, 2324 + x_offset, -3871 + y_offset),
            "Heathcote Junction": (1981 + x_offset, -4186 + y_offset, 2888 + x_offset, -4065 + y_offset),
            "Wandong": (1981 + x_offset, -4426 + y_offset, 2435 + x_offset, -4251 + y_offset),
            "Kilmore East": (1981 + x_offset, -4584 + y_offset, 2564 + x_offset, -4473 + y_offset),
            "Broadford": (1981 + x_offset, -4778 + y_offset, 2453 + x_offset, -4676 + y_offset),
            "Tallarook": (1990 + x_offset, -4982 + y_offset, 2416 + x_offset, -4852 + y_offset),
            "Seymour": (1037 + x_offset, -5213 + y_offset, 1518 + x_offset, -5038 + y_offset),
            "Nagambie": (1800 + x_offset, -5550 + y_offset, 2249 + x_offset, -5401 + y_offset),
            "Murchison East": (1800 + x_offset, -5700 + y_offset, 2549 + x_offset, -5701 + y_offset),
            "Mooroopna": (1800 + x_offset, -6000 + y_offset, 2399 + x_offset, -5851 + y_offset),
            "Shepparton": (1500 + x_offset, -6300 + y_offset, 2099 + x_offset, -6151 + y_offset),
            "Avenel": (2400 + x_offset, -5250 + y_offset, 2849 + x_offset, -5101 + y_offset),
            "Euroa": (2850 + x_offset, -5250 + y_offset, 3149 + x_offset, -5101 + y_offset),
            "Violet Town": (3150 + x_offset, -5250 + y_offset, 3749 + x_offset, -5101 + y_offset),
            "Benalla": (3750 + x_offset, -5250 + y_offset, 4199 + x_offset, -5101 + y_offset),
            "Wangaratta": (4200 + x_offset, -5250 + y_offset, 4799 + x_offset, -4801 + y_offset),
            "Springhurst": (4800 + x_offset, -5250 + y_offset, 5399 + x_offset, -5101 + y_offset),
            "Chiltern": (5400 + x_offset, -5100 + y_offset, 5699 + x_offset, -5101 + y_offset),
            "Wodonga": (5800 + x_offset, -5250 + y_offset, 6250 + x_offset, -4800 + y_offset),
            "Albury": (6250 + x_offset, -5400 + y_offset, 6700 + x_offset, -5100 + y_offset),
        }
        
        self.line_coordinates = {
            'standard_guage': {
                ('Broadmeadows','Seymour'): [
                    (1600 + x_offset, -4900 + y_offset, 1649 + x_offset, -2951 + y_offset),
                    (1550 + x_offset, -5050 + y_offset, 1949 + x_offset, -4901 + y_offset),
                    (1550 + x_offset, -2950 + y_offset, 2049 + x_offset, -2801 + y_offset),
                    ]
            },
            'cross_city': {
                ('Werribee', 'Hoppers Crossing'):[
                    (-4450 + x_offset, 1050 + y_offset, -3951 + x_offset, 1199 + y_offset),
                ],
                ('Hoppers Crossing', 'Williams Landing'):[
                    (-4000 + x_offset, 1050 + y_offset, -3101 + x_offset, 1149 + y_offset),
                ],
                ('Williams Landing','Aircraft'): [
                    (-3150 + x_offset, 1050 + y_offset, -2501 + x_offset, 1199 + y_offset),
                ],
                ('Aircraft', 'Laverton'):[
                    (-2550 + x_offset, 1050 + y_offset, -2001 + x_offset, 1199 + y_offset),
                ],
                ('Laverton', 'Newport'):[ # express route
                    (-2150 + x_offset, 1050 + y_offset, -2001 + x_offset, 1199 + y_offset),
                    (-2000 + x_offset, 1100 + y_offset, -651 + x_offset, 1149 + y_offset),
                    (-750 + x_offset, 900 + y_offset, -601 + x_offset, 1149 + y_offset),
                ],
                ('Westona', 'Laverton'):[
                    (-2000 + x_offset, 1100 + y_offset, -1901 + x_offset, 1249 + y_offset),
                    (-1950 + x_offset, 1200 + y_offset, -1801 + x_offset, 1299 + y_offset),
                ],
                ('Westona', 'Altona'):[
                    (-1850 + x_offset, 1200 + y_offset, -1401 + x_offset, 1299 + y_offset),
                ],
                ('Altona', 'Seaholme'):[
                    (-1450 + x_offset, 1200 + y_offset, -951 + x_offset, 1299 + y_offset),
                ],
                ('Seaholme','Newport'):[
                    (-1000 + x_offset, 1200 + y_offset, -701 + x_offset, 1299 + y_offset),
                    (-700 + x_offset, 1050 + y_offset, -651 + x_offset, 1249 + y_offset),
                    (-750 + x_offset, 900 + y_offset, -601 + x_offset, 1049 + y_offset),
                ],
                ('Newport', 'Spotswood'):[
                    (-750 + x_offset, 750 + y_offset, -601 + x_offset, 1049 + y_offset),
                ],
                ('Spotswood','Yarraville'):[
                    (-750 + x_offset, 550 + y_offset, -651 + x_offset, 799 + y_offset),
                ],
                ('Seddon', 'Yarraville'):[
                    (-750 + x_offset, 350 + y_offset, -651 + x_offset, 599 + y_offset),
                ],
                ('Seddon', 'Footscray'):[
                    (-600 + x_offset, -200 + y_offset, -451 + x_offset, 149 + y_offset), # footscray station icon
                    (-550 + x_offset, 100 + y_offset, -501 + x_offset, 249 + y_offset), # footscray station icon
                    (-600 + x_offset, 200 + y_offset, -451 + x_offset, 349 + y_offset), # footscray station icon
                    (-750 + x_offset, 250 + y_offset, -601 + x_offset, 399 + y_offset),
                ],
                ('Footscray','South Kensington'):[
                    (-600 + x_offset, -200 + y_offset, -451 + x_offset, 149 + y_offset), # footscray station icon
                    (-550 + x_offset, 100 + y_offset, -501 + x_offset, 249 + y_offset), # footscray station icon
                    (-600 + x_offset, 200 + y_offset, -451 + x_offset, 349 + y_offset), # footscray station icon
                    (-450 + x_offset, 250 + y_offset, 99 + x_offset, 349 + y_offset),
                ],
                ('South Kensington', 'North Melbourne'):[
                    (50 + x_offset, 250 + y_offset, 1299 + x_offset, 349 + y_offset),
                    (1200 + x_offset, 350 + y_offset, 1349 + x_offset, 499 + y_offset), # North Melbourne icon
                    (1300 + x_offset, 400 + y_offset, 1649 + x_offset, 449 + y_offset), # North Melbourne icon
                    (1600 + x_offset, 350 + y_offset, 2049 + x_offset, 499 + y_offset), # North Melbourne icon
                ],
                ('North Melbourne', 'Southern Cross'):[
                    (1250 + x_offset, 500 + y_offset, 1299 + x_offset, 1249 + y_offset),
                    (1200 + x_offset, 1250 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
                ],
                ('Southern Cross', 'Flinders Street'):[
                    (1250 + x_offset, 1400 + y_offset, 1299 + x_offset, 2449 + y_offset),
                    (1250 + x_offset, 2400 + y_offset, 2899 + x_offset, 2449 + y_offset),
                    (2900 + x_offset, 1750 + y_offset, 3049 + x_offset, 2699 + y_offset), # Flinders Street icon
                    (1200 + x_offset, 1250 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
                ],
                # Williamstown Branch
                ('Newport', 'North Williamstown'):[
                    (-750.0 + x_offset, 1050.0 + y_offset, -601.0 + x_offset, 1349.0 + y_offset),
                ],
                ('North Williamstown', 'Williamstown Beach'):[
                    (-750.0 + x_offset, 1350.0 + y_offset, -601.0 + x_offset, 1499.0 + y_offset),
                ],
                ('Williamstown Beach', 'Williamstown'):[
                    (-750.0 + x_offset, 1500.0 + y_offset, -601.0 + x_offset, 1799.0 + y_offset),
                ],
                
                
            },
            "burnley": {
            ('Lilydale', 'Mooroolbark'): [
                (6450 + x_offset, -2100 + y_offset, 6600 + x_offset, -1850 + y_offset),
            ],
            ("Flagstaff", "Melbourne Central"):[
                (2500 + x_offset, 800 + y_offset, 2901 + x_offset, 852 + y_offset),
                (2350 + x_offset, 650 + y_offset, 2500 + x_offset, 1150 + y_offset), # Flagstaff Coords
                (2900 + x_offset, 650 + y_offset, 3050 + x_offset, 1150 + y_offset), # Melbourne Central Coords
            ],
            ('Melbourne Central', 'Parliament'):[
                (3050 + x_offset, 800 + y_offset, 3400 + x_offset, 850 + y_offset),
                (3300 + x_offset, 800 + y_offset, 3400 + x_offset, 1250 + y_offset),
                (2900 + x_offset, 650 + y_offset, 3050 + x_offset, 1150 + y_offset), # Melbourne Central Coords
                (3050 + x_offset, 1250 + y_offset, 3600 + x_offset, 1400 + y_offset), # Parliament Coords

            ],
            ('Parliament', 'Richmond'):[
                (3050 + x_offset, 1250 + y_offset, 3600 + x_offset, 1400 + y_offset),
                (3300 + x_offset, 1950 + y_offset, 3500 + x_offset, 2050 + y_offset),
                (3550 + x_offset, 2000 + y_offset, 4450 + x_offset, 2050 + y_offset),
                (3050 + x_offset, 1250 + y_offset, 3600 + x_offset, 1400 + y_offset), # Parliament Coords
                (4450 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # Richmond Coords
            ],
                
            ('Richmond','Flinders Street'):[
                (3550 + x_offset, 2000 + y_offset, 4499 + x_offset, 2049 + y_offset),
                (3050 + x_offset, 2000 + y_offset, 3499 + x_offset, 2059 + y_offset),
            ],
            },
            
            'northern': {
            # ('Sunbury', 'Diggers Rest'): [
            #     (-3350 + x_offset, -1850 + y_offset, -3000 + x_offset, -1700 + y_offset), # Sunbury Coords
            #     (-3100 + x_offset, -1700 + y_offset, -3000 + x_offset, -1550 + y_offset),
            # ],
            # ('Diggers Rest', 'Watergardens'): [
            #     (2450 + x_offset, 1400 + y_offset, 2550 + x_offset, 1400 + y_offset), # Watergardens Coords
            # ],
            
            ('Tottanham', 'West Footscray'): [
                (2450 + x_offset, 1400 + y_offset, 2550 + x_offset, 1400 + y_offset),
            ],
            
            ('North Melbourne', 'Footscray'): [
                (1916 + x_offset, -147 + y_offset, 2027 + x_offset, 344 + y_offset),
                (-450 + x_offset, -157 + y_offset, 1949 + x_offset, -99 + y_offset),
            ],
            },
              
            'flemington': {
                ('Flinders Street','Southern Cross'): [
                    (2900 + x_offset, 1750 + y_offset, 3049 + x_offset, 2699 + y_offset), # Flinders Street icon
                    (1200 + x_offset, 1250 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
                    (1650 + x_offset, 2550 + y_offset, 2849 + x_offset, 2699 + y_offset),
                    (1612 + x_offset, 2451 + y_offset, 1708 + x_offset, 2688 + y_offset),
                    (1621 + x_offset, 1398 + y_offset, 1708 + x_offset, 2388 + y_offset),
                    ],
                ('Southern Cross','North Melbourne'): [
                    (1200 + x_offset, 1250 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
                    (1633 + x_offset, 909 + y_offset, 1708 + x_offset, 1239 + y_offset),
                    (1621 + x_offset, 747 + y_offset, 1696 + x_offset, 834 + y_offset),
                    (1621 + x_offset, 492 + y_offset, 1717 + x_offset, 684 + y_offset),
                    (1200 + x_offset, 350 + y_offset, 1349 + x_offset, 499 + y_offset), # North Melbourne icon
                    (1300 + x_offset, 400 + y_offset, 1649 + x_offset, 449 + y_offset), # North Melbourne icon
                    (1600 + x_offset, 350 + y_offset, 2049 + x_offset, 499 + y_offset), # North Melbourne icon
                    
                ],
                ('North Melbourne','Showgrounds'): [
                    (1621 + x_offset, 492 + y_offset, 1717 + x_offset, 684 + y_offset),
                    (1612 + x_offset, -100 + y_offset, 1708 + x_offset, 345 + y_offset),
                    (1633 + x_offset, -1020 + y_offset, 1717 + x_offset, -156 + y_offset),
                    (1300 + x_offset, -1050 + y_offset, 1700 + x_offset, -900 + y_offset),
                    (1200 + x_offset, 350 + y_offset, 1349 + x_offset, 499 + y_offset), # North Melbourne icon
                    (1300 + x_offset, 400 + y_offset, 1649 + x_offset, 449 + y_offset), # North Melbourne icon
                    (1600 + x_offset, 350 + y_offset, 2049 + x_offset, 499 + y_offset), # North Melbourne icon
                ],
                ('Showgrounds','Flemington Racecourse'): [
                    (900 + x_offset, -1050 + y_offset, 1350 + x_offset, -900 + y_offset),
                    ],
            },
            }
        self.station_order = station_order_dictionary
        self.map_image = Image.open(map_image_path)
        print('Initalised the map maker')
        
    def highlight_map(self, station_pairs, output_path, stations):
        """
        Creates a white cover over the entire map except for holes where the stations and lines are
        
        Args:
            station_pairs (list): List of tuples containing station pairs and line name (station1, station2, line)
            output_path (str): Path where the modified image will be saved
        """
        # Create a copy of the original image
        modified_map = self.map_image.copy()
        
        # Create a white overlay
        overlay = Image.new('RGBA', modified_map.size, 'white')
        draw = ImageDraw.Draw(overlay)
        
        # Get unique stations from pairs
        affected_stations = set()
        for station1, station2, _ in station_pairs:
            affected_stations.add(station1)
            affected_stations.add(station2)
        
        # Create holes for stations
        for station in stations:
            if station in self.station_coordinates:
                coords = self.station_coordinates[station]
                if isinstance(coords, list):
                    for coord in coords:
                        coord2 = []
                        for coor in coord:
                            coor = coor * dpi
                            coord2.append(coor)
                        coord = tuple(coord2)
                        draw.rectangle(coord, fill=(255, 255, 255, 0))
                else:
                    coord2 = []
                    for coor in coords:
                        coor = coor * dpi
                        coord2.append(coor)
                    coord = tuple(coord2)
                    draw.rectangle(coord, fill=(255, 255, 255, 0))
                print(f'Created hole for {station}')
            else:
                print(f'No coordinates for {station}')

        # for testing only, comment out when finished
        '''for station in self.station_coordinates:
            coords = self.station_coordinates[station]
            if isinstance(coords, list):
                for coord in coords:
                    coord2 = []
                        for coor in coord:
                            coor = coor * dpi
                            coord2.append(coor)
                        coord = tuple(coord2)
                    draw.rectangle(coord, fill=(255, 255, 255, 0))
            else:
                coord2 = []
                for coor in coords:
                    coor = coor * dpi
                    coord2.append(coor)
                coords = tuple(coord2)
                draw.rectangle(coords, fill=(255, 255, 255, 0))
            print(f'Created hole for {station}')'''
        
        # Create holes for lines
        for station1, station2, line in station_pairs:
            if line in self.line_coordinates:
                for station_pair, coords in self.line_coordinates[line].items():
                    if (station_pair[0] == station1 and station_pair[1] == station2) or \
                       (station_pair[0] == station2 and station_pair[1] == station1):
                        if isinstance(coords, list):
                            for coord in coords:
                                coord2 = []
                                for coor in coord:
                                    coor = coor * dpi
                                    coord2.append(coor)
                                coord = tuple(coord2)
                                draw.rectangle(coord, fill=(255, 255, 255, 0))
                        else:
                            coord2 = []
                            for coor in coords:
                                coor = coor * dpi
                                coord2.append(coor)
                            coords = tuple(coord2)
                            draw.rectangle(coords, fill=(255, 255, 255, 0))
                        print(f'Created line hole from {station1} to {station2}')
                    # else:
                    #     print(f'No line coordinates for {station1} to {station2}')
        
        # Composite and save
        modified_map = Image.alpha_composite(modified_map.convert('RGBA'), overlay)
        modified_map.save(output_path)
        return modified_map
        
        

        


class CoordinateFinder:
    def __init__(self, image_path):
        self.root = tk.Tk()
        self.original_image = Image.open(image_path)
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate scaling factor
        width_ratio = screen_width / self.original_image.width
        height_ratio = screen_height / self.original_image.height
        self.scale = min(width_ratio * 0.8, height_ratio * 0.8)  # 80% of screen size
        
        # Resize image
        new_width = int(self.original_image.width * self.scale)
        new_height = int(self.original_image.height * self.scale)
        self.image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        
        self.canvas = tk.Canvas(self.root, width=new_width, height=new_height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y
        
    def on_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y, outline="red"
        )
        
    def on_release(self, event):
        # Convert coordinates back to original scale
        x1 = int(min(self.start_x, event.x) / self.scale)
        y1 = int(min(self.start_y, event.y) / self.scale)
        x2 = int(max(self.start_x, event.x) / self.scale) 
        y2 = int(max(self.start_y, event.y) / self.scale)
        # Swap y coordinates to ensure y2 is greater than y1
        y1_adj = round(int(max((y1 / dpi) - y_offset, (y2 / dpi) - y_offset)) / 50) * 50
        y2_adj = round(int(min((y1 / dpi) - y_offset, (y2 / dpi) - y_offset)) / 50) * 50
        x1_adj = round(int((x1 / dpi) - x_offset) / 50) * 50  
        x2_adj = round(int((x2 / dpi) - x_offset) / 50) * 50
        print(f"Coordinates: ({x1_adj}, {y2_adj}, {x2_adj}, {y1_adj})")
        print(f"Copyable: ({x1_adj} + x_offset, {y2_adj} + y_offset, {x2_adj} + x_offset, {y1_adj} + y_offset),")
    def run(self):
        self.root.mainloop()

# Run coord finder if this script is run
if __name__ == "__main__":
    finder = CoordinateFinder("utils/trainlogger/map/log_train_map.png")
    finder.run()
from PIL import Image, ImageDraw, ImageChops
import tkinter as tk
from PIL import ImageTk
from matplotlib.pylab import f
import math
from utils.trainlogger.map.station_coordinates import station_coordinates

dpi = 32/96
padding = 1.2

def compress(image: Image):
    print("Compressing Image")
    try:
        success = False
        while success == False:
            if image.size[0] > 10000 or image.size[1] > 10000:
                image = image.resize((round(image.size[0] / 2), round(image.size[1] / 2)))
            else:
                print("Image Compressed")
                success = True
                return image
    except Exception as e:
        print(e)

class MapImageHandler:
    def __init__(self, map_image_path, station_order_dictionary):
        self.line_coordinates = {
            'standard_guage': {
                ('Albury', 'Wodonga'): [
                    (6000 + x_offset, -5400 + y_offset, 6300 + x_offset, -5200 + y_offset),
                ],
                ('Wodonga', 'Chiltern'): [
                    (5550 + x_offset, -5300 + y_offset, 6050 + x_offset, -5200 + y_offset),
                ],
                ('Chiltern', 'Springhurst'): [
                    (5000 + x_offset, -5350 + y_offset, 5600 + x_offset, -5200 + y_offset),
                ],
                ('Springhurst', 'Wangaratta'): [
                    (4450 + x_offset, -5350 + y_offset, 5100 + x_offset, -5200 + y_offset),
                ],  
                ('Wangaratta', 'Benalla'): [
                    (3950 + x_offset, -5350 + y_offset, 4500 + x_offset, -5200 + y_offset),
                ],
                ('Benalla', 'Violet Town'): [
                    (3450 + x_offset, -5350 + y_offset, 4000 + x_offset, -5200 + y_offset),
                ],
                ('Violet Town', 'Euroa'): [
                    (3000 + x_offset, -5350 + y_offset, 3500 + x_offset, -5200 + y_offset),
                ],
                ('Euroa', 'Avenel'): [
                    (2600 + x_offset, -5350 + y_offset, 3050 + x_offset, -5200 + y_offset),
                ],
                ('Avenel', 'Seymour'): [
                    (1800 + x_offset, -5400 + y_offset, 2650 + x_offset, -5200 + y_offset),
                    (1600 + x_offset, -5300 + y_offset, 1750 + x_offset, -5200 + y_offset),
                    (1550 + x_offset, -5200 + y_offset, 1950 + x_offset, -5050 + y_offset), # seymour station icon
                ],
                
                
                
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
            ('Mooroolbark', 'Croydon'): [
                (6500 + x_offset, -1950 + y_offset, 6600 + x_offset, -1650 + y_offset),
            ],
            ('Croydon', 'Ringwood East'): [
                (6450 + x_offset, -1750 + y_offset, 6600 + x_offset, -1450 + y_offset),
            ],
            ('Ringwood East', 'Ringwood'): [
                (6450 + x_offset, -1450 + y_offset, 6550 + x_offset, -1200 + y_offset),
                (6450 + x_offset, -1250 + y_offset, 6600 + x_offset, -1050 + y_offset),
            ],
            ('Ringwood', 'Heatherdale'): [
                (6450 + x_offset, -1200 + y_offset, 6600 + x_offset, -900 + y_offset),
            ],
            ('Heatherdale', 'Mitcham'): [
                (6450 + x_offset, -950 + y_offset, 6600 + x_offset, -700 + y_offset),
            ],
            ('Mitcham', 'Nunawading'): [
                (6450 + x_offset, -750 + y_offset, 6600 + x_offset, -500 + y_offset),
            ],
            ('Nunawading', 'Blackburn'): [
                (6450 + x_offset, -600 + y_offset, 6600 + x_offset, -300 + y_offset),
            ],
            ('Blackburn', 'Laburnum'): [
                (6500 + x_offset, -400 + y_offset, 6600 + x_offset, -100 + y_offset),
            ],
            ('Laburnum', 'Box Hill'): [
                (6500 + x_offset, -200 + y_offset, 6600 + x_offset, 100 + y_offset),
            ],
            ('Box Hill', 'Union'): [
                (6500 + x_offset, 50 + y_offset, 6600 + x_offset, 300 + y_offset),
            ],
            ('Union', 'Chatham') : [
                (6500 + x_offset, 250 + y_offset, 6600 + x_offset, 500 + y_offset),
            ],
            ('Chatham', 'Canterbury') : [
                (6500 + x_offset, 450 + y_offset, 6600 + x_offset, 700 + y_offset),
            ],
            ('Canterbury', 'East Camberwell') : [
                (6500 + x_offset, 600 + y_offset, 6600 + x_offset, 900 + y_offset),
            ],
            ('East Camberwell', 'Camberwell') : [
                (6500 + x_offset, 800 + y_offset, 6600 + x_offset, 950 + y_offset),
                (6450 + x_offset, 1150 + y_offset, 6600 + x_offset, 1300 + y_offset),
                (6500 + x_offset, 900 + y_offset, 6550 + x_offset, 1150 + y_offset),
            ],
            ('Camberwell', 'Auburn') : [
                (6400 + x_offset, 1150 + y_offset, 6600 + x_offset, 1450 + y_offset),
            ],
            ('Auburn', 'Glenferrie') : [
                (6450 + x_offset, 1350 + y_offset, 6600 + x_offset, 1650 + y_offset),
            ],
            ('Glenferrie', 'Hawthorn') : [
                (6500 + x_offset, 1600 + y_offset, 6600 + x_offset, 1850 + y_offset),
            ],
            ('Hawthorn', 'Burnley') : [
                (6200 + x_offset, 1950 + y_offset, 6550 + x_offset, 2050 + y_offset),
                (6200 + x_offset, 2000 + y_offset, 6350 + x_offset, 2100 + y_offset),
                (6500 + x_offset, 1750 + y_offset, 6600 + x_offset, 2000 + y_offset),
            ],
            ('Burnley', 'East Richmond') : [
                (5650 + x_offset, 1900 + y_offset, 6350 + x_offset, 2100 + y_offset),
            ],
            ('East Richmond', 'Richmond') : [
                (4650 + x_offset, 1950 + y_offset, 5700 + x_offset, 2050 + y_offset),
                (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # richmond coords
            ],
            ('Richmond','Flinders Street'):[
                (3550 + x_offset, 2000 + y_offset, 4499 + x_offset, 2049 + y_offset),
                (3050 + x_offset, 2000 + y_offset, 3499 + x_offset, 2059 + y_offset),
                (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # richmond coords
                (2900 + x_offset, 1750 + y_offset, 3049 + x_offset, 2699 + y_offset), # Flinders Street icon
            ],
            ('Flinders Street', 'Southern Cross'):[
                (2050 + x_offset, 1400 + y_offset, 2100 + x_offset, 2050 + y_offset),
                (2050 + x_offset, 1950 + y_offset, 2900 + x_offset, 2050 + y_offset),
                (2900 + x_offset, 1750 + y_offset, 3049 + x_offset, 2699 + y_offset), # Flinders Street icon
                (1200 + x_offset, 1250 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
            ],
            ('Southern Cross', 'Flagstaff'):[
                (2050 + x_offset, 800 + y_offset, 2350 + x_offset, 850 + y_offset),
                (2000 + x_offset, 800 + y_offset, 2100 + x_offset, 1250 + y_offset),
                (1200 + x_offset, 1250 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
                (2350 + x_offset, 650 + y_offset, 2500 + x_offset, 1150 + y_offset), # Flagstaff Coords
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
            ('Flinders Street', 'Richmond'):[
                (3050 + x_offset, 2000 + y_offset, 3500 + x_offset, 2050 + y_offset),
                (3550 + x_offset, 2000 + y_offset, 4500 + x_offset, 2050 + y_offset),
                (2900 + x_offset, 1750 + y_offset, 3049 + x_offset, 2699 + y_offset), # Flinders Street icon
                (4450 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # Richmond Coords
                
            ],
            
            # alamein branch
            ('Alamein', 'Ashburton'):[
                (9400 + x_offset, 950 + y_offset, 9750 + x_offset, 1150 + y_offset),
            ],
            ('Ashburton','Burwood'):[
                (8900 + x_offset, 1050 + y_offset, 9450 + x_offset, 1150 + y_offset),
            ],
            ('Burwood', 'Hartwell'):[
                (8450 + x_offset, 1050 + y_offset, 8950 + x_offset, 1150 + y_offset),
            ],
            ('Hartwell', 'Willison'):[
                (8000 + x_offset, 1050 + y_offset, 8500 + x_offset, 1150 + y_offset),
            ],
            ('Willison', 'Riversdale'):[
                (7500 + x_offset, 1050 + y_offset, 8050 + x_offset, 1150 + y_offset),
            ],
            ('Riversdale', 'Camberwell'):[
                (6500 + x_offset, 1050 + y_offset, 7550 + x_offset, 1150 + y_offset),
                (6450 + x_offset, 1050 + y_offset, 6600 + x_offset, 1300 + y_offset),
            ],
            
            # the beginning of the belgrave line:
            ('Belgrave', 'Tecoma'):[
                (11000 + x_offset, -1400 + y_offset, 11300 + x_offset, -1200 + y_offset),
            ],
            ('Tecoma', 'Upwey'):[
                (10600 + x_offset, -1350 + y_offset, 11050 + x_offset, -1200 + y_offset),
            ],
            ('Upwey', 'Upper Ferntree Gully'):[
                (9900 + x_offset, -1300 + y_offset, 10650 + x_offset, -1200 + y_offset),
            ],
            ('Upper Ferntree Gully', 'Ferntree Gully'):[
                (9050 + x_offset, -1350 + y_offset, 9950 + x_offset, -1150 + y_offset),
            ],
            ('Ferntree Gully', 'Boronia'):[
                (8500 + x_offset, -1300 + y_offset, 9100 + x_offset, -1200 + y_offset),
            ],
            ('Boronia', 'Bayswater'):[
                (8000 + x_offset, -1300 + y_offset, 8550 + x_offset, -1200 + y_offset),
            ],
            ('Bayswater', 'Heathmont'):[
                (7400 + x_offset, -1300 + y_offset, 8050 + x_offset, -1200 + y_offset),
            ],
            ('Heathmont', 'Ringwood'):[
                (6450 + x_offset, -1200 + y_offset, 6600 + x_offset, -1050 + y_offset),
                (6450 + x_offset, -1300 + y_offset, 7500 + x_offset, -1200 + y_offset),
            ],
            # glen waverley branch
            ('Glen Waverley', 'Syndal'):[
                (12250 + x_offset, 1900 + y_offset, 12600 + x_offset, 2100 + y_offset),
            ],
            ('Syndal', 'Mount Waverley'):[
                (11700 + x_offset, 2000 + y_offset, 12350 + x_offset, 2100 + y_offset),
            ],
            ('Mount Waverley', 'Jordanville'):[
                (11000 + x_offset, 2000 + y_offset, 11750 + x_offset, 2100 + y_offset),
            ],
            ('Jordanville', 'Holmesglen'):[
                (10400 + x_offset, 2000 + y_offset, 11050 + x_offset, 2100 + y_offset),
            ],
            ('Holmesglen', 'East Malvern'):[
                (9750 + x_offset, 2000 + y_offset, 10450 + x_offset, 2100 + y_offset),
            ],
            ('East Malvern', 'Darling'):[
                (9200 + x_offset, 2000 + y_offset, 9800 + x_offset, 2100 + y_offset),
            ],
            ('Darling', 'Glen Iris'):[
                (8800 + x_offset, 2000 + y_offset, 9250 + x_offset, 2100 + y_offset),
            ],
            ('Glen Iris', 'Gardiner'):[
                (8350 + x_offset, 2000 + y_offset, 8850 + x_offset, 2100 + y_offset),
            ],
            ('Gardiner', 'Tooronga'):[
                (7850 + x_offset, 2000 + y_offset, 8400 + x_offset, 2100 + y_offset)
            ],
            ('Tooronga', 'Kooyong'):[
                (7350 + x_offset, 2000 + y_offset, 7900 + x_offset, 2100 + y_offset),
            ],
            ('Kooyong', 'Heyington'):[
                (6850 + x_offset, 2000 + y_offset, 7400 + x_offset, 2100 + y_offset),
            ],
            ('Heyington', 'Burnley'):[
                (6350 + x_offset, 2000 + y_offset, 6900 + x_offset, 2100 + y_offset),
                (6200 + x_offset, 1950 + y_offset, 6350 + x_offset, 2100 + y_offset),
            ],
            },
            'dandenong':{
                ('East Pakenham','Pakenham'): [
                    (15700 + x_offset, 4300 + y_offset, 16000 + x_offset, 4450 + y_offset),
                    (15600 + x_offset, 4300 + y_offset, 15750 + x_offset, 4650 + y_offset), # pakenham coords
                ],
                ('Pakenham','Cardinia Road'): [
                    (15100 + x_offset, 4300 + y_offset, 15600 + x_offset, 4400 + y_offset),
                    (15050 + x_offset, 4300 + y_offset, 15150 + x_offset, 4400 + y_offset),
                    (15600 + x_offset, 4300 + y_offset, 15750 + x_offset, 4650 + y_offset), # pakenham coords
                ],
                ('Cardinia Road','Officer'): [
                    (14500 + x_offset, 4300 + y_offset, 15100 + x_offset, 4400 + y_offset),
                ],
                ('Officer','Beaconsfield'): [
                    (13950 + x_offset, 4300 + y_offset, 14550 + x_offset, 4400 + y_offset),
                ],
                ('Beaconsfield','Berwick'): [
                    (13400 + x_offset, 4300 + y_offset, 14000 + x_offset, 4400 + y_offset),
                ],
                ('Berwick','Narre Warren'): [
                    (12850 + x_offset, 4300 + y_offset, 13450 + x_offset, 4400 + y_offset),
                ],
                ('Narre Warren','Hallam'): [
                    (12300 + x_offset, 4300 + y_offset, 12900 + x_offset, 4400 + y_offset),
                ],
                ('Hallam','Dandenong'): [
                    (11750 + x_offset, 4300 + y_offset, 11900 + x_offset, 4650 + y_offset), # dandenong coords
                    (11900 + x_offset, 4300 + y_offset, 12350 + x_offset, 4400 + y_offset),
                ],
                ('Dandenong','Yarraman'): [
                    (11250 + x_offset, 4300 + y_offset, 11750 + x_offset, 4400 + y_offset),
                    (11750 + x_offset, 4300 + y_offset, 11900 + x_offset, 4650 + y_offset), # dandenong coords
                ],
                ('Yarraman','Noble Park'): [
                    (10700 + x_offset, 4300 + y_offset, 11300 + x_offset, 4400 + y_offset),
                ],
                ('Noble Park','Sandown Park'): [
                    (10050 + x_offset, 4300 + y_offset, 10750 + x_offset, 4400 + y_offset),
                ],
                ('Sandown Park','Springvale'): [
                    (9400 + x_offset, 4300 + y_offset, 10100 + x_offset, 4400 + y_offset),
                ],
                ('Springvale','Westall'): [
                    (8900 + x_offset, 4300 + y_offset, 9450 + x_offset, 4400 + y_offset),
                ],
                ('Westall','Clayton'): [
                    (8400 + x_offset, 4300 + y_offset, 8550 + x_offset, 4650 + y_offset), # clayton coords
                    (8550 + x_offset, 4300 + y_offset, 8950 + x_offset, 4400 + y_offset),
                ],
                ('Clayton','Huntingdale'): [
                    (7950 + x_offset, 4300 + y_offset, 8400 + x_offset, 4400 + y_offset),
                    (8400 + x_offset, 4300 + y_offset, 8550 + x_offset, 4650 + y_offset), # clayton coords
                ],
                ('Huntingdale','Oakleigh'): [
                    (7400 + x_offset, 4300 + y_offset, 8000 + x_offset, 4400 + y_offset),
                ],
                ('Oakleigh','Hughesdale'): [
                    (6850 + x_offset, 4300 + y_offset, 7450 + x_offset, 4400 + y_offset),
                ],
                ('Hughesdale','Murrumbeena'): [
                    (6200 + x_offset, 4300 + y_offset, 6900 + x_offset, 4400 + y_offset),
                ],
                ('Murrumbeena','Carnegie'): [
                    (5600 + x_offset, 4300 + y_offset, 6250 + x_offset, 4400 + y_offset),
                ],
                ('Carnegie','Caulfield'): [
                    (4900 + x_offset, 4150 + y_offset, 5350 + x_offset, 4300 + y_offset), # caulfield coords
                    (5250 + x_offset, 4300 + y_offset, 5650 + x_offset, 4400 + y_offset),
                ],
                ('Caulfield','Malvern'): [
                    (5250 + x_offset, 4000 + y_offset, 5300 + x_offset, 4150 + y_offset),
                ],
                ('Malvern','South Yarra'): [
                    (5250 + x_offset, 2950 + y_offset, 5300 + x_offset, 4000 + y_offset),
                    (4800 + x_offset, 2800 + y_offset, 5000 + x_offset, 2950 + y_offset), # south yarra coords
                    (5000 + x_offset, 2850 + y_offset, 5250 + x_offset, 2900 + y_offset), # south yarra coords
                    (5200 + x_offset, 2800 + y_offset, 5350 + x_offset, 2950 + y_offset), # south yarra coords
                ],
                ('South Yarra','Richmond'): [
                    (4650 + x_offset, 2100 + y_offset, 5300 + x_offset, 2150 + y_offset),
                    (5250 + x_offset, 2100 + y_offset, 5300 + x_offset, 2800 + y_offset),
                    (4800 + x_offset, 2800 + y_offset, 5000 + x_offset, 2950 + y_offset), # south yarra coords
                    (5000 + x_offset, 2850 + y_offset, 5250 + x_offset, 2900 + y_offset), # south yarra coords
                    (5200 + x_offset, 2800 + y_offset, 5350 + x_offset, 2950 + y_offset), # south yarra coords
                    (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # richmond coords
                ],
                ('Richmond','Flinders Street'): [
                    (3050 + x_offset, 2100 + y_offset, 4550 + x_offset, 2150 + y_offset),
                    (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # richmond coords
                    (2900 + x_offset, 1750 + y_offset, 3049 + x_offset, 2699 + y_offset), # Flinders Street icon
                ],
                ('Flinders Street','Southern Cross'): [
                    (1950 + x_offset, 2100 + y_offset, 2900 + x_offset, 2150 + y_offset),
                    (1950 + x_offset, 1400 + y_offset, 2000 + x_offset, 2150 + y_offset),
                    (2900 + x_offset, 1750 + y_offset, 3049 + x_offset, 2699 + y_offset), # Flinders Street icon
                    (1200 + x_offset, 1250 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
                ],
                ('Southern Cross','Flagstaff'): [
                    (1200 + x_offset, 1250 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern Cross icon
                    (1950 + x_offset, 700 + y_offset, 2000 + x_offset, 1250 + y_offset),
                    (1950 + x_offset, 700 + y_offset, 2350 + x_offset, 750 + y_offset),
                    (2350 + x_offset, 650 + y_offset, 2500 + x_offset, 1150 + y_offset), # Flagstaff Coords
                ],
                ('Flagstaff','Melbourne Central'): [
                    (2350 + x_offset, 650 + y_offset, 2500 + x_offset, 1150 + y_offset), # Flagstaff Coords
                    (2500 + x_offset, 650 + y_offset, 2900 + x_offset, 750 + y_offset),
                    (2900 + x_offset, 650 + y_offset, 3050 + x_offset, 1150 + y_offset), # Melbourne Central Coords
                ],
                ('Melbourne Central','Parliament'): [
                    (2900 + x_offset, 650 + y_offset, 3050 + x_offset, 1150 + y_offset), # Melbourne Central Coords
                    (3050 + x_offset, 700 + y_offset, 3550 + x_offset, 750 + y_offset),
                    (3450 + x_offset, 700 + y_offset, 3600 + x_offset, 1250 + y_offset),
                    (3050 + x_offset, 1250 + y_offset, 3600 + x_offset, 1400 + y_offset), # Parliament Coord
                ],
                ('Parliament','Richmond'): [
                    (3050 + x_offset, 1250 + y_offset, 3600 + x_offset, 1400 + y_offset), # Parliament Coord
                    (3500 + x_offset, 1400 + y_offset, 3550 + x_offset, 2150 + y_offset),
                    (3500 + x_offset, 2100 + y_offset, 4500 + x_offset, 2150 + y_offset),
                    (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # Richmond Coords
                ],
                # cranbourne branch
                ('Cranbourne','Merinda Park'): [
                    (11950 + x_offset, 4950 + y_offset, 12100 + x_offset, 5200 + y_offset),
                ],
                ('Merinda Park','Lynbrook'): [
                    (11950 + x_offset, 4700 + y_offset, 12100 + x_offset, 5000 + y_offset),
                ],
                ('Lynbrook','Dandenong'): [
                    (12000 + x_offset, 4350 + y_offset, 12050 + x_offset, 4800 + y_offset),
                    (12000 + x_offset, 4700 + y_offset, 12100 + x_offset, 4800 + y_offset),
                    (11900 + x_offset, 4350 + y_offset, 12050 + x_offset, 4400 + y_offset),
                    (11750 + x_offset, 4300 + y_offset, 11900 + x_offset, 4650 + y_offset), # dandenong coords
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
            'vline_intercity':{
                # traralgon line
                ('Traralgon','Morwell'): [
                    (21750 + x_offset, 4400 + y_offset, 21900 + x_offset, 4650 + y_offset), # traralgon coords
                    (21350 + x_offset, 4400 + y_offset, 21750 + x_offset, 4500 + y_offset),
                ],
                ('Morwell','Moe'): [
                    (21000 + x_offset, 4350 + y_offset, 21400 + x_offset, 4500 + y_offset),
                ],
                ('Moe','Trafalgar'): [
                    (20650 + x_offset, 4400 + y_offset, 21050 + x_offset, 4500 + y_offset),
                ],
                ('Trafalgar','Yarragon'): [
                    (20200 + x_offset, 4400 + y_offset, 20700 + x_offset, 4500 + y_offset),
                ],  
                ('Yarragon','Warragul'): [
                    (19700 + x_offset, 4400 + y_offset, 20250 + x_offset, 4500 + y_offset),
                ],
                ('Drouin','Warragul'): [
                    (19300 + x_offset, 4400 + y_offset, 19750 + x_offset, 4500 + y_offset),
                ],

                ('Drouin','Longwarry'): [
                    (18850 + x_offset, 4400 + y_offset, 19350 + x_offset, 4500 + y_offset),
                ],
                ('Longwarry','Bunyip'): [
                    (18400 + x_offset, 4400 + y_offset, 18900 + x_offset, 4500 + y_offset),
                ],
                ('Bunyip','Garfield'): [
                    (18000 + x_offset, 4350 + y_offset, 18450 + x_offset, 4500 + y_offset),
                ],
                ('Garfield','Tynong'): [
                    (17600 + x_offset, 4350 + y_offset, 18050 + x_offset, 4500 + y_offset),
                ],
                ('Tynong','Nar Nar Goon'): [
                    (17100 + x_offset, 4400 + y_offset, 17650 + x_offset, 4500 + y_offset),
                ],
                ('Nar Nar Goon','Pakenham'): [
                    (15700 + x_offset, 4450 + y_offset, 17150 + x_offset, 4500 + y_offset),
                    (17100 + x_offset, 4400 + y_offset, 17150 + x_offset, 4500 + y_offset),
                    (15600 + x_offset, 4300 + y_offset, 15750 + x_offset, 4650 + y_offset), # pakenham coords
                ],
 
                ('Pakenham','Berwick'): [
                    (13400 + x_offset, 4400 + y_offset, 13450 + x_offset, 4500 + y_offset),
                    (13450 + x_offset, 4450 + y_offset, 15600 + x_offset, 4500 + y_offset),
                    (15600 + x_offset, 4300 + y_offset, 15750 + x_offset, 4650 + y_offset), # pakenham coords
                ],
                ('Berwick','Dandenong'): [
                    (12050 + x_offset, 4450 + y_offset, 13400 + x_offset, 4500 + y_offset),
                    (13400 + x_offset, 4400 + y_offset, 13450 + x_offset, 4500 + y_offset),
                    (11900 + x_offset, 4400 + y_offset, 12000 + x_offset, 4500 + y_offset),
                    (11750 + x_offset, 4300 + y_offset, 11900 + x_offset, 4650 + y_offset), # dandenong coords
                ],
                ('Dandenong','Clayton'): [
                    (8550 + x_offset, 4400 + y_offset, 11750 + x_offset, 4500 + y_offset),
                    (11750 + x_offset, 4300 + y_offset, 11900 + x_offset, 4650 + y_offset), # dandenong coords
                    (8400 + x_offset, 4300 + y_offset, 8550 + x_offset, 4650 + y_offset), # clayton coords
                ],
                ('Clayton','Caulfield'): [
                    (5150 + x_offset, 4450 + y_offset, 8400 + x_offset, 4500 + y_offset),
                    (5150 + x_offset, 4250 + y_offset, 5200 + x_offset, 4500 + y_offset),
                    (8400 + x_offset, 4300 + y_offset, 8550 + x_offset, 4650 + y_offset), # clayton coords
                    (4900 + x_offset, 4150 + y_offset, 5350 + x_offset, 4300 + y_offset), # caulfield coords
                ],
                ('Caulfield','Richmond'): [
                    (5150 + x_offset, 2900 + y_offset, 5200 + x_offset, 4150 + y_offset),
                    (5100 + x_offset, 2200 + y_offset, 5200 + x_offset, 2850 + y_offset),
                    (4650 + x_offset, 2150 + y_offset, 5200 + x_offset, 2250 + y_offset),
                    (4900 + x_offset, 4150 + y_offset, 5350 + x_offset, 4300 + y_offset), # caulfield coords
                    (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # Richmond Coords
                ],
                ('Richmond','Flinders Street'): [
                    (3050 + x_offset, 2200 + y_offset, 4550 + x_offset, 2250 + y_offset),
                    (4500 + x_offset, 1950 + y_offset, 4650 + x_offset, 2600 + y_offset), # Richmond Coords
                    (2900 + x_offset, 1750 + y_offset, 3049 + x_offset, 2699 + y_offset), # Flinders Street icon
                ],
                ('Flinders Street','Southern Cross'): [
                    (1850 + x_offset, 1350 + y_offset, 1900 + x_offset, 2250 + y_offset),
                    (1800 + x_offset, 2150 + y_offset, 2900 + x_offset, 2250 + y_offset),
                    (2900 + x_offset, 1750 + y_offset, 3049 + x_offset, 2699 + y_offset), # Flinders Street icon
                    (1200 + x_offset, 1250 + y_offset, 2349 + x_offset, 1399 + y_offset), # Southern 
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
            if station in station_coordinates:
                coords = station_coordinates[station]
                if isinstance(coords, list):
                    for coord in coords:
                        coord2 = []
                        for coor in coord:
                            coor = coor * dpi
                            coor = math.trunc(coor)
                            if coor == coord[3] or coor == coord[2]:
                                coor = coor - 1
                            coord2.append(coor)
                        coord = tuple(coord2)
                        draw.rectangle(coord, fill=(255, 255, 255, 0))
                else:
                    coord2 = []
                    for coor in coords:
                        coor = coor * dpi
                        coor = math.trunc(coor)
                        if coor == coords[3] or coor == coords[2]:
                            coor = coor - 1
                        coord2.append(coor)
                    coord = tuple(coord2)
                    draw.rectangle(coord, fill=(255, 255, 255, 0))
                print(f'Created hole for {station}')
            else:
                print(f'No coordinates for {station}')

        # for testing only, comment out when finished
        '''for station in station_coordinates:
            coords = station_coordinates[station]
            if isinstance(coords, list):
                for coord in coords:
                    coord2 = []
                        for coor in coord:
                            coor = coor * dpi
                            coor = math.trunc(coor)
                            if coor == coord[3] or coor == coord[2]:
                                coor = coor - 1
                            coord2.append(coor)
                        coord = tuple(coord2)
                    draw.rectangle(coord, fill=(255, 255, 255, 0))
            else:
                coord2 = []
                for coor in coords:
                    coor = coor * dpi
                    coor = math.trunc(coor)
                    if coor == coords[3] or coor == coords[2]:
                        coor = coor - 1
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
                                    coor = math.trunc(coor)
                                    if coor == coord[3] or coor == coord[2]:
                                        coor = coor - 1
                                    coord2.append(coor)
                                coord = tuple(coord2)
                                draw.rectangle(coord, fill=(255, 255, 255, 0))
                        else:
                            coord2 = []
                            for coor in coords:
                                coor = coor * dpi
                                coor = math.trunc(coor)
                                if coor == coords[3] or coor == coords[2]:
                                    coor = coor - 1
                                coord2.append(coor)
                            coords = tuple(coord2)
                            draw.rectangle(coords, fill=(255, 255, 255, 0))
                        print(f'Created line hole from {station1} to {station2}')
                    # else:
                    #     print(f'No line coordinates for {station1} to {station2}')
        
        def trim(image: Image):
            print("Cropping Image")
            image_rgb = image.convert("RGB")
            background = Image.new(image_rgb.mode, image_rgb.size, image_rgb.getpixel((0,0)))
            difference = ImageChops.difference(image_rgb, background)
            bbox = difference.getbbox()
            if bbox:
                print('Image Cropped')
                image_cropped = image.crop(bbox)
                image_padding = Image.new(image_cropped.mode, (round(image_cropped.size[0] * padding), round(image_cropped.size[1] * padding)), (255,255,255))
                image_padding.paste(image_cropped, (round(image_cropped.size[0] * (padding - 1) / 2), round(image_cropped.size[1] * (padding - 1) / 2)))
                return image_padding
            else:
                print('Crop Failure')
                return image
        
        # Composite and save
        modified_map = Image.alpha_composite(modified_map.convert('RGBA'), overlay)
        modified_map = trim(modified_map)
        modified_map = compress(modified_map)
        print('Saving')
        modified_map.save(output_path)
        print('Done')
        return modified_map
        
        

        


class CoordinateFinder:
    def __init__(self, image_path):
        self.root = tk.Tk()
        self.original_image = Image.open(image_path)
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate scaling factor - increased zoom by using 1.5 instead of 0.8
        width_ratio = screen_width / self.original_image.width
        height_ratio = screen_height / self.original_image.height
        self.scale = min(width_ratio * 1.5, height_ratio * 1.5)  # 150% zoom
        
        # Resize image
        new_width = int(self.original_image.width * self.scale)
        new_height = int(self.original_image.height * self.scale)
        self.image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        
        # Create frame with scrollbars
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollbars
        self.h_scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.v_scrollbar = tk.Scrollbar(self.frame)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(self.frame, 
                              width=min(new_width, screen_width * 0.9),
                              height=min(new_height, screen_height * 0.9),
                              xscrollcommand=self.h_scrollbar.set,
                              yscrollcommand=self.v_scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbars
        self.h_scrollbar.config(command=self.canvas.xview)
        self.v_scrollbar.config(command=self.canvas.yview)
        
        # Create image on canvas
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        # Add mouse wheel scrolling
        self.canvas.bind("<MouseWheel>", self.on_mousewheel_y)  # Windows
        self.canvas.bind("<Shift-MouseWheel>", self.on_mousewheel_x)  # Windows with Shift
        self.canvas.bind("<Button-4>", self.on_mousewheel_y)  # Linux
        self.canvas.bind("<Button-5>", self.on_mousewheel_y)  # Linux
        self.canvas.bind("<Shift-Button-4>", self.on_mousewheel_x)  # Linux with Shift
        self.canvas.bind("<Shift-Button-5>", self.on_mousewheel_x)  # Linux with Shift
        
    def on_mousewheel_y(self, event):
        # Handle vertical scrolling
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        else:
            self.canvas.yview_scroll(1, "units")
            
    def on_mousewheel_x(self, event):
        # Handle horizontal scrolling
        if event.num == 4 or event.delta > 0:
            self.canvas.xview_scroll(-1, "units")
        else:
            self.canvas.xview_scroll(1, "units")
        
    def on_click(self, event):
        # Get canvas coordinates accounting for scroll position
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        self.start_x = canvas_x
        self.start_y = canvas_y
        
    def on_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        # Get canvas coordinates accounting for scroll position
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, canvas_x, canvas_y, outline="red"
        )
        
    def on_release(self, event):
        # Get canvas coordinates accounting for scroll position
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Convert coordinates back to original scale
        x1 = int(min(self.start_x, canvas_x) / self.scale)
        y1 = int(min(self.start_y, canvas_y) / self.scale)
        x2 = int(max(self.start_x, canvas_x) / self.scale)
        y2 = int(max(self.start_y, canvas_y) / self.scale)
        
        # Adjust coordinates
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
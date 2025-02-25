from PIL import Image, ImageDraw, ImageChops
import tkinter as tk
from PIL import ImageTk
from matplotlib.pylab import f
import math
from utils.trainlogger.map.station_coordinates import x_offset, y_offset, station_coordinates
from utils.trainlogger.map.line_coordinates import x_offset, y_offset, line_coordinates

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
            if line in line_coordinates:
                for station_pair, coords in line_coordinates[line].items():
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


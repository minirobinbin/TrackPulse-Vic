from PIL import Image, ImageDraw
import tkinter as tk
from PIL import ImageTk

x_offset = 800
y_offset = 1500

class MapImageHandler:
    def __init__(self, map_image_path, station_order_dictionary):
        self.station_coordinates = {
            "Parliament": (3630 + x_offset, 1303 + y_offset, 4398 + x_offset, 1457 + y_offset),
            "Jolimont": (4537 + x_offset, 1714 + y_offset, 5142 + x_offset, 1930 + y_offset),
            "Richmond": (4225 + x_offset, 2789 + y_offset, 4921 + x_offset, 2924 + y_offset),
            "Flinders Street": (2439 + x_offset, 2784 + y_offset, 3519 + x_offset, 2943 + y_offset),
            "Southern Cross": (67 + x_offset, 1291 + y_offset, 1161 + x_offset, 1454 + y_offset),
            "Melbourne Central": (2611 + x_offset, 312 + y_offset, 3365 + x_offset, 662 + y_offset),
            "Flagstaff": (2328 + x_offset, 14 + y_offset, 2535 + x_offset, 672 + y_offset),
            "North Melbourne": (14 + x_offset, 379 + y_offset, 1171 + x_offset, 576 + y_offset),
        }
        
        self.line_coordinates = {
            "burnley_group": {
                ("Flagstaff", "Parliament"): (2500 + x_offset, 800 + y_offset, 2899 + x_offset, 850 + y_offset),
            }
        }
        self.station_order = station_order_dictionary
        self.map_image = Image.open(map_image_path)
        
    def highlight_stations(self, affected_stations):
        """
        Highlights stations on the map by covering their areas with white rectangles
        
        Args:
            affected_stations (list): List of station names to highlight
        
        Returns:
            PIL.Image: Modified map image with highlighted stations
        """
        # Create a copy of the original image
        modified_map = self.map_image.copy()
        draw = ImageDraw.Draw(modified_map)
        
        # Draw white rectangles for each affected station
        for station in affected_stations:
            if station in self.station_coordinates:
                coords = self.station_coordinates[station]
                draw.rectangle(coords, fill='white')
        
        return modified_map
    
    def highlight_lines(self, station1, station2, line):
        # Create a copy of the original image
        modified_map = self.map_image.copy()
        draw = ImageDraw.Draw(modified_map)
        
        # Check if line exists in line_coordinates
        if line in self.line_coordinates:
            # Check if station pair exists in the line
            station_pair = (station1, station2)
            if station_pair in self.line_coordinates[line]:
                coords = self.line_coordinates[line][station_pair]
                draw.rectangle(coords, fill='white')
            # Check reverse pair
            station_pair = (station2, station1)
            if station_pair in self.line_coordinates[line]:
                coords = self.line_coordinates[line][station_pair]
                draw.rectangle(coords, fill='white')
                
        return modified_map
    
    def save_modified_map(self, affected_stations, output_path):
        """
        Saves the modified map with highlighted stations
        
        Args:
            affected_stations (list): List of station names to highlight
            output_path (str): Path where the modified image will be saved
        """
        modified_map = self.highlight_stations(affected_stations)
        # Highlight lines between consecutive stations
        for i in range(len(affected_stations) - 1):
            station1 = affected_stations[i]
            station2 = affected_stations[i + 1]
            for line in self.line_coordinates:
                modified_map = self.highlight_lines(station1, station2, line)
        modified_map.save(output_path)
        


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
        original_x1 = int(self.start_x / self.scale)
        original_y1 = int(self.start_y / self.scale)
        original_x2 = int(event.x / self.scale)
        original_y2 = int(event.y / self.scale)
        print(f"Coordinates: ({original_x1 - x_offset}, {original_y1 - y_offset}, {original_x2 - x_offset}, {original_y2 - y_offset})")
        
    def run(self):
        self.root.mainloop()

# Run coord finder
# if __name__ == "__main__":
#finder = CoordinateFinder("utils/trainlogger/map/base.png")
#finder.run()
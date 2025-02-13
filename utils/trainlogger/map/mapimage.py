from PIL import Image, ImageDraw
import tkinter as tk
from PIL import ImageTk

class MapImageHandler:
    def __init__(self, map_image_path):
        self.station_coordinates = {
            # Add station coordinates (x1, y1, x2, y2) for rectangular areas
            # Example format:
            "Parliament": (3630, 1303, 4398, 1457),
            # Add more stations and their coordinates
        }
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
    
    def save_modified_map(self, affected_stations, output_path):
        """
        Saves the modified map with highlighted stations
        
        Args:
            affected_stations (list): List of station names to highlight
            output_path (str): Path where the modified image will be saved
        """
        modified_map = self.highlight_stations(affected_stations)
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
        print(f"Coordinates: ({original_x1}, {original_y1}, {original_x2}, {original_y2})")
        
    def run(self):
        self.root.mainloop()

# Usage
# finder = CoordinateFinder("utils/trainlogger/map/base.png")
# finder.run()
        
# Example usage
map_handler = MapImageHandler("utils/trainlogger/map/base.png")
affected_stations = ['Parliament']
map_handler.save_modified_map(affected_stations, "temp/themap.png")
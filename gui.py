import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import csv

# Function to load CSV file
def load_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    # Clear existing data in the treeview
    for i in tree.get_children():
        tree.delete(i)

    # Read the CSV file
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            tree.insert("", "end", values=row)

# Function to sort columns
def sort_column(col, reverse):
    data_list = [(tree.set(item, col), item) for item in tree.get_children('')]
    
    # Sort data based on the column value
    data_list.sort(reverse=reverse)

    # Reorder the treeview items
    for index, (val, item) in enumerate(data_list):
        tree.move(item, '', index)

    # Reverse the sorting order for the next click
    tree.heading(col, command=lambda: sort_column(col, not reverse))

# Set up main window
root = tk.Tk()
root.title("CSV Viewer")
root.geometry("800x600")  # Set default window size

# Create a frame for Treeview
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create Treeview widget
columns = ("ID", "Set", "Type", "Date", "Line", "Start", "End")
tree = ttk.Treeview(frame, columns=columns, show="headings")

# Configure headings with sorting functionality
for col in columns:
    tree.heading(col, text=col, command=lambda _col=col: sort_column(_col, False))
    tree.column(col, width=100, anchor=tk.CENTER, stretch=True)

# Add a vertical scrollbar
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Pack the Treeview widget
tree.pack(fill=tk.BOTH, expand=True)

# Create a button to load the CSV
load_button = tk.Button(root, text="Upload CSV", command=load_csv)
load_button.pack(pady=10)

# Configure resizing behavior for root and frame
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Start the Tkinter event loop
root.mainloop()

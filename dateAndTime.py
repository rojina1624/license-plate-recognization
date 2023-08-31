import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("1100x550")
root.title("License Plate Detection")

# Set up style for buttons
style = ttk.Style()
style.configure('TButton', font=('calibri', 18), foreground="white", background="steel blue", borderwidth='4', relief='raised')
style.map('TButton', foreground=[('pressed', 'white'), ('active', 'black')], background=[('pressed', '!disabled', 'blue'), ('active', 'gray')])

# Function to make a widget invisible
def make_invisible(widget):
    widget.grid_forget()

# Function to show the license plate output
def show_plate(plate):
    output_label = tk.Label(root, text="Number on Plate : "+plate, font=("Arial", 22, "bold"), fg="white", bg="steel blue")
    output_label.grid(row=20, column=15, pady=10, sticky='s')
    root.after(5000, output_label.destroy)

# Function to run license plate detection on an image
def run_license_plate_detection(image_path):
    # Replace this with your license plate detection code
    # Here, we are just showing a random license plate number
    plate_number = "ABC 123"
    show_plate(plate_number)

# Function to run license plate detection on a live video feed
def run_live_license_plate_detection():
    # Replace this with your code to capture video from a camera and detect license plates
    # Here, we are just showing a random license plate number every 5 seconds
    while True:
        plate_number = "ABC 123"
        show_plate(plate_number)
        root.update()
        root.after(5000)

# Create the GUI buttons
dataset_button = ttk.Button(root, text="Click Here for Dataset", width=50, command=lambda: [run_license_plate_detection("image.png"), make_invisible(dataset_button), make_invisible(live_button)])
dataset_button.grid(row=0, column=4, padx=200, pady=100, sticky='s')

live_button = ttk.Button(root, text="Click Here for Real-time", width=50, command=run_live_license_plate_detection)
live_button.grid(row=1, column=4, pady=5, sticky='n')

# Create a label to show the license plate image
image_label = tk.Label(root, bg="gray50")
image_label.grid(row=0, column=0, rowspan=15, columnspan=15, padx=10, pady=10, sticky='nw')

# Load an example image
image_path = "54 copy.jpeg"
image = Image.open(image_path)
image = image.resize((500, 350), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)

# Set the image on the label
image_label.config(image=photo)
image_label.image = photo

root.mainloop()
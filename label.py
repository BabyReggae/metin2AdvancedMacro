import os
import json
import time
from PIL import Image
import pygetwindow as gw

# Directory containing the images
dirname = 'img/letterLabel'  # Replace with your directory path
output_file = 'json/shopDictionary.json'

# Dictionary to store the filename and user input
image_labels = {}

# Check if the JSON file exists
if os.path.exists(output_file):
    with open(output_file, 'r') as json_file:
        image_labels = json.load(json_file)

# Find the terminal window
windows = gw.getWindowsWithTitle("Administrateur\xa0: Windows PowerShell")  # For Command Prompt

# Loop through all files in the directory
for filename in os.listdir(dirname):
    if filename.endswith(".png"):
        # Check if the image has already been labeled
        if filename[:-4] not in image_labels:  # Remove the ".png" extension to match the keys in image_labels
            # Open and display the image
            img_path = os.path.join(dirname, filename)
            img = Image.open(img_path)
            img.show()

            if windows:
                window = windows[0]
                window.minimize()
                window.restore()

            # Prompt the user for the label
            label = input(f"Enter the label for {filename}: ")

            # Close the image
            img.close()

            # Add the filename (without extension) and label to the dictionary
            file_key = filename[:-4]  # Remove the ".png" extension
            image_labels[file_key] = label

# Write the dictionary to a JSON file
with open(output_file, 'w') as json_file:
    json.dump(image_labels, json_file, indent=4)

print(f"Labels saved to {output_file}")
    
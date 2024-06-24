import os

def open_folder(folder_path):
    try:
        os.startfile(folder_path)
        print(f"Opened the folder: {folder_path}")
    except Exception as e:
        print(f"Error opening the folder: {e}")

# Replace 'C:\\Path\\To\\Your\\Folder' with the actual path to the folder you want to open
folder_path = r"C:/Users/shyam/Desktop/Projects/agro robot"
open_folder(folder_path)

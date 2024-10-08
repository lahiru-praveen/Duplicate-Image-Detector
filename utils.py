import os
import csv
from tkinter import messagebox

def delete_image(file_path):
    try:
        os.remove(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Could not delete image: {str(e)}")

def rename_image(old_name, new_name):
    try:
        os.rename(old_name, new_name)
    except Exception as e:
        messagebox.showerror("Error", f"Could not rename image: {str(e)}")

def export_duplicates_to_csv(duplicates, save_path, folder_path):
    try:
        with open(save_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Duplicate", "Original", "Size (KB)"])
            for duplicate in duplicates:
                file1 = os.path.join(folder_path, duplicate[0])
                file2 = os.path.join(folder_path, duplicate[1])
                size1 = os.path.getsize(file1) / 1024  # Convert bytes to KB
                size2 = os.path.getsize(file2) / 1024  # Convert bytes to KB
                writer.writerow([duplicate[0], duplicate[1], round(size1, 2), round(size2, 2)])
    except Exception as e:
        messagebox.showerror("Error", f"Could not export to CSV: {str(e)}")

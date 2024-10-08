import os
import cv2
from PIL import Image
import imagehash


def get_image_hash(image_path):
    img = Image.open(image_path)
    return imagehash.phash(img)

def get_image_size(image_path):
    return os.path.getsize(image_path)

def find_duplicates(image_folder):
    hashes = {}
    duplicates = []

    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_path = os.path.join(image_folder, filename)
            img_hash = get_image_hash(image_path)

            if img_hash in hashes:
                duplicates.append((filename, hashes[img_hash]))  # (Duplicate, Original)
            else:
                hashes[img_hash] = filename

    return duplicates

def find_duplicates_with_tolerance(image_folder, tolerance=5):
    hashes = {}
    duplicates = []

    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_path = os.path.join(image_folder, filename)
            img_hash = get_image_hash(image_path)

            for stored_hash, stored_filename in hashes.items():
                if (img_hash - stored_hash) < tolerance:  # Use correct comparison for hash tolerance
                    duplicates.append((filename, stored_filename))  # (Duplicate, Original)
                    break  # Exit loop if a duplicate is found

            hashes[img_hash] = filename  # Add current hash to the list

    return duplicates

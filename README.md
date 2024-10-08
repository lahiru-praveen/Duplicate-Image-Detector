# Duplicate Image Detector

## Description
The Duplicate Image Detector is a Python-based application that helps users find and manage duplicate images in a given directory. This project allows users to identify similar images based on hash comparisons, providing a preview of duplicate files and enabling them to either rename or delete the duplicates. The application offers two distinct methods for detecting duplicates: an exact hash-based comparison and a more flexible hash-based comparison with a tolerance level. With this tool, users can efficiently manage their image libraries and eliminate redundant files.

## Technologies, Frameworks, and Libraries
- **Python**: Core programming language for building the application.
- **Tkinter**: Used for creating the graphical user interface (GUI).
- **PIL (Pillow)**: Library for image processing and previewing images in the GUI.
- **os**: For file system operations, such as reading image files from directories.
- **hashlib**: Used to generate hash values for images to detect duplicates.

## Features
- Detect duplicate images using hashing algorithms.
- Provide two methods for detecting duplicates: exact match and tolerance-based match.
- Preview duplicate images before making decisions.
- Option to rename or delete duplicate images.
- Loading indicator during the search process for better user experience.

## How to Run the Project

### Prerequisites
- Python 3.10 or higher
- Install the required libraries by running:

### Installation

To run this project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone (https://github.com/lahiru-praveen/Duplicate-Image-Detector.git)
   cd Duplicate-Image-Detector

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt

4. **Run the Streamlit app:**

   ```bash
   python app.py

5. **Select Image Folder:**
   - Use the GUI to select the folder where your images are located.

6. **Search for Duplicates:**
   - Click on the 'Search' button to find duplicate images.

7. **Preview and Manage Duplicates:**
   - The application will display a list of duplicate images, and you can preview, rename, or delete them.
  

## Duplicate Detection Methods

### 1. Exact Hash-Based Comparison (`find_duplicates`)
The Exact Hash-Based Comparison method uses image hashing to generate unique hash values for each image. The process checks if two images have identical hash values, which means the images are exactly the same. This method is fast and works well for detecting completely identical files.

```python
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
```

### 2. Hash-Based Comparison with Tolerance (`find_duplicates_with_tolerance`)
The Hash-Based Comparison with Tolerance method adds flexibility by allowing images that are not exactly identical but similar to be detected as duplicates. This method uses a tolerance value to account for slight variations between images, such as compression differences or small edits. It is more suitable for finding visually similar images, even if they aren't pixel-perfect duplicates.

```python
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
```

### Comparison of the Two Methods

- **Exact Hash-Based Comparison**:
    - Faster and more accurate for detecting images that are exactly the same.
    - Efficient for finding identical copies of images.
    - Does not detect slight variations (e.g., compression changes).

- **Hash-Based Comparison with Tolerance**:
    - Slightly slower due to additional comparisons between hashes.
    - Allows for detection of visually similar images with small differences, such as size changes or minor edits.
    - Useful for finding duplicates when images have been altered or compressed but are essentially the same.

### Future Improvements

- Add advanced image comparison techniques (e.g., perceptual hashing, deep learning-based comparison).
- Enhance the UI for a better user experience.


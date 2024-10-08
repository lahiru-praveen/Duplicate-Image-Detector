import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import os
from model import find_duplicates_with_tolerance, get_image_size, find_duplicates
from utils import delete_image, rename_image, export_duplicates_to_csv


class ImageDuplicateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Duplicate Detector")
        self.root.geometry("800x600")

        self.image_folder = ""
        self.duplicates = []

        # Loading label
        self.loading_label = tk.Label(root, text="Searching...", bg="white")
        self.loading_label.pack(pady=10)
        self.loading_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the label
        self.loading_label.config(image=None)  # Initially empty
        self.loading_label.lower()  # Hide initially

        # Folder selection
        folder_frame = tk.Frame(root)
        folder_frame.pack(pady=10)
        tk.Label(folder_frame, text="Folder:").pack(side=tk.LEFT)
        self.folder_label = tk.Label(folder_frame, text="No folder selected", width=50)
        self.folder_label.pack(side=tk.LEFT)
        tk.Button(folder_frame, text="Browse", command=self.browse_folder).pack(side=tk.LEFT)

        # Method selection
        method_frame = tk.Frame(root)
        method_frame.pack(pady=10)
        tk.Label(method_frame, text="Method:").pack(side=tk.LEFT)
        self.method_combobox = ttk.Combobox(method_frame, values=["Hash Comparison", "Hash Comparison with tolerance"])
        self.method_combobox.pack(side=tk.LEFT)

        # Search button
        tk.Button(root, text="Start Search", command=self.start_search).pack(pady=10)

        # Treeview to display duplicates
        self.tree = ttk.Treeview(root, columns=("Filename 1", "Size 1 (KB)", "Filename 2", "Size 2 (KB)"),
                                 show='headings')
        self.tree.heading("Filename 1", text="Image 1 Name")
        self.tree.heading("Size 1 (KB)", text="Image 1 Size (KB)")
        self.tree.heading("Filename 2", text="Image 2 Name")
        self.tree.heading("Size 2 (KB)", text="Image 2 Size (KB)")
        self.tree.column("Filename 1", width=200)
        self.tree.column("Filename 2", width=200)
        self.tree.column("Size 1 (KB)", width=100)
        self.tree.column("Size 2 (KB)", width=100)

        self.tree.pack(pady=10, fill="both", expand=True)

        # Action buttons
        action_frame = tk.Frame(root)
        action_frame.pack(pady=10)
        tk.Button(action_frame, text="Delete", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Export CSV", command=self.export_to_csv).pack(side=tk.LEFT, padx=5)

        # Image preview
        self.preview_frame = tk.Frame(root)
        self.preview_frame.pack(pady=10)
        self.image_label1 = tk.Label(self.preview_frame)
        self.image_label1.pack(side=tk.LEFT, padx=10)
        self.image_label2 = tk.Label(self.preview_frame)
        self.image_label2.pack(side=tk.LEFT, padx=10)

    def browse_folder(self):
        self.image_folder = filedialog.askdirectory()
        self.folder_label.config(text=self.image_folder)

    def show_loading(self):
        self.loading_label.lower()  # Hide the label initially
        self.loading_label.config(image=None)  # Clear previous image
        loading_img = Image.open("loading.gif")  # Load your GIF
        self.loading_icon = ImageTk.PhotoImage(loading_img)
        self.loading_label.config(image=self.loading_icon)  # Set image to label
        self.loading_label.lift()  # Show the label

    def hide_loading(self):
        self.loading_label.lower()  # Hide the loading label

    def start_search(self):
        method = self.method_combobox.get()
        if not self.image_folder:
            messagebox.showerror("Error", "Please select a folder!")
            return
        if not method:
            messagebox.showerror("Error", "Please select a method!")
            return

        self.show_loading()  # Show loading icon
        self.root.update()  # Update the UI to show the loading label immediately

        # Perform the search in a separate thread
        if method == "Hash Comparison":
            self.duplicates = find_duplicates(self.image_folder)
        else:
            self.duplicates = find_duplicates_with_tolerance(self.image_folder)

        self.display_duplicates()
        self.hide_loading()  # Hide loading icon after the search is complete

    def display_duplicates(self):
        # Clear any previous entries in the tree
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Display found duplicates
        for duplicate in self.duplicates:
            file1 = os.path.join(self.image_folder, duplicate[0])
            file2 = os.path.join(self.image_folder, duplicate[1])
            if os.path.exists(file1) and os.path.exists(file2):
                size1, size2 = (get_image_size(file1) / 1024), (get_image_size(file2) / 1024)  # Convert to KB
                file1, file2 = os.path.basename(file1), os.path.basename(file2)
                # Insert into the tree with file sizes in KB
                self.tree.insert("", tk.END, values=(file1, round(size1, 2), file2, round(size2, 2)))

        # Bind double-click event to preview the images
        self.tree.bind("<Double-1>", self.show_preview_popup)

    def preview_image(self, file_path, label):
        try:
            img = Image.open(file_path)
            img.thumbnail((150, 150))  # Resize for preview
            img_tk = ImageTk.PhotoImage(img)
            label.config(image=img_tk)
            label.image = img_tk  # Store reference to avoid garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image: {str(e)}")

    def show_preview_popup(self, event):
        selected = self.tree.selection()
        if selected:
            # Get the selected item
            values = self.tree.item(selected[0], "values")
            file1 = os.path.join(self.image_folder, values[0])
            file2 = os.path.join(self.image_folder, values[2])

            # Create a new popup window
            popup = tk.Toplevel(self.root)
            popup.title("Image Preview")
            popup.geometry("450x250")

            # Display previews of the images
            image_frame = tk.Frame(popup)
            image_frame.pack(pady=10)

            # Label to hold the first image
            img_label1 = tk.Label(image_frame)
            img_label1.pack(side=tk.LEFT, padx=10)
            self.preview_image(file1, img_label1)  # Preview the first image

            # Label to hold the second image
            img_label2 = tk.Label(image_frame)
            img_label2.pack(side=tk.LEFT, padx=10)
            self.preview_image(file2, img_label2)  # Preview the second image

            # Add buttons to delete or rename images
            action_frame = tk.Frame(popup)
            action_frame.pack(pady=10)

            tk.Button(action_frame, text="Delete Image 1",
                      command=lambda: self.delete_image_and_refresh(file1, popup)).pack(side=tk.LEFT, padx=5)
            tk.Button(action_frame, text="Rename Image 1",
                      command=lambda: self.rename_image_and_refresh(file1, popup)).pack(side=tk.LEFT, padx=5)
            tk.Button(action_frame, text="Delete Image 2",
                      command=lambda: self.delete_image_and_refresh(file2, popup)).pack(side=tk.LEFT, padx=5)
            tk.Button(action_frame, text="Rename Image 2",
                      command=lambda: self.rename_image_and_refresh(file2, popup)).pack(side=tk.LEFT, padx=5)

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to delete.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected images?")
        if confirm:
            for item in selected:
                file_path1 = os.path.join(self.image_folder, self.tree.item(item, "values")[0])
                file_path2 = os.path.join(self.image_folder, self.tree.item(item, "values")[2])
                try:
                    delete_image(file_path1)
                    delete_image(file_path2)
                    self.tree.delete(item)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete: {str(e)}")

    def export_to_csv(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if save_path:
            export_duplicates_to_csv(self.duplicates, save_path, self.image_folder)  # Pass image_folder
            messagebox.showinfo("Success", "CSV exported successfully!")

    def delete_image_and_refresh(self, file_path, popup):
        delete_image(file_path)
        messagebox.showinfo("Info", f"Deleted: {file_path}")
        popup.destroy()
        self.start_search()  # Refresh duplicate list after action

    def rename_image_and_refresh(self, file_path, popup):
        new_name = filedialog.asksaveasfilename(initialfile=os.path.basename(file_path), defaultextension=os.path.splitext(file_path)[1])
        if new_name:
            if not os.path.exists(new_name):  # Ensure new name doesn't exist
                rename_image(file_path, new_name)
                messagebox.showinfo("Info", f"Renamed {file_path} to {new_name}")
                popup.destroy()
                self.start_search()  # Refresh duplicate list after action
            else:
                messagebox.showerror("Error", "A file with that name already exists.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDuplicateApp(root)
    root.mainloop()

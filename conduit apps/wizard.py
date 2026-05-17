import os
import tkinter as tk
from tkinter import messagebox

def process_assets():
    # Defines the folder name - change this if you want a different name
    folder_name = "Claude_Optimised_Project"
    
    # This gets the path to your 'Documents' folder to avoid 'Access Denied' errors
    # which often happen when running scripts directly on the C: drive.
    base_path = os.path.join(os.path.expanduser("~"), "Documents")
    output_folder = os.path.join(base_path, folder_name)

    try:
        # Create the directory
        os.makedirs(output_folder, exist_ok=True)
        
        # --- YOUR ASSET PROCESSING LOGIC GOES HERE ---
        # (Example: opening files, stripping tokens, etc.)
        
        messagebox.showinfo("Success", f"Assets assembled in:\n{output_folder}")

    except PermissionError:
        messagebox.showerror("Permission Error", 
            f"Windows blocked access to create the folder.\n\n"
            f"Try closing any folders named '{folder_name}' or run the script as Administrator.")
    
    except Exception as e:
        # FIXED: Changed 'onerror' to 'showerror'
        messagebox.showerror("Error", f"Failed to complete assembly: {str(e)}")

# --- SIMPLE GUI WRAPPER ---
def run_wizard():
    root = tk.Tk()
    root.title("Claude Token Wizard")
    root.geometry("300x150")

    label = tk.Label(root, text="Claude Token Optimizer", pady=10)
    label.pack()

    btn = tk.Button(root, text="Process Assets", command=process_assets, bg="#2ecc71", fg="white", padx=20)
    btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_wizard()
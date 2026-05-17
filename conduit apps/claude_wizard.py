import os
import tkinter as tk
from tkinter import messagebox, filedialog

def process_assets():
    # 1. Ask where the files are (to keep it flexible)
    input_dir = filedialog.askdirectory(title="Select your Project Folder (GitHub Repo or Web Files)")
    if not input_dir:
        return

    # 2. Setup the output location in Documents so Windows doesn't block you
    folder_name = "Claude_Optimised_Project"
    base_path = os.path.join(os.path.expanduser("~"), "Documents")
    output_folder = os.path.join(base_path, folder_name)
    output_file = os.path.join(output_folder, "CLAUDE_CONTEXT.txt")

    try:
        # Create the folder if it's not there
        os.makedirs(output_folder, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"--- PROJECT SUMMARY: {os.path.basename(input_dir)} ---\n")
            
            # 3. Walk through your files
            for root, dirs, files in os.walk(input_dir):
                # Skip the hidden .git folder and node_modules to save tokens
                if '.git' in dirs: dirs.remove('.git')
                if 'node_modules' in dirs: dirs.remove('node_modules')

                for file in files:
                    if file.endswith(('.py', '.js', '.html', '.css', '.md', '.txt')):
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, input_dir)
                        
                        f.write(f"\n\n--- FILE: {relative_path} ---\n")
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as content:
                            f.write(content.read())

        messagebox.showinfo("Done!", f"Optimized file created at:\n{output_file}")

    except PermissionError:
        messagebox.showerror("Permission Error", "Windows blocked the script. Try saving to a different folder.")
    except Exception as e:
        # FIXED: showerror instead of onerror
        messagebox.showerror("Error", f"Something went wrong: {str(e)}")

# --- THE UI ---
root = tk.Tk()
root.title("Charity Project: Token Minimizer")
root.geometry("400x200")

tk.Label(root, text="Select a Repo or Website folder to condense it for Claude", wraplength=350, pady=20).pack()
tk.Button(root, text="Select Folder & Build Context", command=process_assets, bg="#4a90e2", fg="white", pady=10).pack()

root.mainloop()
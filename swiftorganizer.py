import os
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Set the appearance and color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

EXTENSIONS_MAP = {
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".webp": "Images",
    ".pdf": "Documents", ".docx": "Documents", ".txt": "Documents",
    ".mp4": "Videos", ".mp3": "Audio", ".zip": "Archives",
    ".py": "Code", ".exe": "Programs"
}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Modern File Sorter")
        self.geometry("500x350")

        # --- UI ELEMENTS ---
        self.label = ctk.CTkLabel(self, text="File Organizer Pro", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=(20, 10))

        self.sub_label = ctk.CTkLabel(self, text="Select a folder to automatically sort files into categories.", text_color="gray")
        self.sub_label.pack(pady=(0, 20))

        self.btn = ctk.CTkButton(self, text="Select & Organize", command=self.start_sorting, height=45, font=ctk.CTkFont(size=15))
        self.btn.pack(pady=10)

        # Progress Bar (starts at 0)
        self.progress = ctk.CTkProgressBar(self, width=300)
        self.progress.set(0)
        self.progress.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="Status: Ready", text_color="cyan")
        self.status_label.pack(pady=10)

        # Theme Switch
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self, values=["Dark", "Light", "System"], command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.pack(side="bottom", pady=20)

    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def start_sorting(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        if not files:
            messagebox.showinfo("Empty", "No files found in this folder.")
            return

        count = 0
        total_files = len(files)

        for i, filename in enumerate(files):
            filepath = os.path.join(folder, filename)
            ext = os.path.splitext(filename)[1].lower()

            # Logic
            dest_name = EXTENSIONS_MAP.get(ext, "Misc_Other")
            dest_folder = os.path.join(folder, dest_name)
            os.makedirs(dest_folder, exist_ok=True)

            # UI Updates
            self.status_label.configure(text=f"Moving: {filename[:25]}...")
            self.progress.set((i + 1) / total_files)
            self.update_idletasks()

            shutil.move(filepath, os.path.join(dest_folder, filename))
            count += 1

        self.status_label.configure(text="Status: Done!", text_color="green")
        messagebox.showinfo("Success", f"Sorted {count} files successfully!")
        self.progress.set(0)

if __name__ == "__main__":
    app = App()
    app.mainloop()
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import struct
from CEKey.parser import YMKs
from CEKey.core.ce_key import CEKey
from menu_builder import MenuBuilder
from event_handler import EventHandler
from Logger import Logger
from tree_view_manager import TreeViewManager
from file_processor import FileProcessor
from extractor import Extractor

class YANIMTool:
    def __init__(self, root):
        self.root = root
        self.logger = Logger()
        self.root.title("YANIM Tool")
        self.root.geometry("1000x700")

        # Initialize TreeView Manager
        columns = ["Frame Count", "Offset"]
        self.tree_manager = TreeViewManager(self.root, columns, self.logger)
        scrollbar = self.tree_manager.attach_scrollbar(self.root)
        self.tree_manager.get_treeview().pack(fill="both", expand=True, padx=10, pady=10)

        # Initialize File Processor and Extractor
        self.file_processor = FileProcessor(self.logger, CEKey)
        self.extractor = Extractor(self.logger)

        # Build Menu
        self.build_menu()

    def build_menu(self):
        callbacks = {
            'load_file': self.load_file,
            'mass_extract': self.mass_extract
        }
        menubar = MenuBuilder(self.root, callbacks).build_menu()
        self.root.config(menu=menubar)

    def load_file(self):
        file_path = tk.filedialog.askopenfilename(filetypes=[("DAT Files", "*.dat")])
        if not file_path:
            self.logger.log_info("No file selected.")
            return

        try:
            toc_entries, anim_data_start = self.file_processor.load_file(file_path)
            self.tree_manager.clear()
            self.tree_manager.populate(toc_entries)
            self.toc_entries = toc_entries  # Save TOC for extraction
            self.anim_data_start = anim_data_start
            self.file_path = file_path  # Save file path for extraction
            tk.messagebox.showinfo("Success", "File loaded successfully!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to load file: {e}")

    def mass_extract(self):
        if not hasattr(self, "file_path") or not self.file_path:
            self.logger.log_info("No file loaded for extraction.")
            tk.messagebox.showerror("Error", "No file loaded. Please load a file first.")
            return

        output_dir = tk.filedialog.askdirectory()
        if not output_dir:
            self.logger.log_info("Mass extraction cancelled by user.")
            return

        try:
            self.extractor.extract_files(self.file_path, output_dir, self.toc_entries, self.anim_data_start)
            tk.messagebox.showinfo("Success", f"Files extracted to: {output_dir}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to extract files: {e}")

if __name__ == "__main__":
    print("Starting YANIM Tool...")
    root = tk.Tk()
    app = YANIMTool(root)
    print("YANIM Tool initialized. Launching GUI...")
    root.mainloop()
    print("Exiting YANIM Tool.")

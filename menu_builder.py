
import tkinter as tk

class MenuBuilder:
    def __init__(self, root, callbacks):
        self.root = root
        self.callbacks = callbacks

    def build_menu(self):
        menubar = tk.Menu(self.root)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load .dat File", command=self.callbacks['load_file'])
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Tools Menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Mass Extract", command=self.callbacks['mass_extract'])
        menubar.add_cascade(label="Tools", menu=tools_menu)

        return menubar

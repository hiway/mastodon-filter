"""
MastodonFilter GUI.
"""
# pylint: disable=attribute-defined-outside-init
import tkinter as tk
import customtkinter as ctk

from mastodon_filter.gui.filter_list import FilterList
from mastodon_filter.gui.filter_editor import FilterEditor


class MastodonFilterGUI(ctk.CTk):
    """MastodonFilter GUI."""

    def __init__(self):
        """Initialize Frame."""
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize App UI."""
        self.geometry("800x600")
        self.title("MastodonFilter")
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=50)
        self.grid_rowconfigure(0, weight=1)
        self.init_menu_bar()
        self.init_filter_editor()
        self.init_filter_list()

    def init_menu_bar(self):
        """Initialize the menu bar."""
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Instance menu
        self.instance_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.instance_menu.add_command(label="Configure")
        self.menu_bar.add_cascade(label="Instance", menu=self.instance_menu)

        # Filter menu
        self.filter_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.filter_menu.add_command(label="Create")
        self.filter_menu.add_command(label="Use Template")
        self.filter_menu.add_separator()
        self.filter_menu.add_command(label="Delete")
        self.menu_bar.add_cascade(label="Filter", menu=self.filter_menu)

    def init_filter_list(self):
        """Initialize the filter list."""
        self.filter_list = FilterList(self)

    def init_filter_editor(self):
        """Initialize the filter editor."""
        self.filter_editor = FilterEditor(self)


def run_gui():
    """Run the GUI."""
    ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    app = MastodonFilterGUI()
    app.mainloop()

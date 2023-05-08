"""
MastodonFilter GUI.
"""
# pylint: disable=attribute-defined-outside-init
import tkinter as tk
from mastodon_filter.gui.filter_list import FilterList
from mastodon_filter.gui.filter_editor import FilterEditor


class MastodonFilterGUI(tk.Frame):
    """MastodonFilter GUI."""

    def __init__(self, parent):
        """Initialize Frame."""
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Initialize App UI."""
        self.parent.title("MastodonFilter")
        self.init_menu_bar()
        self.init_filter_list()
        self.init_filter_editor()
        self.pack(fill=tk.BOTH, expand=True)

    def init_menu_bar(self):
        """Initialize the menu bar."""
        self.menu_bar = tk.Menu(self.parent)
        self.parent.config(menu=self.menu_bar)

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
        self.filter_list = FilterList(self, relief=tk.SUNKEN, borderwidth=0)
        self.filter_list.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

    def init_filter_editor(self):
        """Initialize the filter editor."""
        self.filter_editor = FilterEditor(self, relief=tk.SUNKEN, borderwidth=0)
        self.filter_editor.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)


def run_gui():
    """Run the GUI."""
    root = tk.Tk()
    root.geometry("640x480+300+300")
    MastodonFilterGUI(root)
    root.mainloop()

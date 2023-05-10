import webbrowser
import tkinter as tk
import customtkinter as ctk
from mastodon_filter import __version__


class MastodonFilterGUI(ctk.CTk):
    """MastodonFilter GUI."""

    def __init__(self):
        """Initialize App."""
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize App UI."""
        self.geometry("800x600")
        self.title(f"Mastodon Filter v{__version__}")
        self.init_menu()

    def init_menu(self):
        """Initialize App Menu."""
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="About", command=self.open_about_page)
        self.help_menu.add_command(label="Issue Tracker", command=self.open_issues_page)
        self.menu.add_cascade(label="Help", menu=self.help_menu)

    def open_about_page(self):
        """Open About page."""
        webbrowser.open("https://github.com/hiway/mastodon-filter")

    def open_issues_page(self):
        """Open Issues page."""
        webbrowser.open("https://github.com/hiway/mastodon-filter/issues")

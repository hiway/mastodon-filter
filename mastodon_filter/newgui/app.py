import tkinter as tk
import customtkinter as ctk


class MastodonFilterGUI(ctk.CTk):
    """MastodonFilter GUI."""

    def __init__(self):
        """Initialize Frame."""
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize App UI."""
        self.geometry("800x600")
        self.title("Mastodon Filter")

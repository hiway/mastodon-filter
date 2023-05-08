"""
MastodonFilter GUI.
"""
import tkinter as tk


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


def run_gui():
    """Run the GUI."""
    root = tk.Tk()
    root.geometry("640x480+300+300")
    MastodonFilterGUI(root)
    root.mainloop()

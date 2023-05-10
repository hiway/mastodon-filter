"""
Keywords Frame
"""
import platform
import tkinter as tk
import customtkinter as ctk


class KeywordsFrame(ctk.CTkFrame):
    """
    Keywords Frame.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.current_filter = tk.StringVar()
        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        """
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.label = ctk.CTkLabel(self, text="Keywords")
        self.label.grid(row=0, column=0, sticky="nsew")
        self.editor = ctk.CTkTextbox(
            self,
            undo=True,
            autoseparators=True,
            maxundo=-1,
        )
        if platform.system() == "Darwin":
            self.editor.bind("<Command-Key-s>", self._save_filter)
        else:
            self.editor.bind("<Control-Key-s>", self._save_filter)
        self.editor.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)

    def _save_filter(self, _event):
        """
        Save filter.
        """
        keywords = self.editor.get("1.0", tk.END).split("\n")
        self.parent.save_filter(self.current_filter.get(), keywords)

    def load_filter(self, title, keywords):
        """
        Update filter.
        """
        self.current_filter.set(title)
        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", "\n".join(keywords))
        self.editor.edit_reset()

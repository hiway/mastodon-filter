"""
Mastodon FilterEditor.
"""
# pylint: disable=attribute-defined-outside-init
import json
import tkinter as tk
import customtkinter as ctk


class FilterEditor(ctk.CTkFrame):
    """Mastodon FilterList."""

    def __init__(self, parent, **kwargs):
        """Initialize Frame."""
        ctk.CTkFrame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Initialize UI."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=50)
        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text="Keywords")
        self.label.grid(row=0, column=0, sticky="nsew")
        self.init_editor()
        self.grid(row=0, column=1, columnspan=3, sticky="nsew")

    def init_editor(self):
        """Initialize editor."""
        self.editor = ctk.CTkTextbox(
            self,
            undo=True,
            autoseparators=True,
            maxundo=-1,
        )
        self.editor.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    def load_filter(self, cached_filters_path, title):
        """Load filter."""
        with open(cached_filters_path, "r", encoding="utf-8") as file:
            filters = json.load(file)
        for filter in filters:  # pylint: disable=redefined-builtin
            if filter["title"] == title:
                current_filter = filter
                break
        else:
            return
        keywords_list = [kw["keyword"] for kw in current_filter.get("keywords", [])]
        keywords = "\n".join(keywords_list)
        self.editor.delete("1.0", tk.END)
        self.editor.insert(tk.END, keywords)
        self.editor.edit_reset()

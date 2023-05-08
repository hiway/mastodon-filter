"""
Mastodon FilterEditor.
"""
# pylint: disable=attribute-defined-outside-init
import json
import threading
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from mastodon_filter.api import MastodonFilters
from mastodon_filter.config import get_config
from mastodon_filter.errors import extract_error_message


class FilterEditor(ctk.CTkFrame):
    """Mastodon FilterList."""

    def __init__(self, parent, **kwargs):
        """Initialize Frame."""
        ctk.CTkFrame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.cached_filters_path = tk.StringVar()
        self.init_ui()

    def init_ui(self):
        """Initialize UI."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=50)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.label = ctk.CTkLabel(self, text="Keywords")
        self.label.grid(row=0, column=0, columnspan=5, sticky="nsew")

        self.init_editor()
        self.init_buttons()

        self.grid(row=0, column=1, columnspan=3, sticky="nsew")

    def init_editor(self):
        """Initialize editor."""
        self.editor = ctk.CTkTextbox(
            self,
            undo=True,
            autoseparators=True,
            maxundo=-1,
        )
        self.editor.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)

    def init_buttons(self):
        """Initialize buttons."""
        self.button_save = ctk.CTkButton(
            self,
            text="Save",
            command=self.save_filter,
        )
        self.button_save.grid(row=2, column=4, sticky="nsew", padx=5, pady=5)

    def load_filter(self, cached_filters_path, title):
        """Load filter."""
        self.cached_filters_path = cached_filters_path
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

    def save_filter(self):
        """Save filter."""
        self.button_save.configure(text="Saving...", state="disabled")
        self.editor.configure(state="disabled")
        thread = threading.Thread(target=self.save_filter_thread)
        thread.daemon = True
        thread.start()

    def save_filter_thread(self):
        """Save filter in background."""
        title = self.parent.filter_list.current_filter.get()
        keywords = self.editor.get("1.0", tk.END)
        keywords_list = keywords.split("\n")
        keywords_list = [kw for kw in keywords_list if kw]

        config = get_config()

        print(f"Saving filter {title} with {len(keywords_list)} keywords.")
        try:
            if not config.api_base_url or not config.access_token:
                raise ValueError("Instance is not configured.")
            filters = MastodonFilters(config)
            filters.sync(title=title, keywords=keywords_list)
            self.parent.filter_list.load_filters()
            self.editor.configure(state="normal")
            self.load_filter(self.cached_filters_path, title)
        except Exception as err:  # pylint: disable=broad-except
            error_message = extract_error_message(err)
            messagebox.showerror("Error", error_message)
        finally:
            self.button_save.configure(text="Save", state="normal")
            print("Done.")

"""
Mastodon FilterEditor.
"""
# pylint: disable=attribute-defined-outside-init
import platform
import json
import threading
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from mastodon_filter.api import MastodonFilters
from mastodon_filter.config import get_config
from mastodon_filter.logging import get_logger
from mastodon_filter.errors import extract_error_message

logger = get_logger(__name__)


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
        self.grid_rowconfigure(2, weight=2)
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
        if platform.system() == "Darwin":
            self.editor.bind("<Command-Key-s>", lambda event: self.save_filter())
        else:
            self.editor.bind("<Control-Key-s>", lambda event: self.save_filter())
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
            logger.error("Filter %s not found.", title)
            return
        logger.debug("Loading filter %s.", title)
        keywords_list = [kw["keyword"] for kw in current_filter.get("keywords", [])]
        keywords = "\n".join(keywords_list)
        self.editor.delete("1.0", tk.END)
        self.editor.insert(tk.END, keywords)
        self.editor.edit_reset()

    def save_filter(self):
        """Save filter."""
        title = self.parent.filter_list.current_filter.get()
        keywords = self.editor.get("1.0", tk.END)
        keywords_list = keywords.split("\n")
        keywords_list = [kw for kw in keywords_list if kw]

        self.button_save.configure(text="Saving...", state="disabled")
        self.editor.configure(state="disabled")
        logger.debug("Saving filter %s in background.", title)
        thread = threading.Thread(
            target=self.save_filter_thread, args=(title, keywords_list)
        )
        thread.daemon = True
        thread.start()

    def save_filter_thread(self, title: str, keywords: list):
        """Save filter in background."""

        config = get_config()

        logger.debug("Saving filter %s with %s keywords.", title, len(keywords))
        try:
            if not config.api_base_url or not config.access_token:
                raise ValueError("Instance is not configured.")
            filters = MastodonFilters(config)
            filters.sync(title=title, keywords=keywords)
            self.parent.filter_list.load_filters()
            self.editor.configure(state="normal")
            self.load_filter(self.cached_filters_path, title)
        except Exception as err:  # pylint: disable=broad-except
            error_message = extract_error_message(err)
            messagebox.showerror("Error", error_message)
            logger.error(error_message)
        finally:
            self.button_save.configure(text="Save", state="normal")
            logger.debug("Done.")

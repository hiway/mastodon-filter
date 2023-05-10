"""
Mastodon FilterList.
"""
# pylint: disable=attribute-defined-outside-init
import json
import threading
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
from darkdetect import isDark

from mastodon_filter.api import MastodonFilters
from mastodon_filter.config import APP_DIR, get_config
from mastodon_filter.logging import get_logger
from mastodon_filter.errors import extract_error_message

logger = get_logger(__name__)


class FilterList(ctk.CTkFrame):
    """Mastodon FilterList."""

    def __init__(self, parent, **kwargs):
        """Initialize Frame."""
        ctk.CTkFrame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.cached_filters_path = APP_DIR / "filters.json"
        self.current_filter = tk.StringVar()
        self.init_ui()
        self.grid(row=0, column=0, sticky="nsew")

    def init_ui(self):
        """Initialize UI."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=20)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text="Filters")
        self.label.grid(row=0, column=0, sticky="ew")

        self.filters = tk.Listbox(
            self,
            bd=0,
            bg="#2f2f2f" if isDark() else "#dadada",
        )
        self.filters.bind("<<ListboxSelect>>", self.filter_selected)
        self.filters.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)

        self.button_delete = ctk.CTkButton(
            self,
            text="Delete",
            command=self.delete_filter,
            fg_color="#ff8888",
        )
        self.button_delete.grid(row=2, column=0, sticky="nsew", padx=15, pady=5)

        self.button_create = ctk.CTkButton(
            self,
            text="Create",
            command=self.create_filter,
        )
        self.button_create.grid(row=3, column=0, sticky="nsew", padx=15, pady=5)

        self.load_filters()

    def load_filters(self):
        """Load filters."""
        config = get_config()
        if not config.api_base_url or not config.access_token:
            return
        try:
            filters = MastodonFilters(config)
            filters.export(self.cached_filters_path)
            self.update_filters()
        except Exception as err:  # pylint: disable=broad-except
            error_message = extract_error_message(err)
            messagebox.showerror("Error", error_message)

    def update_filters(self):
        """Update filters."""
        with open(self.cached_filters_path, "r", encoding="utf-8") as file:
            filters = json.load(file)
        self.filters.delete(0, tk.END)
        filter_titles = sorted([filter["title"] for filter in filters])
        for title in filter_titles:  # pylint: disable=redefined-builtin
            self.filters.insert(tk.END, title)

    def filter_selected(self, event):
        """Handle filter selection."""
        widget = event.widget
        selection = widget.curselection()
        try:
            title = widget.get(selection[0])
            logger.debug("Filter selected: %s", title)
            self.current_filter.set(title)
            self.parent.filter_editor.load_filter(self.cached_filters_path, title)
        except IndexError:
            logger.debug("No filter selected")

    def create_filter(self):
        """Create filter."""
        title = tk.simpledialog.askstring(
            "Create filter",
            "Enter a title for the filter:",
            parent=self,
        )
        if not title:
            return
        self.current_filter.set(title)
        thread = threading.Thread(
            target=self.create_filter_thread,
            args=(title,),
        )
        thread.start()

    def create_filter_thread(self, title):
        """Create filter thread."""
        config = get_config()
        if not config.api_base_url or not config.access_token:
            return
        print(f"Creating filter: {title}")
        try:
            filters = MastodonFilters(config)
            filters.create(
                title=title,
                context=["home", "public", "thread"],
                action="warn",
                keywords=["example-keyword"],
            )
            self.load_filters()
            self.filters.select_clear(0, tk.END)
            # get index of title
            index = self.filters.get(0, tk.END).index(title)
            self.filters.select_set(index)
            self.parent.filter_editor.load_filter(self.cached_filters_path, title)
            print(f"Created filter: {title}")
        except Exception as err:  # pylint: disable=broad-except
            error_message = extract_error_message(err)
            messagebox.showerror("Error", error_message)

    def delete_filter(self):
        """Delete filter."""
        if not self.current_filter.get():
            return
        if not messagebox.askyesno(
            "Delete filter",
            f"Are you sure you want to delete the filter: {self.current_filter.get()}?",
            parent=self,
        ):
            return
        title = self.current_filter.get()
        if not title:
            return
        self.button_delete.configure(state="disabled")
        self.filters.configure(state="disabled")
        logger.info("Starting background task to delete filter: %s ", title)
        thread = threading.Thread(
            target=self.delete_filter_thread,
            args=(title,),
        )
        thread.start()

    def delete_filter_thread(self, title):
        """Delete filter thread."""
        config = get_config()
        if not config.api_base_url or not config.access_token:
            return
        logger.info("Deleting filter: %s", title)
        try:
            filters = MastodonFilters(config)
            filters.delete(title)
            self.filters.configure(state="normal")
            self.load_filters()
            self.parent.filter_editor.editor.delete("1.0", tk.END)
            self.parent.filter_editor.editor.edit_reset()
            logger.info("Deleted filter: %s", title)
        except Exception as err:  # pylint: disable=broad-except
            error_message = extract_error_message(err)
            messagebox.showerror("Error", error_message)
        finally:
            # enable delete button and filters listbox
            self.button_delete.configure(state="normal")

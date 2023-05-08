"""
Mastodon FilterList.
"""
# pylint: disable=attribute-defined-outside-init
import json
import tkinter as tk
from tkinter import messagebox

from mastodon_filter.api import MastodonFilters
from mastodon_filter.config import APP_DIR, get_config
from mastodon_filter.errors import extract_error_message


class FilterList(tk.Frame):
    """Mastodon FilterList."""

    def __init__(self, parent, **kwargs):
        """Initialize Frame."""
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.cached_filters_path = APP_DIR / "filters.json"
        self.current_filter = tk.StringVar()
        self.init_ui()

    def init_ui(self):
        """Initialize UI."""
        self.filters = tk.Listbox(self)
        self.filters.bind("<<ListboxSelect>>", self.filter_selected)
        self.filters.pack(fill=tk.BOTH, expand=True)
        self.load_filters()
        self.pack(fill=tk.BOTH, expand=True)

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
        for filter in filters:  # pylint: disable=redefined-builtin
            self.filters.insert(tk.END, filter["title"])

    def filter_selected(self, event):
        """Handle filter selection."""
        widget = event.widget
        selection = widget.curselection()
        try:
            title = widget.get(selection[0])
            self.current_filter.set(title)
            self.parent.filter_editor.load_filter(self.cached_filters_path, title)
        except IndexError:
            pass

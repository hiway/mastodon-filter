"""
Mastodon FilterList.
"""
import tkinter as tk


class FilterList(tk.Frame):
    """Mastodon FilterList."""

    def __init__(self, parent, **kwargs):
        """Initialize Frame."""
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Initialize App UI."""
        self.filters = tk.Listbox(self)
        self.filters.pack(fill=tk.BOTH, expand=True)
        self.load_filters()

        self.pack(fill=tk.BOTH, expand=True)

    def load_filters(self):
        """Load filters."""
        self.filters.delete(0, tk.END)
        for filter_id in range(10):
            self.filters.insert(tk.END, f"Filter {filter_id}")

"""
Mastodon FilterEditor.
"""
# pylint: disable=attribute-defined-outside-init
import json
import tkinter as tk


class FilterEditor(tk.Frame):
    """Mastodon FilterList."""

    def __init__(self, parent, **kwargs):
        """Initialize Frame."""
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Initialize UI."""
        self.init_editor()
        self.pack(fill=tk.BOTH, expand=True)

    def init_editor(self):
        """Initialize editor."""
        self.editor = tk.Text(self, undo=True, autoseparators=True, maxundo=-1)
        self.editor.pack(fill=tk.BOTH, expand=True)

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

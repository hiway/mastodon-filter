"""
Mastodon FilterEditor.
"""
# pylint: disable=attribute-defined-outside-init
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

import webbrowser
import tkinter as tk
import customtkinter as ctk
from mastodon_filter import __version__


class MastodonFilterGUI(ctk.CTk):
    """MastodonFilter GUI."""

    def __init__(self):
        """Initialize App."""
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize App UI."""
        self.geometry("800x600")
        self.title(f"Mastodon Filter v{__version__}")
        self.init_menu()

    def init_menu(self):
        """Initialize App Menu."""
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        # File menu
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Import Filter", command=self.import_filter)
        self.file_menu.add_command(label="Export Filter", command=self.export_filter)
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="Backup Filters",
            command=self.backup_filters,
        )
        self.file_menu.add_command(
            label="Restore Filters", command=self.restore_filters
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Preferences", command=self.open_preferences)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        # Help menu
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="About", command=self.open_about_page)
        self.help_menu.add_command(label="Issue Tracker", command=self.open_issues_page)
        self.menu.add_cascade(label="Help", menu=self.help_menu)

    def import_filter(self):
        """Import Filter."""
        raise NotImplementedError("Import Filter not implemented yet.")

    def export_filter(self):
        """Export Filter."""
        raise NotImplementedError("Export Filter not implemented yet.")

    def backup_filters(self):
        """Backup Filters."""
        raise NotImplementedError("Backup Filters not implemented yet.")

    def restore_filters(self):
        """Restore Filters."""
        raise NotImplementedError("Restore Filters not implemented yet.")

    def open_preferences(self):
        """Open Preferences."""
        raise NotImplementedError("Preferences not implemented yet.")

    def open_about_page(self):
        """Open About page."""
        webbrowser.open("https://github.com/hiway/mastodon-filter")

    def open_issues_page(self):
        """Open Issues page."""
        webbrowser.open("https://github.com/hiway/mastodon-filter/issues")

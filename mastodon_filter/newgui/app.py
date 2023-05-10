"""
Mastodon Filter App.
"""
# pylint: disable=attribute-defined-outside-init
import webbrowser
import tkinter as tk

import customtkinter as ctk
from darkdetect import isDark

from mastodon_filter import __version__
from mastodon_filter.newgui.filters import FiltersFrame
from mastodon_filter.newgui.keywords import KeywordsFrame
from mastodon_filter.newgui.preferences import PreferencesDialog


class MastodonFilterGUI(ctk.CTk):
    """
    Mastodon Filter App.
    """

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize App UI."""
        self.title(f"Mastodon Filter v{__version__}")

        self.geometry("800x600")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=20)

        self.init_menu()

        self.filters = FiltersFrame(self)
        self.filters.grid(row=0, column=0, sticky="nsew")
        self.filters.update_filters([f"Filter {i}" for i in range(1, 10)])

        self.keywords = KeywordsFrame(self)
        self.keywords.grid(row=0, column=1, sticky="nsew")

        self.init_theme()

    def init_theme(self):
        """
        Patch disparities between tk and ctk components.
        """
        if isDark():
            self.background_color = (
                self.keywords._bg_color  # pylint: disable=protected-access
            )
        else:
            self.background_color = (
                self.keywords._fg_color  # pylint: disable=protected-access
            )
            self.filters.filters_list.configure(bg=self.background_color[0])
        self.configure(fg_color=self.background_color)

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

        # Filter menu
        self.filter_menu = tk.Menu(self.menu, tearoff=0)
        self.filter_menu.add_command(label="Sync", command=self.sync_filter)
        self.filter_menu.add_separator()
        self.filter_menu.add_command(label="Create", command=self.create_filter)
        self.filter_menu.add_command(
            label="Create from Template", command=self.use_template
        )
        self.filter_menu.add_separator()
        self.filter_menu.add_command(label="Delete", command=self.delete_filter)
        self.menu.add_cascade(label="Filter", menu=self.filter_menu)

        # Help menu
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="About", command=self.open_about_page)
        self.help_menu.add_command(label="Issue Tracker", command=self.open_issues_page)
        self.menu.add_cascade(label="Help", menu=self.help_menu)

    # Menu Event Handlers

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
        preferences_dialog = PreferencesDialog(self)
        preferences_dialog.set_preferences("instance_url", "access_token")
        preferences_dialog.wait_window()

    def sync_filter(self):
        """Sync Filter."""
        raise NotImplementedError("Sync Filter not implemented yet.")

    def create_filter(self):
        """Create Filter."""
        raise NotImplementedError("Create Filter not implemented yet.")

    def use_template(self):
        """Use Template."""
        raise NotImplementedError("Use Template not implemented yet.")

    def delete_filter(self):
        """Delete Filter."""
        raise NotImplementedError("Delete Filter not implemented yet.")

    def open_about_page(self):
        """Open About page."""
        webbrowser.open("https://github.com/hiway/mastodon-filter")

    def open_issues_page(self):
        """Open Issues page."""
        webbrowser.open("https://github.com/hiway/mastodon-filter/issues")

    # Filter Event Handlers

    def load_filter(self, current_filter: str, previous_filter: str):
        """Load Filter."""
        print(f"Previous filter: {previous_filter}")
        print(f"Loading filter: {current_filter}")
        self.keywords.load_filter(
            current_filter, [f"{current_filter} Keyword {i}" for i in range(1, 10)]
        )
        raise NotImplementedError("Load Filter not implemented yet.")

    def save_filter(self, current_filter: str, keywords: list[str]):
        """Save Filter."""
        print(f"Saving filter: {current_filter}")
        print(f"Keywords: {keywords}")
        raise NotImplementedError("Save Filter not implemented yet.")

    def save_preferences(self, instance_url: str, access_token: str):
        """Save Preferences."""
        print(f"Instance URL: {instance_url}")
        print(f"Access Token: {access_token}")
        # raise NotImplementedError("Save Preferences not implemented yet.")

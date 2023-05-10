"""
Preferences Dialog.
"""
# pylint: disable=attribute-defined-outside-init
import tkinter as tk

import customtkinter as ctk


class PreferencesDialog(ctk.CTkToplevel):
    """
    Preferences Dialog.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Initialize UI."""
        self.title("Mastodon Filter Preferences")

        self.frame = ctk.CTkFrame(self)

        self.geometry("400x100")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.frame.instance_url_label = ctk.CTkLabel(self.frame, text="Instance URL")
        self.frame.instance_url_label.grid(row=0, column=0, sticky="nsew")
        self.frame.instance_url_entry = ctk.CTkEntry(self.frame)
        self.frame.instance_url_entry.grid(row=0, column=1, sticky="nsew")

        self.frame.access_token_label = ctk.CTkLabel(self.frame, text="Access Token")
        self.frame.access_token_label.grid(row=1, column=0, sticky="nsew")
        self.frame.access_token_entry = ctk.CTkEntry(self.frame)
        self.frame.access_token_entry.grid(row=1, column=1, sticky="nsew")

        self.frame.save_button = tk.Button(
            self.frame, text="Save", command=self._save_clicked
        )
        self.frame.save_button.grid(row=2, column=1, sticky="nsew")

        self.frame.grid(row=0, column=0, sticky="nsew")

    def set_preferences(self, instance_url, access_token):
        """Set preferences."""
        self.frame.instance_url_entry.delete(0, tk.END)
        self.frame.instance_url_entry.insert(0, instance_url)

        self.frame.access_token_entry.delete(0, tk.END)
        self.frame.access_token_entry.insert(0, access_token)

    def _save_clicked(self):
        """Save preferences."""
        instance_url = self.frame.instance_url_entry.get()
        access_token = self.frame.access_token_entry.get()
        self.parent.save_preferences(
            instance_url=instance_url, access_token=access_token
        )
        self.destroy()

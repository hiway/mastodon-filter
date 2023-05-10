"""
Contexts Frame
"""
import tkinter as tk
import customtkinter as ctk


class ContextsFrame(ctk.CTkFrame):
    """
    Contexts Frame.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        """
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text="Contexts")
        self.label.grid(row=0, column=0, sticky="ew")

        self.context_home = ctk.CTkCheckBox(self, text="Home")
        self.context_home.grid(row=1, column=0, sticky="ew")
        self.context_notifications = ctk.CTkCheckBox(self, text="Notifications")
        self.context_notifications.grid(row=2, column=0, sticky="ew")
        self.context_public = ctk.CTkCheckBox(self, text="Public")
        self.context_public.grid(row=3, column=0, sticky="ew")
        self.context_thread = ctk.CTkCheckBox(self, text="Thread")
        self.context_thread.grid(row=4, column=0, sticky="ew")
        self.context_account = ctk.CTkCheckBox(self, text="Account")
        self.context_account.grid(row=5, column=0, sticky="ew")

"""
Contexts Frame
"""
import tkinter as tk
import customtkinter as ctk

from mastodon_filter.schema import Context


class ContextsFrame(ctk.CTkFrame):
    """
    Contexts Frame.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self._context_home = tk.BooleanVar()
        self._context_notifications = tk.BooleanVar()
        self._context_public = tk.BooleanVar()
        self._context_thread = tk.BooleanVar()
        self._context_account = tk.BooleanVar()
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

        self.context_home = ctk.CTkCheckBox(
            self, text="Home", variable=self._context_home, onvalue=True, offvalue=False
        )
        self.context_home.grid(row=1, column=0, sticky="ew")
        self.context_notifications = ctk.CTkCheckBox(
            self,
            text="Notifications",
            variable=self._context_notifications,
            onvalue=True,
            offvalue=False,
        )
        self.context_notifications.grid(row=2, column=0, sticky="ew")
        self.context_public = ctk.CTkCheckBox(
            self,
            text="Public",
            variable=self._context_public,
            onvalue=True,
            offvalue=False,
        )
        self.context_public.grid(row=3, column=0, sticky="ew")
        self.context_thread = ctk.CTkCheckBox(
            self,
            text="Thread",
            variable=self._context_thread,
            onvalue=True,
            offvalue=False,
        )
        self.context_thread.grid(row=4, column=0, sticky="ew")
        self.context_account = ctk.CTkCheckBox(
            self,
            text="Account",
            variable=self._context_account,
            onvalue=True,
            offvalue=False,
        )
        self.context_account.grid(row=5, column=0, sticky="ew")

    def update_context(self, context: Context):
        """
        Update context.
        """
        self._context_home.set(context.home)
        self._context_notifications.set(context.notifications)
        self._context_public.set(context.public)
        self._context_thread.set(context.thread)
        self._context_account.set(context.account)

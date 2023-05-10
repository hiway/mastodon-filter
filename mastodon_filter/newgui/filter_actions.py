"""
Filter Actions Frame
"""
import tkinter as tk
import customtkinter as ctk


class FilterActionsFrame(ctk.CTkFrame):
    """
    Filter Actions Frame.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self._action_hide = tk.BooleanVar()
        self._action_warn = tk.BooleanVar()
        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        """
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.label = ctk.CTkLabel(self, text="Filter Actions")
        self.label.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.action_hide = ctk.CTkCheckBox(
            self,
            text="Hide",
            variable=self._action_hide,
            onvalue=True,
            offvalue=False,
        )
        self.action_hide.grid(row=1, column=0, sticky="ew")
        self.action_warn = ctk.CTkCheckBox(
            self,
            text="Warn",
            variable=self._action_warn,
            onvalue=True,
            offvalue=False,
        )
        self.action_warn.grid(row=1, column=1, sticky="ew")

    def update_filter_action(self, filter_action):
        """
        Update Filter Actions.
        """
        print(f"filter_action: {filter_action}")
        self._action_hide.set("hide" == filter_action)
        self._action_warn.set("warn" == filter_action)

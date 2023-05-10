"""
Filters Frame
"""
import tkinter as tk
import customtkinter as ctk

from mastodon_filter.newgui.contexts import ContextsFrame


class FiltersFrame(ctk.CTkFrame):
    """
    Filters Frame.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.current_filter = tk.StringVar()
        self.previous_filter = tk.StringVar()
        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        """
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text="Filters")
        self.label.grid(row=0, column=0, sticky="ew")

        self.filters_list = tk.Listbox(self, bd=0)
        self.filters_list.bind("<<ListboxSelect>>", self._select_filter)
        self.filters_list.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)

        self.contexts_frame = ContextsFrame(self)
        self.contexts_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=5)

    def _select_filter(self, event):
        """
        Select filter event handler.
        """
        self.previous_filter.set(self.current_filter.get())
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            data = widget.get(index)
            self.current_filter.set(data)
        current_filter = self.current_filter.get()
        previous_filter = self.previous_filter.get()
        if current_filter != previous_filter:
            self.parent.load_filter(current_filter, previous_filter)

    def update_filters(self, filters: list[Filter]):
        """
        Update filters.
        """
        if not filters:
            return
        self.filters_list.delete(0, tk.END)
        for title in filters:
            self.filters_list.insert(tk.END, title)

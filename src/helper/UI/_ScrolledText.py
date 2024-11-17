import tkinter as tk
from tkinter import ttk

class ScrolledText(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._text = tk.Text(self, *args, **kwargs)
        self._text.grid(row=0, column=0, sticky="nsew")

        self._scr_bar = ttk.Scrollbar(self, orient="vertical", command=self._text.yview)
        self._scr_bar.grid(row=0, column=1, sticky="ns")
        self._text.configure(yscrollcommand=self._scr_bar.set)

    def _scr_bar_set(self, upper, lower):
        """For auto-hiding the scrollbar"""
        if float(upper) <= 0.0 and float(lower) >= 1.0:
            self._scr_bar.grid_remove()
        else:
            self._scr_bar.grid()
        self._scr_bar.set(upper, lower)
            
    def __getattr__(self, name):
        if name in self._text.__dict__:
            return getattr(self._text, name)
        else:
            raise AttributeError(f"The attribute `{name}` is not defined for ScrolledText.")

    def configure(self, **kwargs):
        self._text.configure(**kwargs)
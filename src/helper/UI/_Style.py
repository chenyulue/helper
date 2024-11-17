from tkinter import ttk

class MyStyle(ttk.Style):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.theme_use("clam")

        self._item_button()

    def _item_button(self):
        self.configure("Item.TButton", foreground="red", background="blue")
from pathlib import Path
from tkinter import ttk

from PIL import Image, ImageTk

from ..assets import ICON_CMP, ICON_CHECK, ICON_SETTING, ICON_ABOUT


class SideBar(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        icons_size = 50
        self._icons = {
            "check": self._get_image(ICON_CHECK, size=(icons_size, icons_size)),
            "cmp": self._get_image(ICON_CMP, size=(icons_size, icons_size)),
            "setting": self._get_image(
                ICON_SETTING, size=(icons_size - 20, icons_size - 20)
            ),
            "about": self._get_image(
                ICON_ABOUT, size=(icons_size - 20, icons_size - 20)
            ),
        }

        self._create_ui()

    def _create_ui(self):
        self.rowconfigure(4, weight=1)

        self._button_check = ttk.Button(
            self,
            text="形式缺陷",
            image=self._icons["check"],
            compound="top",
            style="Item.TButton"
        )
        self._button_cmp = ttk.Button(
            self,
            text="文本对比",
            image=self._icons["cmp"],
            compound="top",
        )

        ttk.Frame(self).grid(row=4, column=0, sticky="ns")

        self._button_setting = ttk.Button(
            self,
            text="设置",
            image=self._icons["setting"],
            compound="top",
        )
        self._button_about = ttk.Button(
            self, text="关于", image=self._icons["about"], compound="top"
        )

        self._button_check.grid(row=0, column=0, sticky="nwe", pady=(5, 0))
        self._button_cmp.grid(row=1, column=0, sticky="nwe", pady=(5, 0))
        self._button_setting.grid(row=5, column=0, sticky="swe", pady=(5, 0))
        self._button_about.grid(row=6, column=0, sticky="swe", pady=5)

    def _get_image(self, file: Path, size: tuple[int, int]) -> ImageTk.PhotoImage:
        image = Image.open(file).resize(size)
        return ImageTk.PhotoImage(image)

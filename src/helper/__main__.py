import tkinter as tk
import nativesvttk as svttk

from helper.UI import CompareWindow, CheckWindow, SideBar
from helper.assets import ICON_APP
from helper.UI._Style import MyStyle

def main() -> None:
    root = tk.Tk()
    root.iconbitmap(str(ICON_APP))
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    SideBar(root).grid(sticky="nsew")
    svttk.use_light_theme()
    s = MyStyle()
    print(s.layout("TButton"))
    root.mainloop()

if __name__ == "__main__":
    main()
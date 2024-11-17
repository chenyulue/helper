import tkinter as tk
from tkinter import ttk

# from tkinter.scrolledtext import ScrolledText
from ._ScrolledText import ScrolledText


class CompareWindow(ttk.Panedwindow):
    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, orient="vertical", *args, **kwargs)

        self._create_ui()

    def _create_ui(self) -> None:
        frame_top = ttk.Frame(self)
        frame_top.rowconfigure(1, weight=1)
        frame_top.columnconfigure(0, weight=1)
        frame_top.columnconfigure(2, weight=1)
        
        self.label_a = ttk.Label(frame_top, text="原始文本 (请输入或Ctrl+V粘贴文本) :")
        self.label_b = ttk.Label(frame_top, text="修改文本 (请输入或Ctrl+V粘贴文本) :")
        self.label_b.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.label_a.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.text_a = ScrolledText(frame_top, height=30, width=70)
        self.text_b = ScrolledText(frame_top, height=30, width=70)
        self.text_b.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nsew")
        self.text_a.grid(row=1, column=2, padx=5, pady=(0, 5), sticky="nsew")

        frame_btns = ttk.Frame(frame_top)
        frame_btns.grid(row=1, column=1)
        self.button_cmp = ttk.Button(frame_btns, text="比较")
        self.button_clr = ttk.Button(frame_btns, text="清空")
        self.button_cmp.grid(row=0, column=0, padx=(0, 5), pady=10)
        self.button_clr.grid(row=1, column=0, padx=(0, 5), pady=10)

        self.add(frame_top, weight=2)

        frame_bottom = ttk.Frame(self)
        frame_bottom.rowconfigure(1, weight=1)
        frame_bottom.columnconfigure(0, weight=1)
        
        self.label_result = ttk.Label(frame_bottom, text="修改对照 :")
        self.label_result.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.text_result = ScrolledText(frame_bottom, height=20)
        self.text_result.grid(
            row=1, column=0, padx=5, pady=(0, 5), sticky="nsew"
        )

        self.add(frame_bottom, weight=1)


if __name__ == "__main__":
    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    CompareWindow(root).grid(sticky="nsew")
    root.mainloop()

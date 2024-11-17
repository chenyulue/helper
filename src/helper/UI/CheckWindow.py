from tkinter import ttk

from ._ScrolledText import ScrolledText

class CheckWindow(ttk.Panedwindow):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, orient="vertical", *args, **kwargs)

        self._create_ui()

    def _create_ui(self):  
        self._notebook = ttk.Notebook(self, height=400)
        
        self._text_abstract = ScrolledText(self._notebook)

        frame_desc = ttk.Frame(self._notebook)
        frame_desc.rowconfigure(1, weight=1)
        frame_desc.columnconfigure(0, weight=1)
        
        self._text_description = ScrolledText(frame_desc, width=90)
        self._text_figures = ScrolledText(frame_desc, width=20)
        ttk.Label(frame_desc, text="说明书:").grid(row=0, column=0, sticky="w", pady=5)
        self._text_description.grid(row=1, column=0, sticky="nsew")
        ttk.Label(frame_desc, text="附图图号:").grid(row=0, column=1, sticky="w", pady=5, padx=(20, 0))
        self._text_figures.grid(row=1, column=1, sticky="ns", padx=(20, 0))
        
        self._text_claim = ScrolledText(self._notebook)

        self._notebook.add(self._text_abstract, text="摘要")
        self._notebook.add(self._text_claim, text="权利要求书")
        self._notebook.add(frame_desc, text="说明书及附图")

        self.add(self._notebook, weight=2)
        self._notebook.enable_traversal()

        self._notebook_result = ttk.Notebook(self, height=300)
        
        self._text_abstract_result = ScrolledText(self._notebook_result)
        self._text_description_result = ScrolledText(self._notebook_result)
        self._text_claim_result = ScrolledText(self._notebook_result)

        self._notebook_result.add(self._text_abstract_result, text="摘要及其他缺陷")
        self._notebook_result.add(self._text_claim_result, text="权利要求书缺陷")
        self._notebook_result.add(self._text_description_result, text="说明书及附图缺陷")

        self.add(self._notebook_result, weight=1)
        self._notebook_result.enable_traversal()
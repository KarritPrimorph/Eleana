import tkinter as tk
import customtkinter


class CTkListbox(customtkinter.CTkFrame):

    def __init__(self,
                 master,
                 height: int = 100,
                 width: int = 200,
                 hightlight_color: str = "default",
                 fg_color: str = "transparent",
                 bg_color: str = None,
                 text_color: str = "default",
                 select_color: str = "default",
                 hover_color: str = "default",
                 border_width: int = 3,
                 font: tuple = "Arial 10",
                 multiple_selection: bool = False,
                 listvariable=None,
                 hover: bool = True,
                 command=None,
                 justify="left",
                 disable_selection=False,
                 gui_appearance=None,
                 **kwargs):

        super().__init__(master, width=width, height=height,
                         fg_color=fg_color, border_width=border_width)

        self.command = command
        self.multiple = multiple_selection
        self.disable_selection = disable_selection

        if not gui_appearance:
            gui_appearance = customtkinter.get_appearance_mode()

        if gui_appearance.lower() == 'light':
            default_bg = "#f0f0f0"
            default_fg = "#151515"
            default_select = "#999999"
        else:
            default_bg = "#2b2b2b"
            default_fg = "#eaeaea"
            default_select = "#3a7ebf"

        self.text_color = default_fg if text_color == "default" else text_color
        self.select_color = default_select if select_color == "default" else select_color
        self.font = ("Segoe UI", 13) if font == "default" else font

        selectmode = tk.MULTIPLE if self.multiple else tk.SINGLE

        # 🔥 Prawdziwy Listbox (wydajny)
        self.listbox = tk.Listbox(
            self,
            selectmode=selectmode,
            bg=default_bg,
            fg=self.text_color,
            selectbackground=self.select_color,
            selectforeground="white",
            highlightthickness=0,
            borderwidth=0,
            activestyle="none",
            font=self.font,
            justify=justify
        )

        # 🔥 Ładny CTk scrollbar
        self.scrollbar = customtkinter.CTkScrollbar(
            self, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.scrollbar.set)

        self.listbox.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Event
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        # Obsługa listvariable
        if listvariable:
            self.listvariable = listvariable
            self.listvariable.trace_add(
                'write', lambda a, b, c: self.update_listvar())
            self.update_listvar()

    # -------------------------------------------------
    # API zgodne z poprzednią wersją
    # -------------------------------------------------

    def insert(self, index, option, **kwargs):
        self.listbox.insert(index, option)

    def delete(self, index, last=None):
        if str(index).lower() == "all":
            self.listbox.delete(0, tk.END)
        else:
            self.listbox.delete(index, last)

    def size(self):
        return self.listbox.size()

    def get(self, index=None):
        if index is None:
            sel = self.listbox.curselection()
            if not sel:
                return None
            if self.multiple:
                return [self.listbox.get(i) for i in sel]
            return self.listbox.get(sel[0])
        else:
            if str(index).lower() == "all":
                return list(self.listbox.get(0, tk.END))
            return self.listbox.get(index)

    def curselection(self):
        return self.listbox.curselection()

    def select(self, index):
        if self.disable_selection:
            return
        self.listbox.selection_set(index)
        self._trigger_command()

    def deselect(self, index):
        self.listbox.selection_clear(index)

    def activate(self, index):
        self.select(index)

    def deactivate(self, index):
        self.deselect(index)

    def move_up(self, index):
        if index <= 0:
            return
        text = self.listbox.get(index)
        self.listbox.delete(index)
        self.listbox.insert(index - 1, text)
        self.select(index - 1)

    def move_down(self, index):
        if index >= self.size() - 1:
            return
        text = self.listbox.get(index)
        self.listbox.delete(index)
        self.listbox.insert(index + 1, text)
        self.select(index + 1)

    def configure(self, **kwargs):
        if "text_color" in kwargs:
            self.listbox.config(fg=kwargs.pop("text_color"))
        if "highlight_color" in kwargs:
            self.listbox.config(
                selectbackground=kwargs.pop("highlight_color"))
        if "font" in kwargs:
            self.listbox.config(font=kwargs.pop("font"))
        if "command" in kwargs:
            self.command = kwargs.pop("command")

        super().configure(**kwargs)

    def update_listvar(self):
        values = list(eval(self.listvariable.get()))
        self.delete("all")
        for i in values:
            self.insert(tk.END, i)

    # -------------------------------------------------

    def _on_select(self, event):
        if self.command:
            self._trigger_command()

    def _trigger_command(self):
        value = self.get()
        if self.command:
            self.command(value)
from modules.CTkListbox import CTkListbox
import tkinter as tk
import tkinter.font as tkfont
import customtkinter


class MyCombobox(customtkinter.CTkFrame):

    def __init__(
        self,
        master,
        values=None,
        width=200,
        dropdown_width=None,
        dropdown_height=400,
        border_color=None,
        command=None,
        fg_color="#505050",
        height=32
    ):

        super().__init__(
            master,
            fg_color="transparent",
            border_color=border_color,
            border_width=2,
            corner_radius=6,
            width=width,
            height=height
        )

        self.pack_propagate(False)

        self.values = values or []
        self._values = list(self.values)
        self.filtered = list(self.values)

        self.command = command
        self.dropdown_height = dropdown_height
        self.dropdown_width = dropdown_width

        self._dropdown_blocked = False

        self.popup = None
        self.var = tk.StringVar()

        # -------------------------
        # INNER FRAME
        # -------------------------

        self.inner = customtkinter.CTkFrame(
            self,
            fg_color=fg_color,
            corner_radius=4
        )

        self.inner.pack(fill="both", expand=True, padx=3, pady=2)

        # -------------------------
        # ENTRY
        # -------------------------

        self.entry = customtkinter.CTkEntry(
            self.inner,
            textvariable=self.var,
            border_width=0,
            fg_color=fg_color,
            corner_radius=0
        )

        self.entry.pack(side="left", fill="both", expand=True, padx=(6,2))

        # -------------------------
        # SEPARATOR
        # -------------------------

        self.separator = customtkinter.CTkFrame(
            self.inner,
            width=1,
            fg_color="#808080"
        )

        self.separator.pack(side="right", fill="y", padx=2)

        # -------------------------
        # BUTTON
        # -------------------------

        self.button = customtkinter.CTkButton(
            self.inner,
            text="☰",
            width=26,
            fg_color=fg_color,
            border_width=0,
            hover_color="#606060",
            command=self.open_dropdown,
            corner_radius=0,
            text_color=border_color
        )

        self.button.pack(side="right")

        # -------------------------
        # BINDINGS
        # -------------------------

        self.entry.bind("<Button-1>", self.open_dropdown)
        self.entry.bind("<KeyRelease>", self.filter)
        self.entry.bind("<Down>", self.focus_list)
        self.entry.bind("<Return>", self._on_return)
        self.entry.bind("<Escape>", self._on_escape)

    # -------------------------------------------------

    def calc_width(self):

        if self.dropdown_width:
            return self.dropdown_width

        font = tkfont.Font(font=self.entry.cget("font"))

        max_pixels = 0

        for v in self.values:
            max_pixels = max(max_pixels, font.measure(v))

        return max(max_pixels + 40, self.entry.winfo_width())

    # -------------------------------------------------

    def open_dropdown(self, event=None):

        if self.popup:
            return

        if self._dropdown_blocked:
            self._dropdown_blocked = False
            return

        self.filtered = list(self._values)

        width = self.calc_width()

        self.popup = tk.Toplevel(self)
        self.popup.overrideredirect(True)

        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()

        self.popup.geometry(f"{width}x{self.dropdown_height}+{x}+{y}")

        self.listbox = CTkListbox(
            self.popup,
            width=width,
            height=self.dropdown_height,
            command=self._on_listbox_select,
            border_width=10,
            font="Arial 12"
        )

        self.listbox.pack(fill="both", expand=True)

        self.update_list()

        root = self.winfo_toplevel()
        root.bind_all("<Button-1>", self._on_click_outside, add="+")

    # -------------------------------------------------

    def _on_click_outside(self, event):

        if not self.popup:
            return

        widget = event.widget

        # sprawdzamy czy kliknięto gdzieś w popupie
        parent = widget
        while parent is not None:
            if parent == self.popup:
                return
            parent = parent.master

        self.close_dropdown()
    # -------------------------------------------------

    def _on_escape(self, event=None):

        self.close_dropdown()
        self._dropdown_blocked = True

        return "break"

    # -------------------------------------------------

    def update_list(self):

        self.listbox.delete("all")

        for v in self.filtered:
            self.listbox.insert("end", v)

    # -------------------------------------------------

    def filter(self, event=None):

        text = self.var.get().lower()

        self.filtered = [v for v in self._values if text in v.lower()]

        if not self.popup:
            self.open_dropdown()

        self.update_list()

    # -------------------------------------------------

    def focus_list(self, event=None):

        if self.popup and self.listbox.size() > 0:

            self.listbox.listbox.focus_set()
            self.listbox.select(0)

    # -------------------------------------------------

    def _on_listbox_select(self, value):

        self.var.set(value)

        self.close_dropdown()

        if self.command:
            self.command(value)

    # -------------------------------------------------

    def _on_return(self, event=None):

        value = self.var.get()

        if value in self._values:

            if self.command:
                self.command(value)

        else:
            self.var.set("")

    # -------------------------------------------------

    def select(self, value):

        if value in self._values:

            self.var.set(value)

            if self.command:
                self.command(value)

        self.close_dropdown()

    # -------------------------------------------------

    def close_dropdown(self):

        if self.popup:

            self.popup.destroy()
            self.popup = None

            root = self.winfo_toplevel()
            root.unbind_all("<Button-1>")

    # -------------------------------------------------

    def configure(self, **kwargs):

        if "values" in kwargs:

            values = kwargs.pop("values")

            self.values = list(values)
            self._values = list(values)
            self.filtered = list(values)

            if self.popup:
                self.update_list()

        super().configure(**kwargs)

    # -------------------------------------------------

    def set(self, value):

        if value in self._values:

            self.var.set(value)

            return True

        return False

    # -------------------------------------------------

    def get(self):

        return self.var.get()
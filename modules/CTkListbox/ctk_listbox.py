"""
Custom ListBox for customtkinter
Author: Akash Bora
"""

import customtkinter


class CTkListbox(customtkinter.CTkScrollableFrame):

    def __init__(self,
                 master: any,
                 height: int = 100,
                 width: int = 200,
                 hightlight_color: str = "default",
                 fg_color: str = "transparent",
                 bg_color: str = None,
                 text_color: str = "default",
                 select_color: str = "default",
                 hover_color: str = "default",
                 border_width: int = 3,
                 font: tuple = "default",
                 multiple_selection: bool = False,
                 listvariable=None,
                 hover: bool = True,
                 command=None,
                 justify="left",
                 disable_selection = False,
                 **kwargs):
        # mode = customtkinter.get_appearance_mode()
        self.disable_selection = disable_selection
        if customtkinter.get_appearance_mode() == 'Light':
            text_color = '#454545'
            select_color = '#bbbbbb'
            hover_color = '#aaaaaa'
        super().__init__(master, width=width, height=height, fg_color=fg_color, border_width=border_width, **kwargs)
        self._scrollbar.grid_configure(padx=(0, border_width + 4))
        self._scrollbar.configure(width=12)

        if bg_color:
            super().configure(bg_color=bg_color)

        self.select_color = customtkinter.ThemeManager.theme["CTkButton"][
            "fg_color"] if select_color == "default" else select_color
        self.text_color = customtkinter.ThemeManager.theme["CTkButton"][
            "text_color"] if text_color == "default" else text_color
        self.hover_color = customtkinter.ThemeManager.theme["CTkButton"][
            "hover_color"] if hover_color == "default" else hover_color
        self.font = (customtkinter.ThemeManager.theme["CTkFont"]["family"], 13) if font == "default" else font
        if justify == "left":
            self.justify = "w"
        elif justify == "right":
            self.justify = "e"
        else:
            self.justify = "c"
        self.buttons = {}
        self.command = command
        self.multiple = multiple_selection
        self.selected = None
        self.hover = hover
        self.end_num = 0
        self.selections = []

        if listvariable:
            self.listvariable = listvariable
            self.listvariable.trace_add('write', lambda a, b, c: self.update_listvar())
            self.update_listvar()

        super().bind("<Destroy>", lambda e: self.unbind_all("<Configure>"))

        # Mouse over widget bind
        self.mouse_over_widget = False
        self.bind("<Enter>", lambda e: self.set_mouse_over_widget(True))
        self.bind("<Leave>", lambda e: self.set_mouse_over_widget(False))
        # Scroll mouse bind
        self.bind("<MouseWheel>", self.on_mouse_wheel)  # Windows i macOS
        self.bind("<Button-4>", self.wheel_up)  # Linux
        self.bind("<Button-5>", self.wheel_down)  # Linux

    def set_mouse_over_widget(self, value):
        self.mouse_over_widget = value

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.wheel_up(event)
        else:
            self.wheel_down(event)

    def wheel_down(self, event):
        if not self.mouse_over_widget:
            return
        if self._scrollbar:
            current_position = self._scrollbar.get()[1]
            if current_position < 1.0:
                new_position = min(current_position + 0.01, 1.0)
                self._scrollbar.set(new_position - 0.01, new_position)
        self._parent_canvas.yview("scroll", int(100 / 20), "units")

    def wheel_up(self, event):
        if not self.mouse_over_widget:
            return
        if self._scrollbar:
            current_position = self._scrollbar.get()[0]
            if current_position > 0.0:
                new_position = max(current_position - 0.01, 0.0)
                self._scrollbar.set(new_position, new_position + 0.01)
        self._parent_canvas.yview("scroll", -int(100 / 20), "units")

    def update_listvar(self):
        values = list(eval(self.listvariable.get()))
        self.delete("all")
        for i in values:
            self.insert("END", option=i)

    def select(self, index):
        if self.disable_selection:
            return
        """Select the option."""
        for options in self.buttons.values():
            if options.winfo_exists():
                options.configure(fg_color="transparent")
        if self.multiple:
            if self.buttons[index] in self.selections:
                self.selections.remove(self.buttons[index])
                if self.buttons[index].winfo_exists():
                    self.buttons[index].configure(fg_color="transparent", hover=False)
                    self.after(100, lambda: self.buttons[index].configure(hover=self.hover))
            else:
                self.selections.append(self.buttons[index])
            for i in self.selections:
                if i.winfo_exists():
                    i.configure(fg_color=self.select_color, hover=False)
                    self.after(100, lambda button=i: button.configure(hover=self.hover))
        else:
            self.selected = self.buttons[index]
            if self.selected.winfo_exists():
                self.selected.configure(fg_color=self.select_color, hover=False)
                self.after(100, lambda: self.selected.configure(hover=self.hover))

        if self.command:
            self.command(self.get())

    def activate(self, index):
        if str(index).lower() == "all":
            if self.multiple:
                for i in self.buttons:
                    self.select(i)
            return
        selected = list(self.buttons.keys())[index]
        self.select(selected)

    def curselection(self):
        index = 0
        if self.multiple:
            indexes = []
            for i in self.buttons.values():
                if i in self.selections:
                    indexes.append(index)
                index += 1
            return tuple(indexes)

        else:
            for i in self.buttons.values():
                if i == self.selected:
                    return index
                else:
                    index += 1

    def bind(self, key, func):
        #super().bind_all(key, lambda e: func(self.get()), add="+")
        super().bind(key, lambda e: func(self.get()), add="+")

    def deselect(self, index):
        """Deselect the option."""
        if self.disable_selection:
            return
        if not self.multiple:
            if self.selected and self.selected.winfo_exists():
                self.selected.configure(fg_color="transparent")
            self.selected = None
            return
        if self.buttons[index] in self.selections:
            self.selections.remove(self.buttons[index])
            if self.buttons[index].winfo_exists():
                self.buttons[index].configure(fg_color="transparent")

    def deactivate(self, index):
        if str(index).lower() == "all":
            for i in self.buttons:
                self.deselect(i)
            return
        selected = list(self.buttons.keys())[index]
        self.deselect(selected)

    def insert(self, index, option, **args):
        """ add new option in the listbox """

        if str(index).lower() == "end":
            index = f"END{self.end_num}"
            self.end_num += 1

        if index in self.buttons:
            self.buttons[index].destroy()

        self.buttons[index] = customtkinter.CTkButton(self, text=option, fg_color="transparent", anchor=self.justify,
                                                      text_color=self.text_color, font=self.font,
                                                      hover_color=self.hover_color, **args)
        self.buttons[index].configure(command=lambda num=index: self.select(num))
        self.buttons[index].pack(padx=0, pady=(0, 5), fill="x", expand=True)

    def delete(self, index, last=None):
        """ delete options from the listbox """

        if str(index).lower() == "all":
            for i in self.buttons:
                self.buttons[i].destroy()
            self.buttons = {}
            self.end_num = 0
            return

        if str(index).lower() == "end":
            index = f"END{self.end_num}"
            self.end_num -= 1
        else:
            if int(index) == len(self.buttons):
                index = len(self.buttons) - 1
            if int(index) > len(self.buttons):
                return
            if not last:
                index = list(self.buttons.keys())[int(index)]

        if last:
            if str(last).lower() == "end":
                last = len(self.buttons) - 1
            elif int(last) >= len(self.buttons):
                last = len(self.buttons) - 1

            deleted_list = []
            for i in range(index, int(last) + 1):
                list(self.buttons.values())[i].destroy()
                deleted_list.append(list(self.buttons.keys())[i])
            for i in deleted_list:
                del self.buttons[i]
        else:
            self.buttons[index].destroy()
            del self.buttons[index]

    def size(self):
        """ return total number of items in the listbox """
        return len(self.buttons.keys())

    def get(self, index=None):
        """ get the selected value """
        if index:
            if str(index).lower() == "all":
                return list(item.cget("text") for item in self.buttons.values())
            else:
                index = list(self.buttons.keys())[int(index)]
                return self.buttons[index].cget("text")
        else:
            if self.multiple:
                return [x.cget("text") for x in self.selections] if len(self.selections) > 0 else None
            else:
                return self.selected.cget("text") if self.selected is not None else None

    def configure(self, **kwargs):
        """ configurable options of the listbox """

        if "hover_color" in kwargs:
            self.hover_color = kwargs.pop("hover_color")
            for i in self.buttons.values():
                i.configure(hover_color=self.hover_color)
        if "highlight_color" in kwargs:
            self.select_color = kwargs.pop("highlight_color")
            if self.selected: self.selected.configure(fg_color=self.select_color)
            if len(self.selections) > 0:
                for i in self.selections:
                    i.configure(fg_color=self.select_color)
        if "text_color" in kwargs:
            self.text_color = kwargs.pop("text_color")
            for i in self.buttons.values():
                i.configure(text=self.text_color)
        if "font" in kwargs:
            self.font = kwargs.pop("font")
            for i in self.buttons.values():
                i.configure(font=self.font)
        if "command" in kwargs:
            self.command = kwargs.pop("command")

        super().configure(**kwargs)

    def move_up(self, index):
        """ Move the option up in the listbox """
        if index > 0:
            current_key = list(self.buttons.keys())[index]
            previous_key = list(self.buttons.keys())[index - 1]

            # Store the text of the button to be moved
            current_text = self.buttons[current_key].cget("text")

            # Update the text of the buttons
            self.buttons[current_key].configure(text=self.buttons[previous_key].cget("text"))
            self.buttons[previous_key].configure(text=current_text)

            # Clear the selection from the current option
            self.deselect(current_key)

            # Update the selection
            self.select(previous_key)

            # Update the scrollbar position
            if self._parent_canvas.yview() != (0.0, 1.0):
                self._parent_canvas.yview("scroll", -int(100 / 6), "units")

    def move_down(self, index):
        """ Move the option down in the listbox """
        if index < len(self.buttons) - 1:
            current_key = list(self.buttons.keys())[index]
            next_key = list(self.buttons.keys())[index + 1]

            # Store the text of the button to be moved
            current_text = self.buttons[current_key].cget("text")

            # Update the text of the buttons
            self.buttons[current_key].configure(text=self.buttons[next_key].cget("text"))
            self.buttons[next_key].configure(text=current_text)

            # Clear the selection from the current option
            self.deselect(current_key)

            # Update the selection
            self.select(next_key)

            # Update the scrollbar position
            if self._parent_canvas.yview() != (0.0, 1.0):
                self._parent_canvas.yview("scroll", int(100 / 6), "units")

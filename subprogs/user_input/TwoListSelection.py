#!/usr/bin/python3

from modules.CTkListbox import CTkListbox
from subprogs.user_input.TwoListSelectionui import TwoListSelectionUI
from subprogs.user_input.single_dialog import SingleDialog

class TwoListSelection(TwoListSelectionUI):
    def __init__(self, master=None, title = "",
                 items = [],
                 selected_items = [],
                 remove_duplications = True,
                 left_label = "All Groups",
                 right_label = "Selected groups",
                 disable_new = True):

        super().__init__(master)

        self.master = master
        self.mainwindow = self.builder.get_object("toplevel1", self.master)
        self.response = None
        self.disable_new = disable_new

        # Configure Window
        self.mainwindow.title(title)

        # Configure GUI
        self.items_frame = self.builder.get_object("items_frame", self.mainwindow)
        self.selected_frame = self.builder.get_object("selected_frame", self.mainwindow)
        self.list_of_items = self.builder.get_object("list_of_items", self.mainwindow)
        self.list_of_selected = self.builder.get_object("list_of_selected", self.mainwindow)

        self.left_label = self.builder.get_object("left_label", self.mainwindow)
        self.right_label = self.builder.get_object("right_label", self.mainwindow)

        self.left_label.configure(text = left_label)
        self.right_label.configure(text = right_label)

        self.btn_create_new = self.builder.get_object("btn_create_new", self.mainwindow)
        if self.disable_new:
            self.btn_create_new.grid_remove()

        # Remove tkinter list
        self.list_of_selected.destroy()
        self.list_of_items.destroy()

        self.list_of_items = CTkListbox(self.items_frame, multiple_selection=True)
        self.list_of_items.grid(row=1, column=0, sticky="nsew")

        self.list_of_selected = CTkListbox(self.selected_frame, multiple_selection=True)
        self.list_of_selected.grid(row=1, column=0, sticky="nsew")

       # Prepare items for lists:
        self.remove_duplications = remove_duplications
        self.items = []
        self.selected_items = []
        if remove_duplications:
            for item in items:
                if item not in self.items:
                    self.items.append(item)
            for select in selected_items:
                if select not in self.selected_items:
                    self.selected_items.append(select)
        else:
            self.items = items
            self.selected_items = selected_items

        # Populate list
        self.populate_list(items = self.items, listbox=self.list_of_items)
        self.populate_list(items = self.selected_items, listbox=self.list_of_selected)

    def populate_list(self, listbox, items = None):
        ''' Place items to listbox'''
        if items:
            for i, item in enumerate(items):
                listbox.insert(i, item)

    def add_to_list(self):
        ''' Add selected items from list_of_items to selected_items '''
        items = self.list_of_items.get()
        already_selected = self.get_all_elements(self.list_of_selected)
        i = 0
        nr = len(already_selected)
        for item in items:
            if item not in already_selected:
                self.list_of_selected.insert(nr+i, item)
                i+=1
        self.list_of_items.deactivate("all")

    def get_all_elements(self, listbox):
        ''' Get all elements from listbox '''
        elements = []
        for i, button in enumerate(listbox.buttons):
            elements.append(listbox.buttons[i]._text)
        return elements


    def remove_from_list(self):
        all_elements = self.get_all_elements(self.list_of_selected)
        to_remove = self.list_of_selected.get()
        indexes = []
        for i, element in enumerate(to_remove):
            if element in all_elements:
                idx = all_elements.index(element)
                indexes.append(idx)
        indexes.sort(reverse=True)
        for idx in indexes:
            self.list_of_selected.delete(idx)

    def add_all(self):
        self.remove_all()
        items = self.get_all_elements(self.list_of_items)
        for i, item in enumerate(items):
            self.list_of_selected.insert(i, item)

    def create_new(self):
        dialog = SingleDialog(master=self.mainwindow, title = "Create new")
        response = dialog.get()
        if response:
            nr = len(self.get_all_elements(self.list_of_items))
            self.list_of_items.insert(nr,response)

    def remove_all(self):
        self.list_of_selected.delete("all")

    def cancel(self):
        self.response = None
        pass

    def accept(self):
        self.response = self.get_all_elements(self.list_of_selected)
        self.mainwindow.destroy()

    def get(self):
        if self.mainwindow.winfo_exists():
            self.master.wait_window(self.mainwindow)
        return self.response

    def cancel(self, event = None):
        self.mainwindow.destroy()


if __name__ == "__main__":
    app = TwoListSelection()
    app.run()

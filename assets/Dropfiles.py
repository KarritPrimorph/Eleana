import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

class FileDropWindow:
    def __init__(self, master, callbacks):
        self.master = master
        self.callbacks = callbacks
        self.files = []
        self.master.iconify()
        self.master.withdraw()


        # Create window TkinterDnD
        self.root = TkinterDnD.Tk()
        self.root.geometry("400x300")
        self.root.title("Drag & Drop Files")
        self.root.configure(bg="#1f1f1f")

        # handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        # Frame CustomTkinter
        self.frame = ctk.CTkFrame(
            self.root,
            corner_radius=15,
            fg_color="#2b2b2b"
        )
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Label drag-and-drop
        self.label = ctk.CTkLabel(
            self.frame,
            text="Drop files here",
            fg_color="#3c3c3c",
            text_color="white",
            font=ctk.CTkFont(size=20, weight="bold"),
            justify="center",
            corner_radius=10
        )
        self.label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Register drag & drop
        self.label.drop_target_register(DND_FILES)
        self.label.dnd_bind('<<Drop>>', self.drop)

        # Start main loop Tkinter
        self.root.mainloop()

    def drop(self, event):
        ''' Trigger this when you drop file on the window '''
        new_files = self.root.tk.splitlist(event.data)
        loaded_any = False
        for file in new_files:
            type_ = file[-3:].lower()
            if type_ == 'dta' or type_ == 'dsc':
                method = 'import_elexsys'
            elif type_ == 'ele':
                method = 'load_project'
            elif type_ == 'spc':
                method = 'import_EMX'
            elif type_ == 'spe':
                method = 'import_magnettech1'
            elif type_ == 'lsx':
                method = 'import_excel'
            else:
                continue

            # Run function to import
            callback_func = self.callbacks.get(method) if self.callbacks else None
            if callback_func and callable(callback_func):
                callback_func(filename=file)
                loaded_any = True

        # Go to animation
        if loaded_any:
            self.flash_label()

    def flash_label(self):
        """ Flash after loading"""
        original_color = "#3c3c3c"
        flash_color = "#4caf50"  # delikatna zieleń
        self.label.configure(fg_color=flash_color)
        self.root.after(200, lambda: self.label.configure(fg_color=original_color))

    def close_window(self):
        self.master.deiconify()
        self.root.destroy()

if __name__ == '__main__':
    drop_app = FileDropWindow(master=None, callbacks=None)
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

class FileDropWindow:
    def __init__(self, master, callbacks):
        self.master = master
        self.master.iconify()
        self.callbacks = callbacks
        self.files = []

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
        for file in new_files:
            type_ = file[-3:].lower()
            if type_ == 'dta':
                method = 'import_elexsys'
            elif type_ == 'ele':
                method = 'load_project'
            elif type_ == 'spc':
                method = 'import_EMX'

            # Run function to import
            callback_func = self.callbacks.get(method)
            if callback_func and callable(callback_func):
                callback_func(filename = file)

    def close_window(self):
        self.master.deiconify()
        self.root.destroy()

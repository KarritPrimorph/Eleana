import os
import sys
import customtkinter as ctk
from PIL import Image, ImageTk

# ======================================================
# Setup working directory for PyInstaller
# ======================================================
if hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)

''' Create ROOT window '''
root = ctk.CTk()
root.withdraw()
root.overrideredirect(True)

''' Show Splash screen'''
splash = ctk.CTkToplevel(root)
splash.overrideredirect(True)

img = Image.open("./pixmaps/splash.png")

# --- CTkImage ---
ctk_img = ctk.CTkImage(
    light_image=img,
    dark_image=img,
    size=(700, 352)
)

# --- Label with the picture ---
bg_label = ctk.CTkLabel(
    splash,
    image=ctk_img,
    text="",
    fg_color="transparent",
    corner_radius=0
)
bg_label.pack(fill="both", expand=True)


# Set the splash to the center
w, h = img.width, img.height
screen_w = splash.winfo_screenwidth()
screen_h = splash.winfo_screenheight()
x = (screen_w - w) // 2
y = (screen_h - h) // 2
splash.geometry(f"{w}x{h}+{x}+{y}")
splash.update()

# BASIC CONFIGURATION
ELEANA_VERSION = 0.1  # Set the Eleana version. This will be stored in self.eleana.version
INTERPRETER = sys.executable  # Defines python version
DEVEL = True  # For final product set to False

# Import basic modules and add ./modules to sys.path
from pathlib import Path
import ctypes

# Set paths for assets, modules, subprogs and widgets
PROJECT_PATH = Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "Eleana_interface.ui"
MODULES = PROJECT_PATH / "modules"
ASSETS = PROJECT_PATH / "assets"
SUBPROGS = PROJECT_PATH / "subprogs"
WIDGETS = PROJECT_PATH / "widgets"
PIXMAPS = PROJECT_PATH / "pixmaps"

from assets.Eleana import Eleana
from assets.CommandProcessor import CommandProcessor

# Import External modules required
import numpy as np

# Import modules from ./modules folder
from assets.Application import Application
from modules.CTkMessagebox import CTkMessagebox

# Import Eleana specific classes
# Widgets used by main application

''' STARTING THE APPLICATION '''
# Create general main instances for the program
if not DEVEL:
    # Switch off the error display in final product
    if os.name == 'posix':  # Unix/Linux/macOS
        sys.stderr = open(os.devnull, 'w')
    elif os.name == 'nt':  # Windows
        sys.stderr = open('nul', 'w')

    # Switch off nupy RankWarnings in Numpy
    import warnings
    warnings.simplefilter('ignore', np.exceptions.RankWarning)


# Run the application
if __name__ == "__main__":
    # Check if the program is started with root privileges:
    if os.name == 'nt':
        # Windows
        try:
            disp_warn = ctypes.windll.shell32.IsUserAnAdmin()
        except:
            disp_warn = False
    else:
        # Unix (Linux, macOS)
        disp_warn = os.geteuid() == 0

    # When root privileges detected, display warning
    if disp_warn:
        msg = CTkMessagebox(title="Warning!",
                            message="For safety reasons, this program should not be run with administrator privileges.",
                            icon="warning", option_1="Quit", option_2="Ignore")
        if msg.get() == "Quit":
            sys.exit()

    if not DEVEL:
        # Switch off the error display in final product
        if os.name == 'posix':  # Unix/Linux/macOS
            sys.stderr = open(os.devnull, 'w')
        elif os.name == 'nt':  # Windows
            sys.stderr = open('nul', 'w')

        # Switch off nupy RankWarnings in Numpy
        import warnings

        warnings.simplefilter('ignore', np.exceptions.RankWarning)



    ''' Create Main instances '''
    eleana = Eleana(version=ELEANA_VERSION, devel=DEVEL)
    # sound = Sound()
    cmd = CommandProcessor()

    # Create application instance
    app = Application(eleana, cmd, root)  # This is GUI

    # Start application and close splash
    app.run(splash = splash)

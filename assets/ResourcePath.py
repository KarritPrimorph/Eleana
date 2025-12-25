import sys
from pathlib import Path

def resource_path(rel_path):
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller
        return Path(sys._MEIPASS) / rel_path

    # Dev (uruchamiane z katalogu projektu)
    # __file__ wskazuje na plik, w którym jest wywołanie resource_path
    # Dlatego możemy wrócić do katalogu modułu i znaleźć zasoby w tym samym katalogu
    return Path(__file__).parent / rel_path

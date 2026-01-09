# Eleana
# Copyright (C) 2026 Marcin Sarewicz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.

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

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


import platform
import subprocess

class Sound:
    def beep(self):
        if platform.system() == 'Windows':
            import winsound
            winsound.Beep(500, 100)
        else:
            # Play sound in Unix/Linux/macOS
            command = 'paplay /usr/share/sounds/freedesktop/stereo/bell.oga'
            subprocess.run(command, shell=True)


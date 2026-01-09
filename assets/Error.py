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



from modules.CTkMessagebox.ctkmessagebox import CTkMessagebox

class Error:
    @staticmethod
    def show(info = '', details = '', title = '', master = None, wait = False):
        if details:
            message = info + f'\n\nDetails:\n{details}'
        else:
            message = info
        if not title:
            title = 'Error'
        error = CTkMessagebox(title=title, message=message, icon='cancel', master = master)
        if wait:
            error.get()

    @staticmethod
    def ask_for_option(option, info = '', details = '', title = '', option_2 = 'OK'):
        if details:
            message = info + f'\n\nDetails:\n{details}'
        else:
            message = info
        if not title:
            title = 'Dialog'
        question = CTkMessagebox(master = master, title=title, message=message, icon="warning", option_1=option_2, option_2=option)
        answer = question.get()
        return answer

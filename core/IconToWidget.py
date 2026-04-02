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


import customtkinter as ctk
from PIL import Image
from pathlib import Path
import weakref

class IconToWidget:
    @staticmethod
    def set(widget, png, iconset = 'default', size = (20,20)):
        png = png + '.png'
        icon_folder = Path('pixmaps', 'widget_icons', iconset, png)
        image = ctk.CTkImage(light_image=Image.open(icon_folder), size=size)
        widget.configure(image = image, compound='left')

    @staticmethod
    def set2id(id, png, app, iconset='default', size = (20,20)):
        widget = app.builder.get_object(id, app.mainwindow)
        IconToWidget.set(widget, png, iconset = iconset, size=size)

    @staticmethod
    def eleana(application, iconset = 'default'):
        app = weakref.proxy(application)
         # Here you define which widget gets icon. This is static
         #
         #          PYGUBU ID                   PNG FILE (no suffix)                SIZE
         #          ----------------------      --------------------------          ------------
        items = (( 'btn_swap'                  ,'btn_swap',                        (30,20)),
                  ( 'btn_second_modify'         ,'btn_modify',                      (20,20)),
                  ( 'btn_first_modify'          ,'btn_modify',                      (20,20)),
                  ( 'btn_first_to_result'       ,'to_result',                       (20,20)),
                  ( 'btn_second_to_result'      ,'to_result',                       (20,20)),
                  ( 'btn_replace_first'         ,'replace_first',                   (20,20)),
                  ( 'btn_replace_group'         ,'replace_group',                   (20,20)),
                  ( 'btn_clear_results'         ,'clear_results',                   (20,20)),
                  ( 'btn_add_to_group'          ,'btn_add_to_group',                (20,20)),
                  ( 'btn_delete_selected'       ,'btn_delete_selected',             (20,20)),
                  ( 'btn_all_to_group'          ,'btn_all_to_group',                (20,20)),
                  ('btn_all_to_new'             ,'btn_all_to_new',                  (20,20))
                )

        for item in items:
            id = item[0]
            png = item[1]
            size = item[2]
            IconToWidget.set2id(id=id, png=png, app = app, iconset = iconset, size = size)







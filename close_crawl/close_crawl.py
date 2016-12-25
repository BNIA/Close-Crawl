#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""close_crawl

TODO: DOCS
"""

from __future__ import absolute_import, print_function, unicode_literals

from os import path
from sys import platform

try:
    # Python 2
    import Tkinter as tk
    # from Tkinter import tk.Frame, tk.Tk
    import tkFileDialog as file_dialog
    import ttk
except ImportError:
    # Python 3
    import tkinter as tk
    from tkinter import filedialog as file_dialog
    from tkinter import ttk
from PIL import ImageTk, Image

from modules._version import __version__
from modules.close_crawl_cli import main

LARGE_FONT = ("Helvetica", 12)
SMALL_FONT = ("Helvetica", 9)
BASE_PATH = path.dirname(path.abspath(__file__))


class CloseCrawl(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Close Crawl {ver}".format(ver=__version__))

        # TODO: add bitmap icon for Windows systems
        if platform == "win32":
            # tk.Tk.iconbitmap(self, "logo_16.png")
            pass

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for window_frame in (WelcomePage, MainMenu, ScrapeMenu):

            frame = window_frame(container, self)
            self.frames[window_frame] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(WelcomePage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class GUIComponents():

    @staticmethod
    def exit_button(parent, controller):

        exit_button = tk.Button(
            parent, text="Exit",
            command=lambda: controller.quit()
        )

        exit_button.pack(pady=10, padx=10)


class WelcomePage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        welcome_image = Image.open(path.join(BASE_PATH, "static", "logo.png"))
        welcome_image = welcome_image.resize((250, 250), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(welcome_image)
        image_label = ttk.Label(self, image=photo)
        image_label.welcome_image = photo  # keep a reference
        image_label.pack(pady=10, padx=10)

        welcome_button = ttk.Button(
            self, text="Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        welcome_button.pack(padx=10)

        GUIComponents.exit_button(self, controller)


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Main Menu", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        run_button = ttk.Button(
            self, text="Scrape Cases",
            command=lambda: controller.show_frame(ScrapeMenu)
        )

        run_button.pack(pady=10, padx=10)

        view_button = ttk.Button(
            self, text="View Data",
            command=lambda: print("Not yet")
        )

        view_button.pack(pady=10, padx=10)

        GUIComponents.exit_button(self, controller)


class ScrapeMenu(tk.Frame):

    def __init__(self, parent, controller):

        self.dir_opt = {
            "parent": self,
            "mustexist": False,
            "title": "Directory to save output"
        }

        self.fields = [
            "Case Type",
            "Case Year",
            "Output",
            "Lower Bound",
            "Upper Bound",
        ]

        self.dir_path = path.dirname(__file__)

        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Scrape New Cases", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        entries = self.form(self)

        path_button = ttk.Button(
            self, text="Select Output Path",
            command=lambda: self.output_file_path()
        )

        path_button.pack(pady=10, padx=5)

        run_button = ttk.Button(
            self, text="Run",
            command=lambda: main(**self.unpack_form(self.fields, entries))
        )

        run_button.pack(pady=10, padx=5)

        GUIComponents.exit_button(self, controller)

    def form(self, parent):

        entries = []

        for field in self.fields:

            row = tk.Frame(parent)
            label = ttk.Label(row, width=15, text=field, anchor='w')

            entry = ttk.Entry(row)

            if field == "Output":
                entry.insert(0, "output.csv")

            row.pack(side="top", fill='x', padx=5, pady=5)
            label.pack(side="left")
            entry.pack(side="right", expand=True, fill='x')
            entries.append(entry)

        return entries

    def unpack_form(self, fields, entries):

        packed_params = {}

        for field, entry in zip(fields, entries):
            packed_params[str(field.lower().replace(' ', '_'))] = entry.get()

        packed_params["output"] = path.join(
            self.dir_path, packed_params["output"]
        )

        return packed_params

    def output_file_path(self):

        self.dir_path = file_dialog.askdirectory(**self.dir_opt)


if __name__ == '__main__':
    app = CloseCrawl()
    app.mainloop()

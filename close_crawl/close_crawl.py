#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""close_crawl

"""

from __future__ import absolute_import, print_function, unicode_literals

from os import path

from PIL import ImageTk, Image
try:
    # Python 2
    from Tkinter import Frame, Tk
    from ttk import Button, Entry, Label
except:
    # Python 3
    import tkinter as tk
    from tkinter.ttk import Button, Entry, Label

from modules._version import __version__
from modules.close_crawl_cli import main

LARGE_FONT = ("Verdana", 12)
BASE_PATH = path.dirname(path.abspath(__file__))


class CloseCrawl(Tk):

    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)
        Tk.wm_title(self, "Close Crawl " + __version__)
        # TODO: add icon on GUI that supports both OS
        # tk.Tk.iconbitmap(
        #     self, "/logo_16.ico"
        # )

        container = Frame(self)

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


class WelcomePage(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)

        welcome_image = Image.open(
            path.join(path.dirname(BASE_PATH), "static", "logo.png")
        )
        welcome_image = welcome_image.resize((250, 250), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(welcome_image)
        image_label = Label(self, image=photo)
        image_label.welcome_image = photo  # keep a reference
        image_label.pack(pady=10, padx=10)

        welcome_button = Button(
            self, text="Main Menu",
            command=lambda: controller.show_frame(MainMenu)
        )

        welcome_button.pack(padx=10)

        exit_button = Button(
            self, text="Exit",
            command=lambda: controller.quit()
        )

        exit_button.pack(pady=10, padx=10)


class MainMenu(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)
        label = Label(self, text="Main Menu", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        run_button = Button(
            self, text="Scrape Cases",
            command=lambda: controller.show_frame(ScrapeMenu)
        )

        run_button.pack(pady=10, padx=10)

        view_button = Button(
            self, text="View Data",
            command=lambda: print("Not yet")
        )

        view_button.pack(pady=10, padx=10)

        exit_button = Button(
            self, text="Exit",
            command=lambda: controller.quit()
        )

        exit_button.pack(pady=10, padx=10)


class ScrapeMenu(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self, parent)

        label = Label(self, text="Scrape New Cases", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        type_entry = Entry(self)
        type_entry.pack(side="right")

        type_label = Label(self, text="Case Type", font=LARGE_FONT)
        type_label.pack(side="left")

        exit_button = Button(
            self, text="Exit",
            command=lambda: controller.quit()
        )

        exit_button.pack(pady=10, padx=10)


if __name__ == '__main__':

    app = CloseCrawl()
    app.mainloop()

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 11:30:34 2018

@author: Annalise
"""

import tkinter as tk
from tkinter import ttk


LARGE_FONT = ("Verdan", 12)


def print_output(string_to_print):
    print(string_to_print)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="dino_cropped_lines.ico")
        tk.Tk.wm_title(self, "Annalise's Kick Ass Wind Modeling Program")

        container = tk.Frame(self)
        container.grid()
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.configure(background="black")
        # set up future frames
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.configure(background="black")
        opening_message = ('This program allows users to optimize wind farms '
                           + 'or analyze hard-coded turbine layouts!')
        label0 = tk.Label(self, text=opening_message, bg="black", fg="white",
                          font=LARGE_FONT)
        label0.grid(row=0, column=1)
        label = tk.Label(self, text="Start Page", bg="black", fg="purple",
                         font=LARGE_FONT)
        label.grid(row=0, column=0)

        # select an analysis
        message = ('Please select the analysis you wish to perform:')
        label1 = tk.Label(self, text=message, bg="black", fg="white")
        label1.grid(row=1, column=0, sticky=tk.E)
        analysis_selection = tk.StringVar(self)
        analyses = ["optimization", "layout analysis"]
        analysis_selection.set("layout analysis")
        analysis = ttk.OptionMenu(self, analysis_selection, *analyses)
        analysis.grid(row=1, column=1, sticky=tk.W)

#        button1 = ttk.Button(self, text="Visit Page 2",
#                             command=lambda: controller.show_frame(PageTwo))
#        button1.grid(row=2, column=0)

        # analysis selection
#        menu = tk.Menu(master)
#        master.config(menu=menu, background="black")
#        submenu = tk.Menu(menu)
#        menu.add_cascade(label="file", menu=submenu)
#        submenu.add_command(label="print results", command=print_output)
#        submenu.add_command(label="exit", command=frame.quit)
#
#
        # select optimization algorithm
#        algorithm_message = ("Please select your desired "
#                             + "optimization algorithm:")
#        label3 = tk.Label(self, text=algorithm_message,
#                          bg="black", fg="white")
#        label3.grid(row=2, column=0, sticky=tk.E)
#        algorithm_selection = tk.StringVar(master)
#        alogrithms = ["Extended Pattern Search", "Genetic Algorithm",
#                      "Particle Swarm Optimization"]
#        algorithm_selection.set("Extended Pattern Search")
#        algorithm = ttk.OptionMenu(self, algorithm_selection, *alogrithms)
#        algorithm.grid(row=2, column=1, sticky=tk.W)

        # select wake model
        wake_message = ("Please select your wake model:")
        label4 = tk.Label(self, text=wake_message,
                          bg="black", fg="white")
        label4.grid(row=3, column=0, sticky=tk.E)
        wake_selection = tk.StringVar(master)
        wake_models = ["Jensen 2D", "Jensen 3D",
                       "Jensen 2D - NWP", "Jensen 3D - NWP",
                       "WindSE2D (CFD)"]
        wake_selection.set("Jensen 3D")
        wake = ttk.OptionMenu(self, wake_selection, *wake_models)
        wake.grid(row=3, column=1, sticky=tk.W)

        # select onshore/offshore
        shore_message = ("Please select your farm location:")
        label5 = tk.Label(self, text=shore_message,
                          bg="black", fg="white")
        label5.grid(row=4, column=0, sticky=tk.E)
        shore_selection = tk.StringVar(master)
        shores = ["Onshore", "Offshore"]
        shore_selection.set("Onshore")
        shore = ttk.OptionMenu(self, shore_selection, *shores)
        shore.grid(row=4, column=1, sticky=tk.W)

        # select objective function
        obj_message = ("Please select your objective:")
        label6 = tk.Label(self, text=obj_message,
                          bg="black", fg="white")
        label6.grid(row=5, column=0, sticky=tk.E)
        obj_selection = tk.StringVar(master)
        objs = ["Annual energy production", "Cost per unit power",
                "Profit", "Levelized cost of energy", "Cost"]
        obj_selection.set("Annual energy production")
        obj = ttk.OptionMenu(self, obj_selection, *objs)
        obj.grid(row=5, column=1, sticky=tk.W)

        vals_to_get = [analysis_selection, wake_selection,
                       shore_selection, obj_selection]
        button0 = ttk.Button(self, text="Get Values",
                             command=lambda: self.get_values(vals_to_get,
                                                             controller))
        button0.grid(row=79, column=80)
#        button1 = ttk.Button(self, text="Visit Page 1",
#                             command=lambda: controller.show_frame(PageOne))
#        button1.grid(row=80, column=80)

    def get_values(self, values, controller):
        inputs = [i.get() for i in values]
        print(inputs)
        controller.show_frame(PageOne)
        return inputs

#        # status label
#        status_frame = tk.Frame(master)
#        status_frame.grid(sticky=tk.S)
#        status = tk.Label(status_frame, text="waiting for user input", bd=1,
#                          relief=tk.SUNKEN, anchor=tk.E)
#        status.grid(sticky=tk.E)


class PageOne(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.configure(background="black")
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.grid(row=0, column=0)
        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.grid(row=1, column=0)
        button2 = ttk.Button(self, text="To Page 2",
                             command=lambda: controller.show_frame(PageTwo))
        button2.grid(row=2, column=0)


class PageTwo(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.configure(background="black")
        label = tk.Label(self, text="Page Two", font=LARGE_FONT)
        label.grid(row=0, column=0)
        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.grid(row=1, column=0)
        button2 = ttk.Button(self, text="To Page One",
                             command=lambda: controller.show_frame(PageOne))
        button2.grid(row=2, column=0)


if __name__ == "__main__":
    app = App()
    # Start GUI
    app.mainloop()

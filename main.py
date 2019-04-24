"""
This is the main file for Animation creator.

Animation creator is a simple tools for create the
2D skeleton animation and export it to GIF or atlas.
"""

import os
import tkinter
import tkinter.ttk

from tkinter.filedialog import askdirectory

from model import Project
import command


# class View:
#    pass

# class Controller:
#    pass


class MainWindow(tkinter.Tk):
    """This is main window of the aplication. It contains static UI."""
    def __init__(self, project, command_list):
        tkinter.Tk.__init__(self)
        self.title("Animation creator")
        self._init_menu()
        self._init_work_area()
        self.geometry("950x550+300+300")
        self.__project = project
        self.__command_list = command_list

    def _init_menu(self):
        self.main_menu = tkinter.Menu(self)
        self.config(menu=self.main_menu)

        file_menu = tkinter.Menu(self.main_menu)
        file_menu.add_command(label="Open Project", command=self.load_project)
        file_menu.add_command(label="Save Project", command=self.save_project)
        file_menu.add_command(label="Exit", command=self.quit)
        self.main_menu.add_cascade(label="File", menu=file_menu)

        edit_menu = tkinter.Menu(self.main_menu)
        edit_menu.add_command(label="Redo", command=commands.redo)
        edit_menu.add_command(label="Undo", command=commands.undo)

        add_menu = tkinter.Menu(edit_menu)
        add_menu.add_command(label="Animation")
        add_menu.add_command(label="State")
        add_menu.add_command(label="Skeleton")
        add_menu.add_command(label="Bone")

        edit_menu.add_cascade(label="Add", menu=add_menu)
        self.main_menu.add_cascade(label="Edit", menu=edit_menu)

        help_menu = tkinter.Menu(self.main_menu)
        help_menu.add_command(label="Help")
        self.main_menu.add_cascade(label="Help", menu=help_menu)

    def _init_work_area(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.canvas = tkinter.Canvas(background="white")
        self.canvas.grid(row=0, column=0, sticky=tkinter.N+tkinter.E+tkinter.S+tkinter.W)

        self.options = tkinter.Frame(background="blue")
        self.options.grid(row=0, column=1, sticky=tkinter.N+tkinter.E+tkinter.S+tkinter.W)

        self.project_view = tkinter.ttk.Treeview()
        self.project_view.grid(row=0, column=2, sticky=tkinter.N+tkinter.E+tkinter.S+tkinter.W)

    def load_project(self):
        path_to_project_dir = askdirectory()
        if path_to_project_dir:
            self.__project.load(path_to_project_dir)
        self.__command_list.reset()

    def save_project(self):
        path_to_project_dir = askdirectory()
        if path_to_project_dir:
            self.__project.save(path_to_project_dir)


if __name__ == "__main__":
    project = Project()
    commands = command.CommandList(project)

    APP = MainWindow(project, commands)
    APP.mainloop()

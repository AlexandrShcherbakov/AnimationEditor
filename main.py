"""
This is the main file for Animation creator.

Animation creator is a simple tools for create the
2D skeleton animation and export it to GIF or atlas.
"""

import os
import tkinter
import tkinter.ttk

from tkinter.filedialog import askdirectory

from model import Project, CircleBone, SegmentBone, Skeleton, Animation, SkeletonState
import canvas
import command
import editor_view
import tree


class MainWindow(tkinter.Tk):
    """This is main window of the aplication. It contains static UI."""
    def __init__(self, project, command_list):
        tkinter.Tk.__init__(self)
        self.title("Animation creator")
        self.__command_list = command_list
        self.__project = project
        self._init_menu()
        self._init_work_area()
        self.geometry("950x550+300+300")

    def _init_menu(self):
        self.main_menu = tkinter.Menu(self)
        self.config(menu=self.main_menu)

        file_menu = tkinter.Menu(self.main_menu)
        file_menu.add_command(label="Open Project", command=self.load_project)
        file_menu.add_command(label="Save Project", command=self.save_project)
        file_menu.add_command(label="Exit", command=self.quit)
        self.main_menu.add_cascade(label="File", menu=file_menu)

        edit_menu = tkinter.Menu(self.main_menu)
        edit_menu.add_command(label="Redo", command=self.__command_list.redo)
        edit_menu.add_command(label="Undo", command=self.__command_list.undo)

        self.add_menu = tkinter.Menu(edit_menu)
        self.add_menu.add_command(label="Animation", command=lambda: self.__command_list.add_command(
            command.AddAnimationCommand(Animation())
        ))
        self.add_menu.add_command(label="State", command=lambda: self.__command_list.add_command(
            command.AddStateCommand(SkeletonState())
        ))
        self.add_menu.add_command(label="Skeleton", command=lambda: self.__command_list.add_command(
            command.AddSkeletonCommand(Skeleton())
        ))
        self.add_menu.add_command(label="Line bone", command=lambda: self.__command_list.add_command(
            command.AddBoneCommand(SegmentBone(50, 0, (100, 100)))
        ))
        self.add_menu.add_command(label="Circle bone", command=lambda: self.__command_list.add_command(
            command.AddBoneCommand(CircleBone(50, (100, 100)))
        ))

        edit_menu.add_cascade(label="Add", menu=self.add_menu)
        self.main_menu.add_cascade(label="Edit", menu=edit_menu)

        help_menu = tkinter.Menu(self.main_menu)
        help_menu.add_command(label="Help")
        self.main_menu.add_cascade(label="Help", menu=help_menu)

        self.__project.register_view(self)

    def _init_work_area(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.canvas = canvas.ResourceViewer(self.__command_list)
        self.canvas.grid(row=0, column=0, sticky=tkinter.N+tkinter.E+tkinter.S+tkinter.W)
        self.__project.register_view(self.canvas)

        self.options = editor_view.ResourceEditorViewer(self, self.__command_list)
        self.options.grid(row=0, column=1, sticky=tkinter.N+tkinter.E+tkinter.S+tkinter.W)
        self.__project.register_view(self.options)

        self.project_view = tree.ProjectHierarchyView(self.__command_list)
        self.project_view.grid(row=0, column=3, sticky=tkinter.N+tkinter.E+tkinter.S+tkinter.W)
        self.__project.register_view(self.project_view)

    def load_project(self):
        path_to_project_dir = askdirectory()
        if path_to_project_dir:
            self.__project.load(path_to_project_dir)
        self.__command_list.reset()

    def save_project(self):
        path_to_project_dir = askdirectory()
        if path_to_project_dir:
            self.__project.save(path_to_project_dir)

    def on_model_changed(self, model):
        TYPES_TO_ADD = 6
        for i in range(TYPES_TO_ADD):
            self.add_menu.entryconfig(i, state="disabled")
        if isinstance(model.active_element, Skeleton):
            self.add_menu.entryconfig("Line bone", state="normal")
            self.add_menu.entryconfig("Circle bone", state="normal")
        if isinstance(model.active_element, Project):
            self.add_menu.entryconfig("Animation", state="normal")
            self.add_menu.entryconfig("Skeleton", state="normal")
        if isinstance(model.active_element, Animation):
            self.add_menu.entryconfig("State", state="normal")


if __name__ == "__main__":
    project = Project()
    commands = command.CommandList(project)

    APP = MainWindow(project, commands)
    APP.mainloop()

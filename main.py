"""
This is the main file for Animation creator.

Animation creator is a simple tools for create the
2D skeleton animation and export it to GIF or atlas.
"""

import tkinter
import tkinter.ttk
import gettext

from tkinter.filedialog import askdirectory

from model import Project, CircleBone, SegmentBone, Skeleton, Animation, SkeletonState
import canvas
import command
import editor_view
import tree

gettext.install('app', '.')


class MainWindow(tkinter.Tk):
    """This is main window of the aplication. It contains static UI."""
    def __init__(self, project, command_list):
        tkinter.Tk.__init__(self)
        self.title(_("Animation creator"))
        self.__command_list = command_list
        self.__project = project
        self._init_menu()
        self._init_work_area()
        self.geometry("950x550+300+300")

    def _init_menu(self):
        self.main_menu = tkinter.Menu(self)
        self.config(menu=self.main_menu)

        file_menu = tkinter.Menu(self.main_menu)
        file_menu.add_command(label=_("Open Project"), command=self.load_project)
        file_menu.add_command(label=_("Save Project"), command=self.save_project)
        file_menu.add_command(label=_("Exit"), command=self.quit)
        self.main_menu.add_cascade(label=_("File"), menu=file_menu)

        edit_menu = tkinter.Menu(self.main_menu)
        edit_menu.add_command(label=_("Redo"), command=self.__command_list.redo)
        edit_menu.add_command(label=_("Undo"), command=self.__command_list.undo)

        self.add_menu = tkinter.Menu(edit_menu)
        self.add_menu.add_command(label=_("Animation"), command=lambda: self.__command_list.add_command(
            command.AddAnimationCommand(Animation())
        ))
        self.add_menu.add_command(label=_("State"), command=lambda: self.__command_list.add_command(
            command.AddStateCommand(SkeletonState())
        ))
        self.add_menu.add_command(label=_("Skeleton"), command=lambda: self.__command_list.add_command(
            command.AddSkeletonCommand(Skeleton())
        ))
        self.add_menu.add_command(label=_("Line bone"), command=lambda: self.__command_list.add_command(
            command.AddBoneCommand(SegmentBone(50, 0, (100, 100)))
        ))
        self.add_menu.add_command(label=_("Circle bone"), command=lambda: self.__command_list.add_command(
            command.AddBoneCommand(CircleBone(50, (100, 100)))
        ))

        edit_menu.add_cascade(label=_("Add"), menu=self.add_menu)
        self.main_menu.add_cascade(label=_("Edit"), menu=edit_menu)

        help_menu = tkinter.Menu(self.main_menu)
        help_menu.add_command(label=_("Help"))
        self.main_menu.add_cascade(label=_("Help"), menu=help_menu)

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
            self.add_menu.entryconfig(_("Line bone"), state="normal")
            self.add_menu.entryconfig(_("Circle bone"), state="normal")
        if isinstance(model.active_element, Project):
            self.add_menu.entryconfig(_("Animation"), state="normal")
            self.add_menu.entryconfig(_("Skeleton"), state="normal")
        if isinstance(model.active_element, Animation):
            self.add_menu.entryconfig(_("State"), state="normal")


if __name__ == "__main__":
    project = Project()
    commands = command.CommandList(project)

    APP = MainWindow(project, commands)
    APP.mainloop()

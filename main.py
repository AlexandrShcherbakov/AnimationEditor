"""
This is the main file for Animation creator.

Animation creator is a simple tools for create the
2D skeleton animation and export it to GIF or atlas.
"""

import os
import tkinter
import tkinter.ttk

from model import Skeleton, Animation
from settings import ProjectSettings
import command


class Project:
    """
    Main class of the project.
    Contains lists of entities (skeletons and animations).
    """

    def __init__(self):
        self.active_element = self

        self.__skeletons = list()
        self.__animations = list()

    def has_skeleton(self, name: str):
        return any(name == skeleton.name for skeleton in self.__skeletons)

    def has_animation(self, name: str):
        return any(name == animation.name for animation in self.__animations)

    def get_skeleton(self, name: str):
        return list(filter(lambda s: s.name == name, self.__skeletons))[0] if self.has_skeleton(name) else None

    def get_animation(self, name: str):
        return list(filter(lambda a: a.name == name, self.__animations))[0] if self.has_animation(name) else None

    @property
    def number_of_skeletons(self):
        return len(self.__skeletons)

    @property
    def number_of_animations(self):
        return len(self.__animations)

    def add_skeleton(self, skeleton: Skeleton):
        if not self.has_skeleton(skeleton.name):
            self.__skeletons.append(skeleton)
        else:
            raise NameError(f'Skeleton with name {skeleton.name} already exists in the project.')

    def remove_skeleton(self, skeleton_id: int):
        if skeleton_id < self.number_of_skeletons:
            self.__skeletons.pop(skeleton_id)
        else:
            raise IndexError(f'Project does not have a skeleton with index {skeleton_id}. '
                             f'It has only {self.number_of_skeletons} skeletons.')

    def add_animation(self, animation: Animation):
        if not self.has_animation(animation.name):
            self.__animations.append(animation)
        else:
            raise NameError(f'Animation with name {animation.name} already exists in the project.')

    def remove_animation(self, animation_id: int):
        if animation_id < self.number_of_animations:
            self.__animations.pop(animation_id)
        else:
            raise IndexError(f'Project does not have an animation with index {animation_id}. '
                             f'It has only {self.number_of_animations} animations.')

    def load(self):
        for filename in os.listdir(ProjectSettings.skeletons_dir):
            if filename.endswith('.json'):
                skeleton = Skeleton(name=filename[:-5])
                skeleton.load()
                self.add_skeleton(skeleton)

        for filename in os.listdir(ProjectSettings.animations_dir):
            if filename.endswith('.json'):
                animation = Animation(name=filename[:-5])
                skeleton_name = animation.load()
                animation.set_skeleton(self.get_skeleton(skeleton_name))
                self.add_animation(animation)

#class View:
#    pass

#class Controller:
#    pass


class MainWindow(tkinter.Tk):
    """This is main window of the aplication. It contains static UI."""
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("Animation creator")
        self._init_menu()
        self._init_work_area()
        self.geometry("950x550+300+300")

    def _init_menu(self):
        self.main_menu = tkinter.Menu(self)
        self.config(menu=self.main_menu)

        file_menu = tkinter.Menu(self.main_menu)
        file_menu.add_command(label="Open Project")
        file_menu.add_command(label="Save Project")
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


if __name__ == "__main__":
    project = Project()
    commands = command.CommandList(project)

    APP = MainWindow()
    APP.mainloop()

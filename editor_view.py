import tkinter

import command
from model import Skeleton, SegmentBone, Bone


class ResourceEditorViewer(tkinter.Frame):
    def __init__(self, command_list):
        tkinter.Frame.__init__(self)
        self.__command_list = command_list

    def __draw_bone(self, bone):
        if isinstance(bone, SegmentBone):
            params = bone.to_dict()
            end_x = params["position"][0] + params["length"] * math.cos(params["rotation"])
            end_y = params["position"][1] + params["length"] * math.sin(params["rotation"])
            self.create_line(
                (params["position"][0], params["position"][0], end_x, end_y),
                fill="#{:02x}{:02x}{:02x}".format(*params["color"]),
                width=params["thickness"]
            )

    def __draw_skeleton(self, skeleton):
        for i in range(skeleton.number_of_bones):
            self.__draw_bone(skeleton.get_bone(i))

    def on_model_changed(self, model):
        for widget in self.winfo_children():
            widget.destroy()
        last_row = 0
        save_command = None
        if isinstance(model.active_element, Skeleton):
            lb = tkinter.Label(self, text="Name:")
            lb.grid(row=0, column=0)
            name = tkinter.Entry(self, bg="white")
            name.insert("end", model.active_element.name)
            name.grid(row=0, column=1)
            last_row = 1

            def save_command:
                self.__command_list.add_command(command.PatchCommand({"name": name.get()}))

        if isinstance(model.active_element, Bone):
            lb = tkinter.Label(self, text="Name:")
            lb.grid(row=0, column=0)
            name = tkinter.Entry(self, bg="white")
            name.insert("end", model.active_element.name)
            name.grid(row=0, column=1)
            last_row = 1

            def save_command:
                self.__command_list.add_command(command.PatchCommand({"name": name.get()}))

        save = tkinter.Button(self, text="Save", command=save_command)
        save.grid(row=last_row, column=0)

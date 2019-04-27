import tkinter

import command
from model import Skeleton, SegmentBone, CircleBone, Animation


class ResourceEditorViewer(tkinter.Frame):
    def __init__(self, command_list):
        tkinter.Frame.__init__(self)
        self.__command_list = command_list

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

            def save_command():
                self.__command_list.add_command(command.PatchCommand({"name": name.get()}))

        if isinstance(model.active_element, CircleBone):
            lb = tkinter.Label(self, text="Name:")
            lb.grid(row=0, column=0)
            name = tkinter.Entry(self, bg="white")
            name.insert("end", model.active_element.name)
            name.grid(row=0, column=1)

            lb = tkinter.Label(self, text="Position:")
            lb.grid(row=1, column=0)
            pos_x = tkinter.Entry(self, bg="white")
            pos_x.insert("end", model.active_element.to_dict()["position"][0])
            pos_x.grid(row=1, column=1)
            pos_y = tkinter.Entry(self, bg="white")
            pos_y.insert("end", model.active_element.to_dict()["position"][1])
            pos_y.grid(row=1, column=2)

            lb = tkinter.Label(self, text="Thickness:")
            lb.grid(row=2, column=0)
            thickness = tkinter.Entry(self, bg="white")
            thickness.insert("end", model.active_element.to_dict()["thickness"])
            thickness.grid(row=2, column=1)

            lb = tkinter.Label(self, text="Color:")
            lb.grid(row=3, column=0)
            col_r = tkinter.Entry(self, bg="white")
            col_r.insert("end", model.active_element.to_dict()["color"][0])
            col_r.grid(row=3, column=1)
            col_g = tkinter.Entry(self, bg="white")
            col_g.insert("end", model.active_element.to_dict()["color"][1])
            col_g.grid(row=3, column=2)
            col_b = tkinter.Entry(self, bg="white")
            col_b.insert("end", model.active_element.to_dict()["color"][2])
            col_b.grid(row=3, column=3)

            lb = tkinter.Label(self, text="Radius:")
            lb.grid(row=4, column=0)
            radius = tkinter.Entry(self, bg="white")
            radius.insert("end", model.active_element.to_dict()["radius"])
            radius.grid(row=4, column=1)

            last_row = 5

            def save_command():
                self.__command_list.add_command(command.PatchCommand({
                    "name": name.get(),
                    "position": (int(pos_x.get()), int(pos_y.get())),
                    "thickness": float(thickness.get()),
                    "color": (int(col_r.get()), int(col_g.get()), int(col_b.get())),
                    "radius": float(radius.get()),
                }))

        if isinstance(model.active_element, SegmentBone):
            lb = tkinter.Label(self, text="Name:")
            lb.grid(row=0, column=0)
            name = tkinter.Entry(self, bg="white")
            name.insert("end", model.active_element.name)
            name.grid(row=0, column=1)

            lb = tkinter.Label(self, text="Position:")
            lb.grid(row=1, column=0)
            pos_x = tkinter.Entry(self, bg="white")
            pos_x.insert("end", model.active_element.to_dict()["position"][0])
            pos_x.grid(row=1, column=1)
            pos_y = tkinter.Entry(self, bg="white")
            pos_y.insert("end", model.active_element.to_dict()["position"][1])
            pos_y.grid(row=1, column=2)

            lb = tkinter.Label(self, text="Thickness:")
            lb.grid(row=2, column=0)
            thickness = tkinter.Entry(self, bg="white")
            thickness.insert("end", model.active_element.to_dict()["thickness"])
            thickness.grid(row=2, column=1)

            lb = tkinter.Label(self, text="Color:")
            lb.grid(row=3, column=0)
            col_r = tkinter.Entry(self, bg="white")
            col_r.insert("end", model.active_element.to_dict()["color"][0])
            col_r.grid(row=3, column=1)
            col_g = tkinter.Entry(self, bg="white")
            col_g.insert("end", model.active_element.to_dict()["color"][1])
            col_g.grid(row=3, column=2)
            col_b = tkinter.Entry(self, bg="white")
            col_b.insert("end", model.active_element.to_dict()["color"][2])
            col_b.grid(row=3, column=3)

            lb = tkinter.Label(self, text="Length:")
            lb.grid(row=4, column=0)
            length = tkinter.Entry(self, bg="white")
            length.insert("end", model.active_element.to_dict()["length"])
            length.grid(row=4, column=1)

            lb = tkinter.Label(self, text="Rotation:")
            lb.grid(row=5, column=0)
            rotate = tkinter.Entry(self, bg="white")
            rotate.insert("end", model.active_element.to_dict()["rotation"])
            rotate.grid(row=5, column=1)

            last_row = 6

            def save_command():
                self.__command_list.add_command(command.PatchCommand({
                    "name": name.get(),
                    "position": (int(pos_x.get()), int(pos_y.get())),
                    "thickness": float(thickness.get()),
                    "color": (int(col_r.get()), int(col_g.get()), int(col_b.get())),
                    "length": float(length.get()),
                    "rotation": float(rotate.get()),
                }))

        if isinstance(model.active_element, Animation):
            lb = tkinter.Label(self, text="Name:")
            lb.grid(row=0, column=0)
            name = tkinter.Entry(self, bg="white")
            name.insert("end", model.active_element.name)
            name.grid(row=0, column=1)

            lb = tkinter.Label(self, text="Skeleton name:")
            lb.grid(row=1, column=0)
            skeleton = tkinter.Entry(self, bg="white")
            skeleton.insert("end", model.active_element.skeleton_name or "None")
            skeleton.grid(row=1, column=1)

            last_row = 2

            def save_command():
                self.__command_list.add_command(command.PatchCommand({
                    "name": name.get(),
                    "skeleton": model.get_skeleton(skeleton.get()),
                }))

        save = tkinter.Button(self, text="Save", command=save_command)
        save.grid(row=last_row, column=0)

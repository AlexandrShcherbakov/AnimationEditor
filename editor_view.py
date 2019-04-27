import tkinter

import command
from model import Skeleton, SegmentBone, CircleBone, Animation, SkeletonState


class ResourceEditorViewer(tkinter.Canvas):
    def __init__(self, parent, command_list):
        tkinter.Canvas.__init__(self)
        self.__command_list = command_list
        scrollbar = tkinter.Scrollbar(parent, orient="vertical", command=self.yview)
        scrollbar.grid(row=0, column=2)
        self.configure(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.yview)
        self.xview_moveto(0)
        self.yview_moveto(0)
        self.interior = interior = tkinter.Frame(self)
        interior_id = self.create_window(0, 0, window=interior, anchor=tkinter.NW)

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

        if isinstance(model.active_element, SkeletonState):
            def bone_name(name, minuses=20):
                return "-" * ((minuses - len(name)) // 2) + name + "-" * ((minuses - len(name) + 1) // 2)

            last_row = 0

            positions = dict()
            thickness = dict()
            colors = dict()
            radiuses = dict()
            lengthes = dict()
            rotates = dict()

            if model.active_element.skeleton_name:
                skeleton = model.active_element.get_skeleton() or model.get_skeleton(model.active_element.skeleton_name)
                for i in range(skeleton.number_of_bones):
                    if i == 2:
                        break
                    bone = skeleton.get_bone(i)
                    lb = tkinter.Label(self, text=bone_name(bone.name), justify="center")
                    lb.grid(row=last_row, column=0)
                    last_row += 1
                    lb = tkinter.Label(self, text="Position:")
                    lb.grid(row=last_row, column=0)
                    positions[i] = [tkinter.Entry(self, bg="white"), tkinter.Entry(self, bg="white")]
                    for j in range(len(positions[i])):
                        positions[i][j].insert("end", bone.to_dict()["position"][j])
                        positions[i][j].grid(row=last_row, column=j + 1)
                    last_row += 1

                    lb = tkinter.Label(self, text="Thickness:")
                    lb.grid(row=last_row, column=0)
                    thickness[i] = tkinter.Entry(self, bg="white")
                    thickness[i].insert("end", bone.to_dict()["thickness"])
                    thickness[i].grid(row=last_row, column=1)
                    last_row += 1

                    lb = tkinter.Label(self, text="Color:")
                    lb.grid(row=last_row, column=0)
                    colors[i] = [
                        tkinter.Entry(self, bg="white"),
                        tkinter.Entry(self, bg="white"),
                        tkinter.Entry(self, bg="white"),
                    ]
                    for j in range(len(colors[i])):
                        colors[i][j].insert("end", bone.to_dict()["color"][j])
                        colors[i][j].grid(row=last_row, column=j + 1)
                    last_row += 1

                    if isinstance(bone, CircleBone):
                        lb = tkinter.Label(self, text="Radius:")
                        lb.grid(row=last_row, column=0)
                        radiuses[i] = tkinter.Entry(self, bg="white")
                        radiuses[i].insert("end", bone.to_dict()["radius"])
                        radiuses[i].grid(row=last_row, column=1)
                        last_row += 1
                    elif isinstance(bone, SegmentBone):
                        lb = tkinter.Label(self, text="Length:")
                        lb.grid(row=last_row, column=0)
                        lengthes[i] = tkinter.Entry(self, bg="white")
                        lengthes[i].insert("end", bone.to_dict()["length"])
                        lengthes[i].grid(row=last_row, column=1)
                        last_row += 1

                        lb = tkinter.Label(self, text="Rotation:")
                        lb.grid(row=last_row, column=0)
                        rotates[i] = tkinter.Entry(self, bg="white")
                        rotates[i].insert("end", bone.to_dict()["rotation"])
                        rotates[i].grid(row=last_row, column=1)
                        last_row += 1

            def save_command():
                patch = [dict() for i in range(skeleton.number_of_bones)]

                for bone_name, p in positions.items():
                    patch[bone_name]["position"] = (int(p[0].get()), int(p[1].get()))
                for bone_name, t in thickness.items():
                    patch[bone_name]["thickness"] = float(t.get())
                for bone_name, c in colors.items():
                    patch[bone_name]["color"] = (int(c[0].get()), int(c[1].get()), int(c[2].get()))
                for bone_name, r in radiuses.items():
                    patch[bone_name]["radius"] = float(r.get())
                for bone_name, l in lengthes.items():
                    patch[bone_name]["length"] = float(l.get())
                for bone_name, r in rotates.items():
                    patch[bone_name]["rotation"] = float(r.get())

                self.__command_list.add_command(command.PatchCommand(patch))

        save = tkinter.Button(self, text="Save", command=save_command)
        save.grid(row=last_row, column=0)

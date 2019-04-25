import tkinter.ttk

import command


class ProjectHierarchyView(tkinter.ttk.Treeview):
    def __init__(self, command_list):
        tkinter.ttk.Treeview.__init__(self)
        self.__command_list = command_list
        self.__items = dict()
        self.bind("<1>", self.select_item)

    def on_model_changed(self, model):
        self.delete(*self.get_children())
        self.__items.clear()
        
        animations = self.insert("", "end", text="Animations", open=True)
        skeletons = self.insert("", "end", text="Skeletons", open=True)

        for i in range(model.number_of_animations):
            animation = self.insert(animations, "end", iid=model.get_animation(i).name,
                text=model.get_animation(i).name, open=True)
            self.__items[animation] = model.get_animation(i)

        for i in range(model.number_of_skeletons):
            skeleton = self.insert(skeletons, "end", iid=model.get_skeleton(i).name,
                text=model.get_skeleton(i).name, open=True)
            self.__items[skeleton] = model.get_skeleton(i)

    def select_item(self, event):
        iid = self.identify("item", event.x, event.y)
        if iid in self.__items:
            self.__command_list.add_command(command.SelectCommand(self.__items[iid]))


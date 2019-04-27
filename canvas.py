import math
import tkinter

from model import Skeleton, SegmentBone, CircleBone, Bone, SkeletonState, Animation


class ResourceViewer(tkinter.Canvas):
    def __init__(self, command_list):
        tkinter.Canvas.__init__(self, background="white")
        self.__command_list = command_list
        self.__animation = None
        self.current_state = 0

    def __draw_bone(self, bone):
        if isinstance(bone, SegmentBone):
            params = bone.to_dict()
            end_x = params["position"][0] + params["length"] * math.cos(params["rotation"])
            end_y = params["position"][1] + params["length"] * math.sin(params["rotation"])
            self.create_line(
                (params["position"][0], params["position"][1], end_x, end_y),
                fill="#{:02x}{:02x}{:02x}".format(*params["color"]),
                width=params["thickness"]
            )
        if isinstance(bone, CircleBone):
            params = bone.to_dict()
            left = params["position"][0] - params["radius"]
            right = params["position"][0] + params["radius"]
            top = params["position"][1] - params["radius"]
            bottom = params["position"][1] + params["radius"]
            self.create_oval(
                (left, top, right, bottom),
                outline="#{:02x}{:02x}{:02x}".format(*params["color"]),
                width=params["thickness"]
            )

    def __draw_skeleton(self, skeleton):
        for i in range(skeleton.number_of_bones):
            self.__draw_bone(skeleton.get_bone(i))

    def __draw_skeleton(self, skeleton):
        for i in range(skeleton.number_of_bones):
            self.__draw_bone(skeleton.get_bone(i))

    def on_model_changed(self, model):
        self.delete("all")
        self.__animation = None
        if isinstance(model.active_element, Skeleton):
            self.__draw_skeleton(model.active_element)
        elif isinstance(model.active_element, Bone):
            self.__draw_bone(model.active_element)
        elif isinstance(model.active_element, SkeletonState):
            self.__draw_skeleton(model.active_element.get_skeleton())
        elif isinstance(model.active_element, Animation):
            self.__animation = model.active_element
            self.current_state = 0
            self.update_clock()


    def update_clock(self):
        if self.__animation and self.__animation.number_of_states:
            self.delete("all")
            self.__draw_skeleton(self.__animation.get_state(self.current_state).get_skeleton())
            self.current_state = (self.current_state + 1) % self.__animation.number_of_states
            self.after(1000, self.update_clock)

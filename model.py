"""
This is the Model's file in our MVC framework.
It contains data structure and data managing.
"""


import json
import os

from abc import ABC, abstractmethod
from time import time


class Project:
    """
    Main class of the project.
    Project is a static class
    Contains settings and lists of entities
    (skeletons and animations).
    """
    default_bone_color = (0, 0, 0)
    default_bone_thickness = 1.0
    default_transition_time = 1.0

    animations_dir = 'animations'
    skeletons_dir = 'skeletons'

    skeletons = list()
    animations = list()

    def __init__(self):
        self.active_element = self

    @staticmethod
    def has_skeleton(name):
        return any(name == skeleton.name for skeleton in Project.skeletons)

    @staticmethod
    def has_animation(name):
        return any(name == animation.name for animation in Project.animations)

    @property
    def number_of_skeletons(self):
        return len(self.skeletons)

    @staticmethod
    def load():
        for filename in os.listdir(Project.skeletons_dir):
            if filename.endswith('.json'):
                skeleton = Skeleton(name=filename[:-5])
                skeleton.load()

        for filename in os.listdir(Project.animations_dir):
            if filename.endswith('.json'):
                animation = Animation(name=filename[:-5])
                animation.load()

    def add_skeleton(self, skeleton):
        self.skeletons.append(skeleton)

    def remove_skeleton(self, skeleton_id: int):
        self.skeletons.pop(skeleton_id)


class Bone(ABC):
    """
    Abstract bone class.
    Any new bone class in the project should be inherited from this class
    and implement update() and to_dict() methods.
    Position is the coordinates of the bone - (float, float) tuple.
    What is position of the bone depends on the type of the bone.
    Bone can change color and thickness.
    """
    def __init__(self, position: tuple, color: tuple, thickness: float):
        self.__position = position
        self.__color = color
        self.__thickness = thickness

    @abstractmethod
    def update(self, **kwargs):
        for attr in kwargs:
            if attr == 'position':
                self.__position = kwargs[attr]
            elif attr == 'color':
                self.__color = kwargs[attr]
            elif attr == 'thickness':
                self.__thickness = kwargs[attr]

    @abstractmethod
    def to_dict(self):
        return dict(
            position=self.__position,
            color=self.__color,
            thickness=self.__thickness,
        )


class SegmentBone(Bone):
    """
    Bone with shape of a segment.
    Position is the coordinates of one of the ends of the segment.
    Length is segment's length.
    Rotation is the angle between the segment and the horizontal line (OX).
    """
    def __init__(self, length: float, rotation: float, position: tuple,
                 color=Project.default_bone_color, thickness=Project.default_bone_thickness):
        self.__length = length
        self.__rotation = rotation
        super().__init__(position, color, thickness)

    def update(self, **kwargs):
        for attr in kwargs:
            if attr == 'length':
                self.__length = kwargs[attr]
            elif attr == 'rotation':
                self.__rotation = kwargs[attr]
        super().update(**kwargs)

    def to_dict(self):
        res = super().to_dict()
        res['length'] = self.__length
        res['rotation'] = self.__rotation
        return res


class CircleBone(Bone):
    """
    Bone with the shape of a circle.
    Position is the coordinates of the center of the circle.
    Radius is the radius of the circle.
    """
    def __init__(self, radius: float, position: tuple,
                 color=Project.default_bone_color, thickness=Project.default_bone_thickness):
        self.__radius = radius
        super().__init__(position, color, thickness)

    def update(self, **kwargs):
        for attr in kwargs:
            if attr == 'length':
                self.__radius = kwargs[attr]
        super().update(**kwargs)

    def to_dict(self):
        res = super().to_dict()
        res['radius'] = self.__radius
        return res


class Skeleton:
    """
    Skeleton is a named set of bones.
    If name is not provided, creates name with format "skeleton_{timestamp}"
    Can be saved to the hard drive and loaded from there.
    Supports following operations:
        - add a bone
        - remove a bone
        - update existing bone
        - transform into a dictionary
        - save to the hard drive
        - load from the hard drive
    """
    def __init__(self, name=None):
        self.__name = name if name else f'skeleton_{str(int(time()))}'
        try:
            self.load()
        except FileNotFoundError:
            self.__bones = list()
        if not Project.has_skeleton(self.__name):
            Project.skeletons.append(self)

    @property
    def number_of_bones(self):
        return len(self.__bones)

    @property
    def name(self):
        return self.__name

    def add_bone(self, bone: Bone):
        self.__bones.append(bone)

    def remove_bone(self, bone_id: int):
        self.__bones.pop(bone_id)

    def update_bone(self, bone_id: int, **kwargs):
        if bone_id < self.number_of_bones:
            self.__bones[bone_id].update(**kwargs)
        else:
            raise IndexError(f'Skeleton does not have a bone with index {bone_id}. It has only {self.number_of_bones} bones.')

    def to_dict(self):
        return dict(
            name=self.__name,
            bones=[bone.to_dict() for bone in self.__bones],
        )

    def save(self):
        if not self.__bones:
            raise ValueError('Skeleton has no bones to save.')
        with open(f'{Project.skeletons_dir}/{self.__name}.json', 'w') as file:
            json.dump(self.to_dict(), file)

    def load(self):
        try:
            with open(f'{Project.skeletons_dir}/{self.__name}.json', 'r') as file:
                data = json.load(file)
                self.__bones = data['bones']
        except FileNotFoundError:
            raise FileNotFoundError(f'File for skeleton "{self.__name}" was not found.')


class SkeletonState:
    """
    Update for a skeleton.
    Updates is a list of update for each bone of the skeleton.
    Update for the bone is a dictionary with parameters to change as keys and parameter's new values as values.
    """
    def __init__(self, skeleton: Skeleton, updates=None):
        self.__updates = updates
        self.__skeleton = skeleton

    @property
    def skeleton_name(self):
        return self.__skeleton.name

    def apply(self):
        for i in range(len(self.__updates)):
            self.__skeleton.update_bone(i, **self.__updates[i])


class Animation:
    """
    Animation of the skeleton.
    If name is not provided, creates name with format "animation_{timestamp}"
    Consists of skeleton's states and transition timings between them.
    Addition of the new move (SkeletonState) creates transition time before that move.
    Removing of the state removes transition time before the state.
    Can be saved to the hard drive and loaded from there.
    Can be exported to GIF.
    """
    def __init__(self, skeleton: Skeleton, name=None):
        self.__name = name if name else f'animation_{str(int(time()))}'
        self.__skeleton = skeleton
        try:
            self.load()
        except FileNotFoundError:
            self.__states, self.__transitions = list(), list()
        if not Project.has_animation(self.__name):
            Project.animations.append(self)

    @property
    def name(self):
        return self.__name

    @property
    def skeleton_name(self):
        return self.__skeleton.name

    def check_state(self, state: SkeletonState):
        if state.skeleton_name != self.skeleton_name:
            raise ValueError(f'Can not add a state for a different skeleton to the animation')

    def add_state(self, state: SkeletonState, transition_time=Project.default_transition_time):
        self.check_state(state)
        if not self.__states:
            self.__states.append(state)
        else:
            self.__states.append(state)
            self.__transitions.append(transition_time)

    def update_state(self, state_id: int, state: SkeletonState):
        self.check_state(state)
        if state_id < len(self.__states):
            self.__states.pop(state_id)
            self.__states.insert(state_id, state)
        else:
            raise IndexError(f'Animation does not have a state with index {state_id}.')

    def remove_state(self, state_id: int):
        if state_id < len(self.__states):
            self.__states.pop(state_id)
            if state_id == 0:
                self.__transitions.pop(0)
            else:
                self.__transitions.pop(state_id - 1)
        else:
            raise IndexError(f'Animation does not have a state with index {state_id}.')

    def change_transition_time(self, state_id: int, transition_time=Project.default_transition_time):
        if state_id < len(self.__states) and state_id != 0:
            self.__transitions.pop(state_id - 1)
            self.__transitions.insert(state_id - 1, transition_time)
        else:
            raise IndexError(f'Animation does not have a state with index {state_id}.')

    def to_dict(self):
        return dict(
            name=self.__name,
            skeleton_name=self.skeleton_name,
            states=self.__states,
            transitions=self.__transitions,
        )

    def save(self):
        if not self.__states:
            raise ValueError('Animation has nothing to save.')
        with open(f'{Project.animations_dir}/{self.__name}.json', 'w') as file:
            json.dump(self.to_dict(), file)

    def load(self):
        try:
            with open(f'{Project.animations_dir}/{self.__name}.json', 'r') as file:
                data = json.load(file)
                self.__states = data['states']
                self.__transitions = data['transitions']
        except FileNotFoundError:
            raise FileNotFoundError(f'File for animation "{self.__name}" was not found.')

    def export_to_gif(self):
        pass

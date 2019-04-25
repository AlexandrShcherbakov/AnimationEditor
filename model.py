"""
This is the Model's file in our MVC framework.
It contains data structure and data managing.
"""

import json
import os
import shutil
from abc import ABC, abstractmethod
from time import time

from settings import ProjectSettings


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
                 color=ProjectSettings.default_bone_color, thickness=ProjectSettings.default_bone_thickness):
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
        res['type'] = 'SEGMENT'
        return res


class CircleBone(Bone):
    """
    Bone with the shape of a circle.
    Position is the coordinates of the center of the circle.
    Radius is the radius of the circle.
    """
    def __init__(self, radius: float, position: tuple,
                 color=ProjectSettings.default_bone_color, thickness=ProjectSettings.default_bone_thickness):
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
        res['type'] = 'CIRCLE'
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
        self.__bones = list()

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

    def get_bone(self, idx):
        return self.__bones[idx]

    def to_dict(self):
        return dict(
            name=self.__name,
            bones=[bone.to_dict() for bone in self.__bones],
        )

    def save(self, path_to_project_dir):
        if not self.__bones:
            raise ValueError('Skeleton has no bones to save.')
        with open(os.path.join(path_to_project_dir, ProjectSettings.skeletons_dir, self.name), 'w') as file:
            json.dump(self.to_dict(), file, indent=2)

    def load(self, path_to_project_dir):
        try:
            with open(os.path.join(path_to_project_dir, ProjectSettings.skeletons_dir, self.name), 'r') as file:
                data = json.load(file)
                self.__name = data['name']
                for bone in data['bones']:
                    if bone['type'] == 'SEGMENT':
                        self.__bones.append(SegmentBone(
                            bone['length'],
                            bone['rotation'],
                            bone['position'],
                            bone['color'],
                            bone['thickness'],
                        ))
                    elif bone['type'] == 'CIRCLE':
                        self.__bones.append(CircleBone(
                            bone['radius'],
                            bone['position'],
                            bone['color'],
                            bone['thickness'],
                        ))

        except FileNotFoundError:
            raise FileNotFoundError(f'File for skeleton "{self.__name}" was not found.')

    def process_patch(self, opts):
        old_values = dict()
        if "name" in opts:
            old_values["name"] = self.__name
            self.__name = opts["name"]
        return old_values


class SkeletonState:
    """
    Update for a skeleton.
    Updates is a list of update for each bone of the skeleton.
    Update for the bone is a dictionary with parameters to change as keys and parameter's new values as values.
    """
    def __init__(self, skeleton=None, updates=None):
        self.__updates = updates if updates else list()
        self.__skeleton = skeleton

    @property
    def skeleton_name(self):
        return self.__skeleton.name if self.__skeleton else None

    def set_skeleton(self, skeleton: Skeleton):
        self.__skeleton = skeleton

    def apply(self):
        for i in range(len(self.__updates)):
            self.__skeleton.update_bone(i, **self.__updates[i])

    def to_dict(self):
        return dict(
            skeleton_name=self.skeleton_name,
            bone_updates=self.__updates,
        )


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
    def __init__(self, skeleton=None, name=None):
        self.__name = name if name else f'animation_{str(int(time()))}'
        self.__skeleton = skeleton
        self.__states, self.__transitions = list(), list()

    @property
    def name(self):
        return self.__name

    @property
    def skeleton_name(self):
        return self.__skeleton.name if self.__skeleton else None

    @property
    def number_of_states(self):
        return len(self.__states)

    def set_skeleton(self, skeleton: Skeleton):
        self.__skeleton = skeleton
        for state in self.__states:
            state.set_skeleton(skeleton)

    def check_state(self, state: SkeletonState):
        if not self.__skeleton:
            raise ValueError(f'There is no skeleton matched for this animation.')
        elif state.skeleton_name != self.skeleton_name:
            raise ValueError(f'Can not add a state for a different skeleton to the animation')

    def add_state(self, state: SkeletonState, transition_time=ProjectSettings.default_transition_time):
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

    def get_state(self, idx):
        return self.__states[idx]

    def change_transition_time(self, state_id: int, transition_time=ProjectSettings.default_transition_time):
        if state_id < len(self.__states) and state_id != 0:
            self.__transitions.pop(state_id - 1)
            self.__transitions.insert(state_id - 1, transition_time)
        else:
            raise IndexError(f'Animation does not have a state with index {state_id}.')

    def to_dict(self):
        return dict(
            name=self.__name,
            skeleton_name=self.skeleton_name,
            states=[state.to_dict() for state in self.__states],
            transitions=self.__transitions,
        )

    def save(self, path_to_project_dir):
        if not self.__states:
            raise ValueError('Animation has nothing to save.')
        with open(os.path.join(path_to_project_dir, ProjectSettings.animations_dir, self.name), 'w') as file:
            json.dump(self.to_dict(), file, indent=2)

    def load(self, path_to_project_dir):
        try:
            with open(os.path.join(path_to_project_dir, ProjectSettings.animations_dir, self.name), 'r') as file:
                data = json.load(file)
                self.__states = [SkeletonState(updates=state['bone_updates']) for state in data['states']]
                self.__transitions = data['transitions']
                return data['skeleton_name']
        except FileNotFoundError:
            raise FileNotFoundError(f'File for animation "{self.__name}" was not found.')

    def export_to_gif(self):
        pass


class Project:
    """
    Main class of the project.
    Contains lists of entities (skeletons and animations).
    """

    def __init__(self):
        self.active_element = self

        self.__skeletons = list()
        self.__animations = list()
        self.__views = list()

    def has_skeleton(self, name: str):
        return any(name == skeleton.name for skeleton in self.__skeletons)

    def has_animation(self, name: str):
        return any(name == animation.name for animation in self.__animations)

    def get_skeleton(self, name: str):
        if isinstance(name, int):
            return self.__skeletons[name]
        return list(filter(lambda s: s.name == name, self.__skeletons))[0] if self.has_skeleton(name) else None

    def get_animation(self, name: str):
        if isinstance(name, int):
            return self.__animations[name]
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

    def load(self, path_to_project_dir):
        for filename in os.listdir(os.path.join(path_to_project_dir, ProjectSettings.skeletons_dir)):
            skeleton = Skeleton(name=filename)
            skeleton.load(path_to_project_dir)
            self.add_skeleton(skeleton)

        for filename in os.listdir(os.path.join(path_to_project_dir, ProjectSettings.animations_dir)):
            animation = Animation(name=filename)
            skeleton_name = animation.load(path_to_project_dir)
            animation.set_skeleton(self.get_skeleton(skeleton_name))
            self.add_animation(animation)

        self.update_views()

    def save(self, path_to_project_dir):
        directories_to_create = [
            path_to_project_dir,
            os.path.join(path_to_project_dir, ProjectSettings.skeletons_dir),
            os.path.join(path_to_project_dir, ProjectSettings.animations_dir),
        ]
        for directory in directories_to_create:
            try:
                os.mkdir(directory)
            except FileExistsError:
                shutil.rmtree(directory)
                os.mkdir(directory)

        for skeleton in self.__skeletons:
            skeleton.save(path_to_project_dir)

        for animation in self.__animations:
            animation.save(path_to_project_dir)

    def update_views(self):
        for view in self.__views:
            view.on_model_changed(self)

    def register_view(self, view):
        self.__views.append(view)
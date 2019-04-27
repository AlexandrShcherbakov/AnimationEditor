"""
This is the Model's file in our MVC framework.
It contains data structure and data managing.
"""

import json
import os
import shutil
from abc import ABC, abstractmethod
from time import time

import fixtures
from settings import ProjectSettings


class Bone(ABC):
    """
    Abstract bone class.
    Any new bone class in the project should be inherited from this class
    and implement process_patch() and to_dict() methods.
    Position is the coordinates of the bone - (float, float) tuple.
    What is position of the bone depends on the type of the bone.
    Bone also can change color and thickness.

    >>> Bone((0, 0), (0, 0, 0), 10, 'Head')
    Traceback (most recent call last):
    ...
    TypeError: Can't instantiate abstract class Bone with abstract methods process_patch, to_dict
    >>> bone = SegmentBone(10, 1, (0, 0), name='Leg')
    """
    def __init__(self, position: tuple, color: tuple, thickness: float, name=None):
        """
        :param position: position of the bone
        :param color: color of the bone as tuple of 3 (x, y, z)
        :param thickness: thickness of the bone
        :param name: name of the bone
        >>> bone = SegmentBone(10, 1, (0, 0), name='Leg')
        >>> Bone.__init__(bone, (1, 1), (1, 1, 1), 228, 'Hand')
        >>> Bone.to_dict(bone)
        {'position': (1, 1), 'color': (1, 1, 1), 'thickness': 228, 'name': 'Hand'}
        """
        self.__position = position
        self.__color = color
        self.__thickness = thickness
        self.__name = name

    @property
    def name(self):
        """
        :return: name of the bone if there is one
        >>> bone = SegmentBone(10, 1, (0, 0), name='Leg')
        >>> bone.name
        'Leg'
        """
        return self.__name

    @abstractmethod
    def process_patch(self, opts):
        """
        Method to proceed update on the bone.
        :param opts: Dictionary with update on the bone.
        The keys are attributes that should be changed and values are new values of these attributes.
        :return: old values as dictionary
        >>> bone = SegmentBone(10, 1, (0, 0), name='Leg')
        >>> Bone.process_patch(bone, dict(name='Hand', thickness=10))  # updating only attributes from class "Bone"
        {'name': 'Leg', 'thickness': 1.0}
        >>> Bone.to_dict(bone)
        {'position': (0, 0), 'color': (0, 0, 0), 'thickness': 10, 'name': 'Hand'}
        """
        old_values = dict()
        for key in ['name', 'position', 'thickness', 'color']:
            if key in opts:
                old_values[key] = getattr(self, '_Bone__{}'.format(key))
                setattr(self, '_Bone__{}'.format(key), opts[key])
        return old_values

    @abstractmethod
    def to_dict(self):
        """
        :return: Dictionary with parameters of the bone.
        >>> bone = SegmentBone(10, 1, (0, 0), name='Leg')
        >>> Bone.to_dict(bone)
        {'position': (0, 0), 'color': (0, 0, 0), 'thickness': 1.0, 'name': 'Leg'}
        """
        res = dict(
            position=self.__position,
            color=self.__color,
            thickness=self.__thickness,
        )
        if self.__name:
            res['name'] = self.__name
        return res


class SegmentBone(Bone):
    """
    Bone with shape of a segment.
    Position is the coordinates of one of the ends of the segment.
    Length is segment's length.
    Rotation is the angle between the segment and the horizontal line (OX).
    >>> bone = SegmentBone(10, 1, (0, 0), name='Leg')
    >>> assert bone.to_dict() == fixtures.segment_bone_fixture
    """
    def __init__(self, length: float, rotation: float, position: tuple,
                 color=ProjectSettings.default_bone_color, thickness=ProjectSettings.default_bone_thickness, name=None):
        """
        :param length: length of the segment
        :param rotation: the angle between the segment and the horizontal line (OX).
        :param position: tuple of two (x, y) - coordinates of left end of the segment
        :param color: tuple of three (x, y, z) - color of the bone
        :param thickness: thickness of the bone
        :param name: name of the bone
        >>> bone = SegmentBone(10, 1, (0, 0), name='Leg')
        >>> assert bone.to_dict() == fixtures.segment_bone_fixture

        """
        self.__length = length
        self.__rotation = rotation
        super().__init__(position, color, thickness, name)

    def to_dict(self):
        """
        :return: dictionary with attributes of the bone.
        >>> bone = SegmentBone(10, 1, (0, 0), name='Leg')
        >>> assert bone.to_dict() == fixtures.segment_bone_fixture
        """
        res = super().to_dict()
        res['length'] = self.__length
        res['rotation'] = self.__rotation
        res['type'] = 'SEGMENT'
        return res

    def process_patch(self, opts):
        """
        Method to proceed update on the bone.
        :param opts: Dictionary with update on the bone.
        The keys are attributes that should be changed and values are new values of these attributes.
        :return: old values as dictionary
        >>> bone = SegmentBone(10, 1, (0, 0), name='Leg')
        >>> bone.process_patch(dict(name='Hand', length=120))
        {'name': 'Leg', 'length': 10}
        >>> assert bone.to_dict() == fixtures.segment_bone_process_patch_fixture
        """
        old_values = super().process_patch(opts)
        if "length" in opts:
            old_values["length"] = self.__length
            self.__length = opts["length"]
        if "rotation" in opts:
            old_values["rotation"] = self.__rotation
            self.__rotation = opts["rotation"]
        return old_values


class CircleBone(Bone):
    """
    Bone with the shape of a circle.
    Position is the coordinates of the center of the circle.
    Radius is the radius of the circle.
    >>> bone = CircleBone(10, (0, 0), name='Leg')
    >>> bone.to_dict()
    {'position': (0, 0), 'color': (0, 0, 0), 'thickness': 1.0, 'name': 'Leg', 'radius': 10, 'type': 'CIRCLE'}

    """
    def __init__(self, radius: float, position: tuple,
                 color=ProjectSettings.default_bone_color, thickness=ProjectSettings.default_bone_thickness, name=None):
        """
        :param radius: radius of the circle
        :param position: tuple of two (x, y) - coordinates of the center of the circle.
        :param color: tuple of three (x, y, z) - color of the bone
        :param thickness: thickness of the bone
        :param name: name of he bone
        >>> bone = CircleBone(10, (0, 0), name='Leg')
        >>> bone.to_dict()
        {'position': (0, 0), 'color': (0, 0, 0), 'thickness': 1.0, 'name': 'Leg', 'radius': 10, 'type': 'CIRCLE'}
        """
        self.__radius = radius
        super().__init__(position, color, thickness, name)

    def to_dict(self):
        """
        :return: dictionary with attributes of the bone.
        >>> bone = CircleBone(10, (0, 0), name='Leg')
        >>> bone.to_dict()
        {'position': (0, 0), 'color': (0, 0, 0), 'thickness': 1.0, 'name': 'Leg', 'radius': 10, 'type': 'CIRCLE'}
        """
        res = super().to_dict()
        res['radius'] = self.__radius
        res['type'] = 'CIRCLE'
        return res

    def process_patch(self, opts):
        """
        Method to proceed update on the bone.
        :param opts: Dictionary with update on the bone.
        The keys are attributes that should be changed and values are new values of these attributes.
        :return: old values as dictionary
        >>> bone = CircleBone(10, (0, 0), name='Leg')
        >>> bone.process_patch(dict(name='Hand', radius=120))
        {'name': 'Leg', 'radius': 10}
        >>> bone.to_dict()
        {'position': (0, 0), 'color': (0, 0, 0), 'thickness': 1.0, 'name': 'Hand', 'radius': 120, 'type': 'CIRCLE'}
        """
        old_values = super().process_patch(opts)
        if "radius" in opts:
            old_values["radius"] = self.__radius
            self.__radius = opts["radius"]
        return old_values


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
    >>> skeleton = Skeleton(name='Vasiliy')
    >>> skeleton.to_dict()
    {'name': 'Vasiliy', 'bones': []}
    """
    def __init__(self, name=None):
        """
        :param name: name of the skeleton
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> skeleton.to_dict()
        {'name': 'Vasiliy', 'bones': []}
        """
        self.__name = name if name else 'skeleton_{}'.format(str(int(time())))
        self.__bones = list()

    @property
    def number_of_bones(self):
        """
        :return: number of bones of the skeleton
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> skeleton.number_of_bones
        0
        >>> bone = CircleBone(10, (0, 0), name='Leg')
        >>> skeleton.add_bone(bone)
        >>> skeleton.number_of_bones
        1
        """
        return len(self.__bones)

    @property
    def name(self):
        """
        :return: name of the bone
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> skeleton.name
        'Vasiliy'
        """
        return self.__name

    def add_bone(self, bone: Bone):
        """
        :param bone: bone that should be added
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> bone = CircleBone(10, (0, 0), name='Leg')
        >>> skeleton.add_bone(bone)
        >>> bone = SegmentBone(10, 1, (1, 1))
        >>> skeleton.add_bone(bone)
        >>> skeleton.number_of_bones
        2
        """
        if not bone.name:
            bone.process_patch(dict(name='{}_bone_{}'.format(self.name, self.number_of_bones)))
        self.__bones.append(bone)

    def remove_bone(self, idx: int):
        """
        :param idx: index of the bone that should be removed
        :return: raises and exception if idx >= number of bones
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> bone = CircleBone(10, (0, 0), name='Leg')
        >>> skeleton.add_bone(bone)
        >>> bone = SegmentBone(10, 1, (1, 1))
        >>> skeleton.add_bone(bone)
        >>> skeleton.number_of_bones
        2
        >>> skeleton.remove_bone(12)
        Traceback (most recent call last):
        ...
        IndexError: Skeleton does not have a bone with index 12. It has only 2 bones.
        >>> skeleton.remove_bone(1)
        >>> skeleton.number_of_bones
        1
        >>> skeleton.remove_bone(0)
        >>> skeleton.number_of_bones
        0
        """
        if idx < self.number_of_bones:
            self.__bones.pop(idx)
        else:
            raise IndexError(
                'Skeleton does not have a bone with index {}. It has only {} bones.'.format(idx, self.number_of_bones)
            )

    def update_bone(self, idx: int, updates: dict):
        """
        :param idx:
        :param updates:
        :return: raises and exception if idx >= number of bones
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> bone = CircleBone(10, (0, 0), name='Head')
        >>> skeleton.add_bone(bone)
        >>> bone = SegmentBone(10, 1, (1, 1))
        >>> skeleton.add_bone(bone)
        >>> skeleton.update_bone(12, dict(name='Head'))
        Traceback (most recent call last):
        ...
        IndexError: Skeleton does not have a bone with index 12. It has only 2 bones.
        >>> skeleton.update_bone(1, dict(name='Leg'))
        >>> assert skeleton.to_dict() == fixtures.skeleton_update_bone_fixture
        """
        if idx < self.number_of_bones:
            self.__bones[idx].process_patch(updates)
        else:
            raise IndexError(
                'Skeleton does not have a bone with index {}. It has only {} bones.'.format(idx, self.number_of_bones)
            )

    def get_bone(self, idx):
        """
        :param idx: index of the bone
        :return: bone if there is one, else raises an exception
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> bone = CircleBone(10, (0, 0), name='Head')
        >>> skeleton.add_bone(bone)
        >>> bone = SegmentBone(10, 1, (1, 1))
        >>> skeleton.add_bone(bone)
        >>> skeleton.get_bone(12)
        Traceback (most recent call last):
        ...
        IndexError: Skeleton does not have a bone with index 12. It has only 2 bones.
        >>> skeleton.get_bone(0).to_dict()
        {'position': (0, 0), 'color': (0, 0, 0), 'thickness': 1.0, 'name': 'Head', 'radius': 10, 'type': 'CIRCLE'}

        >>> assert skeleton.get_bone(1).to_dict() == fixtures.skeleton_get_bone_fixture

        """
        if idx < self.number_of_bones:
            return self.__bones[idx]
        else:
            raise IndexError(
                'Skeleton does not have a bone with index {}. It has only {} bones.'.format(idx, self.number_of_bones)
            )

    def to_dict(self):
        """
        :return: dictionary with attributes of the skeleton
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> bone = CircleBone(10, (0, 0), name='Head')
        >>> skeleton.add_bone(bone)
        >>> bone = SegmentBone(10, 1, (1, 1))
        >>> skeleton.add_bone(bone)
        >>> assert skeleton.to_dict() == fixtures.skeleton_to_dict_fixture
        """
        return dict(
            name=self.__name,
            bones=[bone.to_dict() for bone in self.__bones],
        )

    def process_patch(self, opts):
        """
        Method to proceed update on the skeleton.
        :param opts: Dictionary with update on the bone.
        The keys are attributes that should be changed and values are new values of these attributes.
        :return: old values as dictionary
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> skeleton.process_patch(dict(name='Ivan'))
        {'name': 'Vasiliy'}

        >>> skeleton.to_dict()
        {'name': 'Ivan', 'bones': []}
        """
        old_values = dict()
        if "name" in opts:
            old_values["name"] = self.__name
            self.__name = opts["name"]
        return old_values

    def load(self, path_to_project_dir):
        """
        Loads a skeleton from the directory of the project if there is a saved skeleton with that name.
        :param path_to_project_dir: path to the directory where project was saved
        :return: raises an exception if there is no file for the skeleton
        >>> skeleton = Skeleton(name="Ivan_Vasil'evich")
        >>> skeleton.load('TestProject')
        >>> assert skeleton.to_dict() == fixtures.skeleton_loaded_fixture

        >>> skeleton = Skeleton(name="Vasiliy")
        >>> skeleton.load('TestProject')
        Traceback (most recent call last):
        ...
        FileNotFoundError: File for skeleton "Vasiliy" was not found.
        """
        try:
            with open(os.path.join(path_to_project_dir, ProjectSettings.skeletons_dir, self.name), 'r') as file:
                data = json.load(file)
                self.__name = data['name']
                self.__bones = list()
                for bone in data['bones']:
                    if bone['type'] == 'SEGMENT':
                        self.__bones.append(SegmentBone(
                            bone['length'],
                            bone['rotation'],
                            bone['position'],
                            bone['color'],
                            bone['thickness'],
                            name=bone['name'] if 'name' in bone else '{}_bone_{}'.format(
                                self.name,
                                self.number_of_bones
                            ),
                        ))
                    elif bone['type'] == 'CIRCLE':
                        self.__bones.append(CircleBone(
                            bone['radius'],
                            bone['position'],
                            bone['color'],
                            bone['thickness'],
                            name=bone['name'] if 'name' in bone else '{}_bone_{}'.format(
                                self.name,
                                self.number_of_bones
                            ),
                        ))

        except FileNotFoundError:
            raise FileNotFoundError('File for skeleton "{}" was not found.'.format(self.__name))

    def save(self, path_to_project_dir):
        """
        Saves a skeleton to the file inside "skeletons" directory inside the project directory.
        Name of the file is the name of the skeleton.
        :param path_to_project_dir: path to the directory where project is going to be saved
        >>> skeleton = Skeleton(name="Ivan_Vasil'evich")
        >>> skeleton.load('TestProject')
        >>> skeleton.save('TestProject')
        >>> assert os.path.exists('TestProject/skeletons/{}'.format(skeleton.name))
        >>> skeleton.load('TestProject')
        >>> assert skeleton.to_dict() == fixtures.skeleton_loaded_fixture

        """
        with open(os.path.join(path_to_project_dir, ProjectSettings.skeletons_dir, self.name), 'w') as file:
            json.dump(self.to_dict(), file, indent=2)


class SkeletonState:
    """
    Update for a skeleton.
    Updates is a dict of update for bones of the skeleton. Keys are indexes of the bones.
    Update for the bone is a dictionary with parameters to change as keys and parameter's new values as values.
    >>> SkeletonState().to_dict()
    {'skeleton_name': None, 'bone_updates': {}}
    """
    def __init__(self, skeleton=None, updates=None):
        """
        :param skeleton: skeleton for which updates are for
        :param updates: list of dictionaries with updates, see Skeleton.update_bone()
        >>> SkeletonState().to_dict()
        {'skeleton_name': None, 'bone_updates': {}}
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> skeleton.add_bone(SegmentBone(10, 1, (0, 0), name='Leg'))
        >>> SkeletonState(skeleton).to_dict()
        {'skeleton_name': 'Vasiliy', 'bone_updates': {}}
        >>> SkeletonState(skeleton, {0: dict(length=20)}).to_dict()
        {'skeleton_name': 'Vasiliy', 'bone_updates': {0: {'length': 20}}}
        """
        self.__updates = updates if updates else dict()
        self.__skeleton = skeleton

    @property
    def skeleton_name(self):
        """
        :return: name of the skeleton of the state if there is one
        >>> SkeletonState().skeleton_name
        >>> SkeletonState(Skeleton(name='Vasiliy')).skeleton_name
        'Vasiliy'

        """
        return self.__skeleton.name if self.__skeleton else None

    def set_skeleton(self, skeleton: Skeleton):
        """
        Sets a skeleton for the state
        :param skeleton: skeleton of the state
        :return: None
        >>> state = SkeletonState()
        >>> state.set_skeleton(Skeleton(name='Vasiliy'))
        >>> state.skeleton_name
        'Vasiliy'
        """
        self.__skeleton = skeleton

    def get_skeleton(self):
        """
        :return: skeleton of the state
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> state = SkeletonState(skeleton)
        >>> assert state.get_skeleton() == skeleton
        """
        return self.__skeleton

    def apply(self):
        """
        Applies updates of that state to the skeleton.
        :return: None
        >>> skeleton = Skeleton(name="Ivan_Vasil'evich")
        >>> skeleton.load('TestProject')
        >>> state = SkeletonState(skeleton, updates={9: dict(radius=100)})
        >>> state.apply()
        >>> fixture = fixtures.skeleton_loaded_fixture
        >>> fixture['bones'][9]['radius'] = 100
        >>> assert fixture == state.get_skeleton().to_dict()
        """
        for bone_idx in self.__updates:
            self.__skeleton.update_bone(bone_idx, self.__updates[bone_idx])

    def to_dict(self):
        """
        :return: dictionary with skeleton name and updates
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> skeleton.add_bone(SegmentBone(10, 1, (0, 0), name='Leg'))
        >>> SkeletonState(skeleton, {0: dict(length=20)}).to_dict()
        {'skeleton_name': 'Vasiliy', 'bone_updates': {0: {'length': 20}}}
        """
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

    >>> skeleton = Skeleton(name='Vasiliy')
    >>> animation = Animation(skeleton, 'Dancing')
    """

    def __init__(self, skeleton=None, name=None):
        """
        :param skeleton: skeleton which should execute this animation
        :param name: name of the animation
        If name is not provided, generates it as animation_{timestamp}
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> animation = Animation(skeleton, 'Dancing')
        >>> animation.to_dict()
        {'name': 'Dancing', 'skeleton_name': 'Vasiliy', 'states': [], 'transitions': []}
        """
        self.__name = name if name else 'animation_{}'.format(str(int(time())))
        self.__skeleton = skeleton
        self.__states, self.__transitions = list(), list()

    def process_patch(self, opts):
        old_values = dict()
        if "name" in opts:
            old_values["name"] = self.__name
            self.__name = opts["name"]
        if "skeleton" in opts:
            old_values["skeleton"] = self.__skeleton
            self.__skeleton = opts["skeleton"]
        return old_values

    @property
    def name(self):
        """
        :return: name of the animation
        >>> Animation(name='Dancing').name
        'Dancing'
        """
        return self.__name

    @property
    def skeleton_name(self):
        """
        :return: name of the skeleton
        >>> Animation(skeleton=Skeleton(name='Vasiliy')).skeleton_name
        'Vasiliy'
        """
        return self.__skeleton.name if self.__skeleton else None

    @property
    def number_of_states(self):
        """
        :return: number of states in the animation
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> animation = Animation(skeleton, 'Dancing')
        >>> animation.number_of_states
        0
        >>> animation.add_state(SkeletonState(skeleton, None))
        >>> animation.number_of_states
        1
        """
        return len(self.__states)

    def set_skeleton(self, skeleton: Skeleton):
        """
        :param skeleton: skeleton which is the animation for
        :return: None
        >>> animation = Animation(name='Dancing')
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> animation.set_skeleton(skeleton)
        >>> animation.skeleton_name
        'Vasiliy'
        """
        self.__skeleton = skeleton
        for state in self.__states:
            state.set_skeleton(skeleton)

    def add_state(self, state: SkeletonState, transition_time=ProjectSettings.default_transition_time):
        """
        :param state: state to be added
        :param transition_time: transition time before state if state is not first
        :return: None
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> state_1 = SkeletonState(skeleton)
        >>> state_2 = SkeletonState(skeleton)
        >>> animation = Animation(skeleton, name='Dancing')
        >>> animation.add_state(state_1)
        >>> assert animation.to_dict() == fixtures.animation_with_one_state_fixture
        >>> animation.add_state(state_2)
        >>> assert animation.to_dict() == fixtures.animation_with_two_states_fixture
        """
        if not self.__states:
            self.__states.append(state)
        else:
            self.__states.append(state)
            self.__transitions.append(transition_time)

    def update_state(self, idx: int, state: SkeletonState):
        """
        :param idx: index of the state to be updated
        :param state: new version of the state
        :return: raises IndexError if idx >= number of states

        >>> skeleton = Skeleton(name='Vasiliy')
        >>> state_1 = SkeletonState(skeleton)
        >>> state_2 = SkeletonState(skeleton)
        >>> animation = Animation(skeleton, name='Dancing')
        >>> animation.add_state(state_2)
        >>> animation.update_state(0, state_1)
        >>> assert animation.to_dict() == fixtures.animation_with_one_state_fixture
        """
        if idx < len(self.__states):
            self.__states.pop(idx)
            self.__states.insert(idx, state)
        else:
            raise IndexError('Animation does not have a state with index {}.'.format(idx))

    def remove_state(self, idx: int):
        """
        :param idx: index of the state to be removed
        :return: raises IndexError if idx >= number of states
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> state_1 = SkeletonState(skeleton)
        >>> state_2 = SkeletonState(skeleton)
        >>> animation = Animation(skeleton, name='Dancing')
        >>> animation.add_state(state_1)
        >>> animation.add_state(state_2)
        >>> animation.remove_state(12)
        Traceback (most recent call last):
        ...
        IndexError: Animation does not have a state with index 12.
        >>> animation.remove_state(1)
        >>> animation.number_of_states
        1
        >>> animation.remove_state(0)
        >>> animation.number_of_states
        0
        """
        if idx < len(self.__states):
            self.__states.pop(idx)
            if idx > 0:
                self.__transitions.pop(idx - 1)
        else:
            raise IndexError('Animation does not have a state with index {}.'.format(idx))

    def get_state(self, idx):
        """
        :param idx: index of the state to be returned
        :return: SkeltonState. Raises IndexError if idx >= number of states
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> state_1 = SkeletonState(skeleton)
        >>> state_2 = SkeletonState(skeleton)
        >>> animation = Animation(skeleton, name='Dancing')
        >>> animation.add_state(state_1)
        >>> animation.add_state(state_2)
        >>> animation.get_state(12)
        Traceback (most recent call last):
        ...
        IndexError: Animation does not have a state with index 12.
        >>> assert state_2 == animation.get_state(1)
        """
        if idx < len(self.__states):
            return self.__states[idx]
        else:
            raise IndexError('Animation does not have a state with index {}.'.format(idx))

    def change_transition_time(self, state_id: int, transition_time=ProjectSettings.default_transition_time):
        """
        :param state_id: index of the state which is the end of the transition
        :param transition_time: new time
        :return: raises IndexError if idx >= number of states
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> state_1 = SkeletonState(skeleton)
        >>> state_2 = SkeletonState(skeleton)
        >>> animation = Animation(skeleton, name='Dancing')
        >>> animation.add_state(state_1)
        >>> animation.add_state(state_2)
        >>> animation.change_transition_time(1, 10)
        >>> assert animation.to_dict() == fixtures.animation_with_changed_transition
        """
        if state_id < len(self.__states) and state_id != 0:
            self.__transitions.pop(state_id - 1)
            self.__transitions.insert(state_id - 1, transition_time)
        else:
            raise IndexError('Animation does not have a state with index {}.'.format(state_id))

    def to_dict(self):
        """
        :return: dictionary with attributes of the animation.
        >>> skeleton = Skeleton(name='Vasiliy')
        >>> state_1 = SkeletonState(skeleton)
        >>> state_2 = SkeletonState(skeleton)
        >>> animation = Animation(skeleton, name='Dancing')
        >>> animation.add_state(state_1)
        >>> assert animation.to_dict() == fixtures.animation_with_one_state_fixture
        >>> animation.add_state(state_2)
        >>> assert animation.to_dict() == fixtures.animation_with_two_states_fixture
        """
        return dict(
            name=self.__name,
            skeleton_name=self.skeleton_name,
            states=[state.to_dict() for state in self.__states],
            transitions=self.__transitions,
        )

    def load(self, path_to_project_dir):
        """
        Loads an animation from the directory of the project if there is a saved animation with that name.
        :param path_to_project_dir: path to the directory where project was saved
        :return: name of the skeleton. Raises an exception if there is no file for the animation
        # >>> animation = Animation(name='Dancing')
        # >>> skeleton.load('TestProject')
        # >>> assert animation.to_dict() == ???
        TODO: complete test
        >>> animation = Animation(name="Slamming")
        >>> animation.load('TestProject')
        Traceback (most recent call last):
        ...
        FileNotFoundError: File for animation "Slamming" was not found.
        """
        try:
            with open(os.path.join(path_to_project_dir, ProjectSettings.animations_dir, self.name), 'r') as file:
                data = json.load(file)
                self.__states = [SkeletonState(updates=state['bone_updates']) for state in data['states']]
                self.__transitions = data['transitions']
                return data['skeleton_name']
        except FileNotFoundError:
            raise FileNotFoundError('File for animation "{}" was not found.'.format(self.__name))

    def save(self, path_to_project_dir):
        """
        Saves an animation to the file inside "animations" directory inside the project directory.
        Name of the file is the name of the animation.
        :param path_to_project_dir: path to the directory where project is going to be saved
        TODO: test
        """
        with open(os.path.join(path_to_project_dir, ProjectSettings.animations_dir, self.name), 'w') as file:
            json.dump(self.to_dict(), file, indent=2)


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
            raise NameError('Skeleton with name {} already exists in the project.'.format(skeleton.name))

    def remove_skeleton(self, skeleton_id: int):
        if skeleton_id < self.number_of_skeletons:
            self.__skeletons.pop(skeleton_id)
        else:
            raise IndexError('Project does not have a skeleton with index {}. '
                             'It has only {} skeletons.'.format(skeleton_id, self.number_of_skeletons))

    def add_animation(self, animation: Animation):
        if not self.has_animation(animation.name):
            self.__animations.append(animation)
        else:
            raise NameError('Animation with name {} already exists in the project.'.format(animation.name))

    def remove_animation(self, animation_id: int):
        if animation_id < self.number_of_animations:
            self.__animations.pop(animation_id)
        else:
            raise IndexError('Project does not have an animation with index {}. '
                             'It has only {} animations.'.format(animation_id, self.number_of_animations))

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

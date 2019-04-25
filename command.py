"""
This is a module with command pattern, which supports
animation editing in the project.
"""

class CommandList:
    """This class manages commands queue"""
    def __init__(self, model):
        self.model = model
        self.commands = list()
        self.last_id = -1

    def add_command(self, command):
        """Add command and apply"""
        self.commands.append(command)
        self.redo()

    def undo(self):
        """Revert last command"""
        if self.last_id == -1:
            return
        self.commands[self.last_id].revert()
        self.last_id -= 1
        self.model.update_views()

    def redo(self):
        """Redo next command"""
        if self.last_id + 1 == len(self.commands):
            return
        self.last_id += 1
        self.commands[self.last_id].apply(self.model)
        self.model.update_views()

    def reset(self):
        self.commands = list()
        self.last_id = -1


class PatchCommand:
    """Command which change an element."""
    def __init__(self, opts):
        self.opts = opts
        self.old_value = None
        self.target = None

    def apply(self, model):
        """Apply command to model"""
        self.target = model.active_element
        self.old_value = model.active_element.process_patch(self.opts)

    def revert(self):
        """Revert command"""
        self.target.process_patch(self.old_value)


class AddBoneCommand:
    """This command add bone to the skeleton"""
    def __init__(self, bone):
        self.bone = bone
        self.target = None
        self.added_id = None

    def apply(self, model):
        """Apply command to model"""
        self.target = model.active_element
        self.added_id = model.active_element.number_of_bones
        model.active_element.add_bone(self.bone)

    def revert(self):
        """Revert command"""
        self.target.remove_bone(self.added_id)


class AddSkeletonCommand:
    """This command add a skeleton to the project"""
    def __init__(self, skeleton):
        self.skeleton = skeleton
        self.target = None
        self.added_id = None

    def apply(self, model):
        """Apply command to model"""
        self.target = model.active_element
        self.added_id = model.active_element.number_of_skeletons
        model.active_element.add_skeleton(self.skeleton)

    def revert(self):
        """Revert command"""
        self.target.remove_skeleton(self.added_id)


class SelectCommand:
    """This command select another element"""
    def __init__(self, elem):
        self.elem = elem
        self.previous = None
        self.model = None

    def apply(self, model):
        """Apply command to model"""
        self.previous = model.active_element
        self.model = model
        model.active_element = self.elem

    def revert(self):
        """Revert command"""
        self.model.active_element = self.previous

import datetime
from typing import Set, List
from functools import partial
import uuid

# class TimeSpan:
#     def __init__(self):
#         self.earliest
#         self.latest

class Node:

    def __init__(self, *, parents: List['Node'] = [], children: List['Node'] = []):
        self._parents = set(parents)
        self._children = set(children)
        self._uuid = uuid.uuid4()

    def __hash__(self):
        return self._uuid.int

    def __eq__(self, other):
        return self._uuid == other._uuid

    def addChild(self, child: 'Node'):
        self._children.add(child)
        child._parents.add(self)

    def removeChild(self, child: 'Node'):
        self._children.remove(child)
        child._parents.remove(self)

    def getID(self):
        return self._uuid

    def getRoot(self):
        root=self
        def searchFunc(parent):
            nonlocal root
            if len(parent._parents) is 0:
                root = parent
        self.applyOnParents(searchFunc)
        return root

    def applyOnChildren(self, func, recursive=True):
        for child in self._children:
            func(child)
            if recursive:
                child.applyOnChildren(func)

    def applyOnParents(self, func, recursive=True):
        for parent in self._parents:
            func(parent)
            if recursive:
                parent.applyOnParents(func)

class TimeSpan:

    def __init__(self, earliest=0, latest=0):
        self.earliest = earliest
        self.latest = latest

class Task(Node):

    def __init__(self, name, duration=None, *, start=None, end=None, parents: List['Task'] = [], children: List['Task'] = []):
        super(Task, self).__init__(parents=parents, children=children)
        self.name = name
        self.duration = duration
        self.start = start
        self.end = end


    

    

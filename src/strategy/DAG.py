from typing import Set, List
from functools import partial
import uuid

class _NoFilter:

    def __eq__(self, other):
        if isinstance(_NoFilter, other):
            return True

class Node:

    __registry = set([])

    def _getRegistry(self):
        return Node.__registry

    registry = property(_getRegistry, None)

    def __init__(self, *, parents: List['Node'] = [], children: List['Node'] = []):
        self._parents = set(parents)
        self._children = set(children)
        self._uuid = uuid.uuid4()
        self.registry.add(self)

    def __del__(self):
        self._registry.remove(self)

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

    def isARoot(self):
        return len(self._parents) is 0

    def isALeave(self):
        return len(self._children) is 0

    def getRootNodes(self):
        return [node for node in self.registry if node.isARoot()]

    def getLeaveNodes(self):
        return [node for node in self.registry if node.isALeave()]

    def getRoots(self):
        def searchFunc(parent):
            return parent.isARoot()
        roots = self.applyOnParents(searchFunc, filter=False)
        return [ obj for obj, val in roots.items()]

    def getLeaves(self):
        def searchFunc(child):
            return child.isALeave()
        leaves = self.applyOnChildren(searchFunc, filter=False)
        return [ obj for obj, val in leaves.items()]

    def applyOnChildren(self, func, *, recursive=True, filter=_NoFilter()):
        results = {}
        for child in self._children:
            results.update({child: func(child)})
            if recursive:
                results.update(child.applyOnChildren(func))
        if filter is not _NoFilter():
            results = {k:v for k,v in results.items() if v is not filter}
        return results

    def applyOnParents(self, func, *, recursive=True, filter=_NoFilter()):
        results = {}
        for parent in self._parents:
            results.update({parent: func(parent)})
            if recursive:
                results.update(parent.applyOnParents(func))
        if filter is not _NoFilter():
            results = {k:v for k,v in results.items() if v is not filter}
        return results

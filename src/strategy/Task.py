from datetime import timedelta, datetime
from typing import Set, List
from DAG import Node
# class TimeSpan:
#     def __init__(self):
#         self.earliest
#         self.latest

class TimeSpan:
        def __init__(self, earliest: datetime = None, latest: datetime = None):
            self.earliest = earliest if earliest is not None else datetime.now()
            self.latest = latest if latest is not None else datetime.now()
            
        #TODO Link times if empty

class Task(Node):

    def __init__(self, name, duration: timedelta, *, start=None, end=None, parents: List['Task'] = None, children: List['Task'] = None):
        super(Task, self).__init__(parents=parents, children=children)
        self.name = name
        self.duration = duration
        if isinstance(start, TimeSpan):
            self.start = start
        else:
            self.start = TimeSpan()
        if isinstance(end, TimeSpan):
            self.end = end
        else:
            self.end = TimeSpan()
            
    def calculate(self):
        for root in self.getRootNodes():
            root.calculateForwards()
        for leaf in self.getLeafNodes():
            leaf.calculateBackwards()

    def calculateForwards(self):
        self.calculateEarliestEnd()
        for child in self._children:
            child.calculateForwards()
            
    def calculateBackwards(self):
        if self.isALeaf():
            self.end.latest = self.end.earliest
        self.calculateLatestStart()
        for parent in self._parents:
            parent.calculateBackwards()

    def calculateEarliestStart(self):
        if self.hasParents():
            self.start.earliest = max([ parent.end.earliest for parent in self._parents])
        
    def calculateLatestEnd(self):
        if self.hasChildren():
            self.end.latest = min([ child.start.latest for child in self._children])

    def calculateEarliestEnd(self):
        self.calculateEarliestStart()
        self.end.earliest = self.start.earliest + self.duration

    def calculateLatestStart(self):
        self.calculateLatestEnd()
        self.start.latest = self.end.latest - self.duration

from datetime import timedelta, datetime
from typing import Set, List
from DAG import Node
# class TimeSpan:
#     def __init__(self):
#         self.earliest
#         self.latest

class TimeSpan:
        def __init__(self, earliest: datetime = datetime.now(), latest: datetime = datetime.now()):
            self.earliest = earliest
            self.latest = latest

class Task(Node):

    def __init__(self, name, duration: timedelta = timedelta(), *, start=None, end=None, parents: List['Task'] = [], children: List['Task'] = []):
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

    def calculateForward(self):
        self.calculateEarliestEnd()
        for child in self._children:
            child.calculateForward()

    def setEarliestStartFromParent(self):
        startEarliest = self.start.earliest
        for parent in self._parents:
            if parent.start.earliest < startEarliest:
                startEarliest = parent.start.earliest
        self.start.earliest = startEarliest

    def calculateEarliestEnd(self):
        self.end.earliest = self.start.earliest + self.duration

    def calculateLatestStart(self):
        self.start.latest = self.end.latest - self.duration

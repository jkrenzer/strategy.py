from datetime import timedelta, datetime
from typing import Set, List
from DAG import Node
# class TimeSpan:
#     def __init__(self):
#         self.earliest
#         self.latest

class TimeSpan:
        def __init__(self, earliest: datetime = None, latest: datetime = None):
            self._earliest = earliest
            self._latest = latest

        def _getEarliest(self):
            return min(self.asList())

        def _getLatest(self):
            return max(self.asList())

        def asList(self):
            return [ value if value is not None else datetime.now() for value in  self.asRawList() ]

        def asRawList(self):
            return [self._earliest, self._latest]

        def _setEarliest(self, value):
            self._earliest = value

        def _setLatest(self, value):
            self._latest = value

        def reset(self):
            self._earliest = None
            self._latest = None

        def isEmpty(self):
            return self._earliest is None and self._latest is None

        earliest = property(_getEarliest, _setEarliest)
        latest = property(_getLatest, _setLatest)

class Task(Node):

    def __init__(self, name, duration: timedelta, *, start=None, end=None, parents: List['Task'] = None, children: List['Task'] = None):
        super(Task, self).__init__(parents=parents, children=children)
        self.name = name
        self.duration = duration
        self.pinned = False
        if isinstance(start, TimeSpan):
            self.manualStart = start
        else:
            self.manualStart = TimeSpan()
        if isinstance(end, TimeSpan):
            self.manualEnd = end
        else:
            self.manualEnd = TimeSpan()

    def _getStart(self):
        if self.isARoot():
            return TimeSpan(self.calculateEarliestStart(), None)
        else:
            return TimeSpan(self.calculateEarliestStart(), self.calculateLatestStart())

    def _getEnd(self):
        if self.isALeaf():
            return TimeSpan(self.calculateEarliestEnd(), None)
        else:
            return TimeSpan(self.calculateEarliestEnd(), self.calculateLatestEnd())

    start = property(_getStart,None)
    end = property(_getEnd,None)

    def noDatesSet(self):
        return all([node.manualStart.isEmpty() for node in self.getAll()]) and all([node.manualEnd.isEmpty() for node in self.getAll()])

    def raiseIfNoDatesSet(self):
        if self.noDatesSet():
            raise SyntaxError("You must set at least one date as fixpoint for solving!")

    def calculateEarliestStart(self):
        self.raiseIfNoDatesSet()
        if self.manualStart._earliest is not None:
            return self.manualStart._earliest
        if self.hasParents():
            return max([parent.calculateEarliestEnd() for parent in self._parents])
        else:
            return self.calculateLatestStart()

    def calculateLatestEnd(self):
        self.raiseIfNoDatesSet()
        if self.manualEnd._latest is not None:
            return self.manualEnd._latest
        if self.hasChildren():
            return min([child.calculateLatestStart() for child in self._children])
        else:
            return self.calculateEarliestEnd()

    def calculateEarliestEnd(self):
        self.raiseIfNoDatesSet()
        if self.manualEnd._earliest is not None:
            return self.manualEnd._earliest
        else:
            return self.calculateEarliestStart() + self.duration

    def calculateLatestStart(self):
        self.raiseIfNoDatesSet()
        if self.manualStart._latest is not None:
            return self.manualStart._latest
        else:
            return self.calculateLatestEnd() - self.duration

from datetime import timedelta, datetime
from typing import Set, List
from .graph import Node
from .logging import getLogger


log = getLogger(__name__)

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
            self._manualStart = start
        else:
            self._manualStart = TimeSpan()
        if isinstance(end, TimeSpan):
            self._manualEnd = end
        else:
            self._manualEnd = TimeSpan()

    def _getManualStart(self):
        return self._manualStart
    
    def _getManualEnd(self):
        return self._manualEnd
    
    def _setManualStart(self, value):
        map(lambda o: o.deleteCachedValue("start"), self.getAll)
        self._manualStart = value
    
    def _setManualEnd(self, value):
        map(lambda o: o.deleteCachedValue("end"), self.getAll)
        self._manualEnd = value

    manualStart = property(_getManualStart,_setManualStart)
    manualEnd = property(_getManualEnd,_setManualEnd)

    def _getStart(self):
            return TimeSpan(self.calculateEarliestStart(), self.calculateLatestStart())

    def _getEnd(self):
            return TimeSpan(self.calculateEarliestEnd(), self.calculateLatestEnd())

    start = property(_getStart,None)
    end = property(_getEnd,None)

    def noDatesSet(self):
        return all([node._manualStart.isEmpty() for node in self.getAll()]) and all([node._manualEnd.isEmpty() for node in self.getAll()])
    
    def getManuallyDated(self):
        allNodes = self.getAll()
        return {node for node in allNodes if not node._manualStart.isEmpty or not node._manualEnd.isEmpty}

    def raiseIfNoDatesSet(self):
        if self.noDatesSet():
            raise SyntaxError("You must set at least one date as fixpoint for solving!")

    def no_recursion(method):
        attrname = "_%s_running" % id(method)
        def decorated(self, *args, **kwargs):
            try:
                if getattr(self, attrname):
                    return None
            except AttributeError:
                pass
            setattr(self, attrname, True)
            result = method(self, *args, **kwargs)
            delattr(self, attrname)
            return result
        return decorated

    @no_recursion
    def calculateEarliestStart(self):
        self.raiseIfNoDatesSet()
        if self.manualStart._earliest is not None:
            log.debug("Node %s (%s) had a manual earliest start set: %s", self.name, str(self.getID()), str(self.manualStart._earliest))
            return self.manualStart._earliest
        if self.hasParents():
            earliestEndsParents = [e for parent in self._parents if (e := parent.calculateEarliestEnd())]
            if earliestEndsParents:
                earliestStart = max(earliestEndsParents)
                log.debug("Node %s (%s) calculated earliest start: %s", self.name, str(self.getID()), str(earliestStart))
                return earliestStart
            else:
                return None
        else:
            log.debug("Node %s (%s) determined earliest start to be latest start", self.name, str(self.getID()))
            return self.calculateLatestStart()

    @no_recursion
    def calculateLatestEnd(self):
        self.raiseIfNoDatesSet()
        if self.manualEnd._latest is not None:
            log.debug("Node %s (%s) had a manual latest end set: %s", self.name, str(self.getID()), str(self.manualEnd._latest))
            return self.manualEnd._latest
        if self.hasChildren():
            latestStartsChildren = [s for child in self._children if (s := child.calculateLatestStart())]
            if latestStartsChildren:
                latestEnd = min(latestStartsChildren)
                log.debug("Node %s (%s) calculated latest end: %s", self.name, str(self.getID()), str(latestEnd))
                return latestEnd
            else:
                return None
        else:
            log.debug("Node %s (%s) determined latest end to be earliest end", self.name, str(self.getID()))
            return self.calculateEarliestEnd()

    @no_recursion
    def calculateEarliestEnd(self):
        self.raiseIfNoDatesSet()
        if self.manualEnd._earliest is not None:
            log.debug("Node %s (%s) had a manual earliest end set: %s", self.name, str(self.getID()), str(self.manualEnd._earliest))
            return self.manualEnd._earliest
        else:
            earliestStart = self.calculateEarliestStart()
            earliestEnd = earliestStart + self.duration if earliestStart is not None else None
            log.debug("Node %s (%s) calculated earliest end: %s", self.name, str(self.getID()), str(earliestEnd))
            return earliestEnd

    @no_recursion
    def calculateLatestStart(self):
        self.raiseIfNoDatesSet()
        if self.manualStart._latest is not None:
            log.debug("Node %s (%s) had a manual latest start set: %s", self.name, str(self.getID()), str(self.manualStart._latest))
            return self.manualStart._latest
        else:
            latestEnd = self.calculateLatestEnd()
            latestStart = latestEnd - self.duration if latestEnd is not None else None
            log.debug("Node %s (%s) calculated latest start: %s", self.name, str(self.getID()), str(latestStart))
            return latestStart

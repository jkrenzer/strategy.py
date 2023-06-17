from unittest import TestCase


class TestTask(TestCase):
    def test_construction(self):
        from strategy.task import Task
        from datetime import timedelta, datetime

        a = Task("A", timedelta(days=1))
        self.assertIsInstance(a, Task)

    def test_complex_example(self):
        from strategy.task import Task
        from datetime import timedelta, datetime

        a = Task("A", timedelta(days=1))
        b = Task("B", timedelta(days=2))
        c = Task("C", timedelta(days=3))
        d = Task("D", timedelta(days=4))
        e = Task("E", timedelta(days=5))
        f = Task("F", timedelta(days=6))
        g = Task("G", timedelta(days=7))

        a1 = Task("A1", timedelta(days=1))
        g1 = Task("G1", timedelta(days=7))

        a.addChild(b)
        b.addChild(c)
        c.addChild(d)
        d.addChild(e)
        e.addChild(f)
        f.addChild(g)

        a1.addChild(d)
        d.addChild(g1)

        a.manualStart.earliest = datetime(year=2018, month=1, day=1, hour=8, minute=0)
        self.assertEqual(
            g.end.earliest,
            datetime(year=2018, month=1, day=1, hour=8, minute=0) + timedelta(days=28),
        )
        self.assertEqual(
            g1.end.earliest,
            datetime(year=2018, month=1, day=1, hour=8, minute=0) + timedelta(days=17),
        )
        a1.manualStart.earliest = datetime(year=2018, month=2, day=1, hour=8, minute=0)
        self.assertEqual(
            g.end.earliest,
            datetime(year=2018, month=2, day=1, hour=8, minute=0) + timedelta(days=23),
        )
        self.assertEqual(
            g1.end.earliest,
            datetime(year=2018, month=2, day=1, hour=8, minute=0) + timedelta(days=12),
        )


test_cases = [TestTask]

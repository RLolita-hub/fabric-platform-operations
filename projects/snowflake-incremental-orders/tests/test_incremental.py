import tempfile
import unittest
from pathlib import Path
from src.incremental import apply
class IncrementalTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup);self.db=str(Path(self.t.name)/"a.db")
    def e(self,v=1,a=100,op="UPSERT"):return dict(order_id="O1",version=v,amount_cents=a,op=op)
    def test_replay(self):
        apply(self.db,[self.e()]);self.assertEqual(apply(self.db,[self.e()]),(1,100))
    def test_update(self):
        apply(self.db,[self.e()]);self.assertEqual(apply(self.db,[self.e(2,200)]),(1,200))
    def test_delete_and_late_arrival(self):
        apply(self.db,[self.e(2,0,"DELETE")]);self.assertEqual(apply(self.db,[self.e()]),(0,0))
    def test_conflict_current(self):
        apply(self.db,[self.e()])
        with self.assertRaises(ValueError):apply(self.db,[self.e(1,200)])
    def test_conflict_in_batch(self):
        with self.assertRaises(ValueError):apply(self.db,[self.e(),self.e(1,200)])
    def test_invalid_amount(self):
        with self.assertRaises(ValueError):apply(self.db,[self.e(1,-1)])

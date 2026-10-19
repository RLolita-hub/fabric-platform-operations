import unittest
from src.mapping_contract import transform
class MappingTests(unittest.TestCase):
    def row(self,amount="10.25",**kw):return dict(source="crm",order_id="O1",amount=amount,currency="USD",**kw)
    def test_cents_exact(self):self.assertEqual(transform([self.row()])["revenue_cents"],1025)
    def test_no_fractional_cent_rounding(self):self.assertEqual(transform([self.row("1.001")])["rejected"][0]["reason"],"INVALID_AMOUNT")
    def test_nonfinite(self):
        for a in ("NaN","Infinity","-1","bad"):
            self.assertEqual(len(transform([self.row(a)])["rejected"]),1)
    def test_exact_duplicate(self):self.assertEqual(len(transform([self.row(),self.row()])["accepted"]),1)
    def test_conflict_stops_batch(self):
        with self.assertRaises(ValueError):transform([self.row(),self.row("11")])
    def test_currency(self):
        r=self.row();r["currency"]="EUR"
        self.assertEqual(transform([r])["rejected"][0]["reason"],"UNSUPPORTED_CURRENCY")

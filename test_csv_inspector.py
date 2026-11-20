
import csv
import tempfile
import unittest
from pathlib import Path
from csv_inspector import analyze_csv

class TestCSVInspector(unittest.TestCase):
    def test_summary(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "sample.csv"
            p.write_text("name,age\nAlice,25\nBob,30\n", encoding="utf-8")
            result = analyze_csv(str(p))
            self.assertEqual(result["rows"], 2)
            self.assertEqual(result["columns"], ["name", "age"])
            self.assertEqual(result["duplicate_rows"], 0)

    def test_missing_values(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "sample.csv"
            p.write_text("name,age\nAlice,25\nBob,\n", encoding="utf-8")
            result = analyze_csv(str(p))
            self.assertEqual(result["missing_values"]["age"], 1)

    def test_duplicates(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "sample.csv"
            p.write_text("name,age\nAlice,25\nAlice,25\n", encoding="utf-8")
            result = analyze_csv(str(p))
            self.assertEqual(result["duplicate_rows"], 1)

if __name__ == "__main__":
    unittest.main()

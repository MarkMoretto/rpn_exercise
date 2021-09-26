import unittest

import math
from rpn.src._rpn import ComparisonMixin, OperatorsMixin
from rpn.src._exceptions import ValueCountError



class ComparisonMixinTestCase(unittest.TestCase):
    def setUp(self):
        self.cm = ComparisonMixin()

    def test_is_int(self):
        """Test ComparisonMixin.is_int() method on various
        numeric and non-numeric scenarios.
        """
        tests = [
            dict(candidate = "1", expected = True),
            dict(candidate = "1.0", expected = True),
            dict(candidate = "1.01", expected = False),
            dict(candidate = "-1", expected = True),
            dict(candidate = "-1.0", expected = True),
            dict(candidate = "-1.01", expected = False),

            dict(candidate = "-0", expected = True),
            dict(candidate = "-0.0", expected = False),
            dict(candidate = "-0.01", expected = False),

            dict(candidate = 1, expected = True),
            dict(candidate = 1.0, expected = False),
            dict(candidate = 1.01, expected = False),
            
            dict(candidate = None, expected = False),
            dict(candidate = "A", expected = False),
        ]
        for t in tests:
            with self.subTest():
                self.assertEqual(self.cm.is_int(t["candidate"]), t["expected"])            

    def test_is_float(self):
        """Test ComparisonMixin.is_float() method on various
        numeric and non-numeric scenarios.
        """
        tests = [
            dict(candidate = "1", expected = False),
            dict(candidate = "1.0", expected = False),
            dict(candidate = "1.01", expected = True),
            dict(candidate = "-1", expected = False),
            dict(candidate = "-1.0", expected = False),
            dict(candidate = "-1.01", expected = True),

            dict(candidate = "-0", expected = False),
            dict(candidate = "-0.0", expected = True),
            dict(candidate = "-0.01", expected = True),

            dict(candidate = 1, expected = False),
            dict(candidate = 1.0, expected = True),
            dict(candidate = 1.01, expected = True),
            
            dict(candidate = None, expected = False),
            dict(candidate = "A", expected = False),
        ]
        for t in tests:
            with self.subTest():
                self.assertEqual(self.cm.is_float(t["candidate"]), t["expected"])  

    def test_is_string(self):
        """Test ComparisonMixin.is_string() method on various
        numeric and non-numeric scenarios.
        """
        tests = [
            dict(candidate = "", expected = True),

            dict(candidate = "1", expected = True),
            dict(candidate = "1.0", expected = True),
            dict(candidate = "1.01", expected = True),

            dict(candidate = "0", expected = True),
            dict(candidate = "0.0", expected = True),
            dict(candidate = "0.01", expected = True),

            dict(candidate = "-1", expected = True),
            dict(candidate = "-1.0", expected = True),
            dict(candidate = "-1.01", expected = True),

            dict(candidate = "-0", expected = True),
            dict(candidate = "-0.0", expected = True),
            dict(candidate = "-0.01", expected = True),

            dict(candidate = 1, expected = False),
            dict(candidate = 1.0, expected = False),
            dict(candidate = 1.01, expected = False),
            
            dict(candidate = None, expected = False),
            dict(candidate = "A", expected = True),
        ]
        for t in tests:
            with self.subTest():
                self.assertEqual(self.cm.is_string(t["candidate"]), t["expected"])  


if __name__ == "__main__":
    unittest.main()

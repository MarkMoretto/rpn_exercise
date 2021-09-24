
import unittest

import math
from ..src._rpn import Expression, OperatorsMixin, Rpn



class ExpressionsTestCase(unittest.TestCase):
    def setUp(self):
        self.e = Expression("+", lambda a, b: b + a)

    def test_expression_alias(self):
        self.assertEqual(self.e.alias, "+")

    def test_expression_signature(self):
        self.assertEqual(self.e.signature, "(a, b)")  

    def test_expression_func_string(self):
        self.assertEqual(self.e.func_string, "b + a")        

    def test_expression_lengths(self):
        self.assertEqual(self.e.lengths, (1, 6, 5))            

    def test_expression_values(self):
        self.assertEqual(self.e.values, ('+', '(a, b)', 'b + a'))

    def test_expression_proc_function(self):
        self.assertEqual(self.e.process_function(self.e.function), "b + a")

    @unittest.expectedFailure
    def test_expression_init_fail(self):
        self.assertEqual(Expression(""), "<class 'src._rpn.Expression'>")        

    def tearDown(self):
        del self.e


class RpnTestCase(unittest.TestCase):
    def setUp(self):
        self.rpn = Rpn()

    def test_rpn_init_stack(self):
        self.assertEqual(self.rpn.stacker, [])

    def test_rpn_basic_operators(self):
        expected = ['*', '+', '-', '/', '^', 'acos', 'cos', 'e', 'log', 'sin', 'tanh']
        for i in self.rpn.operators:
            with self.subTest(i=i):
                self.assertEqual(1 if i in expected else 0, 1)

    def test_rpn_is_int(self):
        cases = [
            {"1": True},
            {"1": False},
            {"1.01": True},
            {"1.01": False}
        ]
        for case in cases:
            for num, expected in case.items():
                with self.subTest():
                    self.assertEqual(self.rpn.is_int(num), expected)
            

    def test_expression_add_expression(self):
        """Testing Rpn.new_expression()"""
        prev_len = len(self.rpn.OPERATIONS)
        self.rpn.add_expression("gcd", lambda a, b: math.gcd(b, a))
        post_len = len(self.rpn.OPERATIONS)
        self.assertGreater(post_len, prev_len)

    # def test_expression_lengths(self):
    #     self.assertEqual(self.e.lengths, (1, 6, 5))            

    # def test_expression_values(self):
    #     self.assertEqual(self.e.values, ('+', '(a, b)', 'b + a'))

    # def test_expression_proc_function(self):
    #     self.assertEqual(self.e.process_function(self.e.function), "b + a")

    def tearDown(self):
        del self.rpn



if __name__ == "__main__":
    unittest.main()

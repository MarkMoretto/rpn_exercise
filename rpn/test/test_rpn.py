
import unittest

import math
from rpn.src._rpn import Expression, OperatorsMixin, Rpn
from rpn.src._exceptions import ValueCountError



class ExpressionsTestCase(unittest.TestCase):
    def setUp(self):
        self.e = Expression("+", lambda a, b: b + a)

    def test_expression_alias(self):
        """Test for correct Expression().alias
        on test instance.
        """
        self.assertEqual(self.e.alias, "+")

    def test_expression_signature(self):
        """Test for correct Expression().signature
        on test instance.
        """        
        self.assertEqual(self.e.signature, "(a, b)")  

    def test_expression_func_string(self):
        """Test for correct Expression().func_string
        on test instance.
        """
        self.assertEqual(self.e.func_string, "b + a")        

    def test_expression_lengths(self):
        """Test for correct Expression().lengths
        on test instance.
        """
        self.assertEqual(self.e.lengths, (1, 6, 5))            

    def test_expression_values(self):
        """Test for correct Expression().values
        on test instance.
        """
        self.assertEqual(self.e.values, ('+', '(a, b)', 'b + a'))

    def test_expression_proc_function(self):
        """Test for correct Expression().process_function()
        on test instance and test function.
        """        
        self.assertEqual(self.e.process_function(self.e.function), "b + a")

    def test_expression_init_fail(self):
        """Test for zero-length operator expression on instance creation.
        """
        with self.assertRaises(ValueError):
            Expression("")

    def tearDown(self):
        del self.e


class RpnTestCase(unittest.TestCase):
    def setUp(self):
        self.rpn = Rpn()

    def test_rpn_init_stack(self):
        """Test that Rpn.stacker is empty when initializing class instance.
        """
        self.assertEqual(self.rpn.stacker, [])

    def test_rpn_basic_operators(self):
        """Test that all initial operators appear when initializing Rpn().
        """
        all_operators = ['*', '+', '-', '/', '^', 'acos', 'cos', 'e', 'log', 'sin', 'tanh']
        expected = len(all_operators)

        n_equal = 0
        for oper in self.rpn.operators:
            if oper in all_operators:
                n_equal += 1
        self.assertEqual(n_equal, expected)

    def test_rpn_is_int(self):
        """Testing Rpn.is_int() on mix of integer and float strings."""
        cases = [
            {"1": True},
            {"-1": True},
            {"1.01": False},
            {"1.00000001": False},        
        ]
        for case in cases:
            for num, expected in case.items():
                with self.subTest():
                    self.assertEqual(self.rpn.is_int(num), expected)

    def test_rpn_is_int_incorrect_type(self):
        """Testing failure on Rpn.is_int() for alphabetic
        character and zero-length character.
        """
        test_items = ["", "A"]
        for item in test_items:
            with self.subTest():
                with self.assertRaises(ValueError):
                    self.rpn.is_int(item)


    def test_expression_add_expression(self):
        """Testing Rpn.new_expression()"""
        prev_len = len(self.rpn.OPS_DOUBLE_ARG)
        self.rpn.add_expression("gcd", lambda a, b: math.gcd(b, a))
        post_len = len(self.rpn.OPS_DOUBLE_ARG)
        self.assertGreater(post_len, prev_len)

    def test_rpn_reset(self):
        expected = []
        self.rpn.execute_next("2")
        self.rpn.reset

        self.assertEqual(self.rpn.status, expected)

    def test_rpn_execute_next_single_int(self):
        """Testing Rpn.execute_next() for entry 2.
        """        
        expected = [2.0]
        self.rpn.execute_next("2")
        self.assertEqual(self.rpn.status, expected)

    def test_rpn_execute_next_dual_int(self):
        """Testing Rpn.execute_next() for entries 2, 3.
        """        
        expected = [2.0, 3.0]
        self.rpn.execute_next("2")
        self.rpn.execute_next("3")
        self.assertEqual(self.rpn.status, expected)

    def test_rpn_execute_next_complete_execution(self):
        """Testing Rpn.execute_next() for entries 2, 3, +.
        """
        expected = [5.0]
        self.rpn.execute_next("2")
        self.rpn.execute_next("3")
        self.rpn.execute_next("+")     
        self.assertEqual(self.rpn.status, expected)

    def test_rpn_execute_valid_result(self):
        """Testing Rpn.result property for entries 2, 3, +.
        """
        expected = 5
        self.rpn.execute_next("2")
        self.rpn.execute_next("3")
        self.rpn.execute_next("+")     
        self.assertEqual(self.rpn.result, expected)

    def test_rpn_execute_next_invalid_token(self):
        """Testing Rpn.execute_next() property for entries 2, 3, +, -.
        """
        self.rpn.execute_next("2")
        self.rpn.execute_next("3")
        self.rpn.execute_next("+")
        with self.assertRaises(ValueCountError):
            self.rpn.execute_next("-")

    def test_rpn_execute_next_initial_value_error(self):
        """Testing Rpn.execute_next() for initial value that
        is not a number nor a valid operator.
        """
        with self.assertRaises(ValueError):
            self.rpn.execute_next("{")

    def test_rpn_stack_size(self):
        """Testing Rpn.stack_size property for one valid value.
        """
        expected = 1
        self.rpn.reset
        self.rpn.execute_next("2")
        self.assertEqual(self.rpn.stack_size, expected)

    def test_rpn_stack_size_anti(self):
        """Testing Rpn.stack_size property for one valid value.
        """
        expected = 0
        self.rpn.reset
        self.rpn.execute_next("+")
        self.assertEqual(self.rpn.stack_size, expected)        

    def tearDown(self):
        del self.rpn

class RpnExecutionTestCase(unittest.TestCase):
    def setUp(self):
        self.rpn = Rpn()


    def test_rpn_execution_case_1(self):
        """Test expression:
        5 8 +
        """
        expected = 13
        self.rpn.execute_next("5")
        self.rpn.execute_next("8")
        self.rpn.execute_next("+")
        self.assertEqual(self.rpn.result, expected)

    def test_rpn_execution_case_2(self):
        """Test expression:
        5 5 5 8 + + -
        """
        expected = -13
        
        self.rpn.execute_next("5")
        self.rpn.execute_next("5")
        self.rpn.execute_next("5")
        self.rpn.execute_next("8")
        self.rpn.execute_next("+")
        self.rpn.execute_next("+")
        self.rpn.execute_next("-")

        self.assertEqual(self.rpn.result, expected)

    def test_rpn_execution_case_3(self):
        """Test expression:
        5 5 5 8 + + -
        13 +
        """
        expected = 0
        
        self.rpn.execute_next("5")
        self.rpn.execute_next("5")
        self.rpn.execute_next("5")
        self.rpn.execute_next("8")
        self.rpn.execute_next("+")
        self.rpn.execute_next("+")
        self.rpn.execute_next("-")

        self.rpn.execute_next("13")
        self.rpn.execute_next("+")

        self.assertEqual(self.rpn.result, expected)


    def test_rpn_execution_case_4(self):
        """Test expression:
        -3 -2 * 5 +
        """
        expected = 11
        self.rpn.execute_next("-3")
        self.rpn.execute_next("-2")
        self.rpn.execute_next("*")
        self.rpn.execute_next("5")
        self.rpn.execute_next("+")
        self.assertEqual(self.rpn.result, expected)

    def test_rpn_execution_case_5(self):
        """Test expression:
        5 9 1 - /
        """
        expected = 0.625
        self.rpn.execute_next("5")
        self.rpn.execute_next("9")
        self.rpn.execute_next("1")
        self.rpn.execute_next("-")
        self.rpn.execute_next("/")
        self.assertEqual(self.rpn.result, expected)

    def tearDown(self):
        del self.rpn



if __name__ == "__main__":
    unittest.main()

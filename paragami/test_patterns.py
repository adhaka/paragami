#!/usr/bin/env python3
import copy
import unittest
from numpy.testing import assert_array_almost_equal
import numpy as np

from paragami import base_patterns
from paragami import numeric_array_patterns
from paragami import pdmatrix_patterns


def _test_pattern(
    testcase, pattern, valid_value, check_equal=assert_array_almost_equal):

    # Execute required methods.
    empty_val = pattern.empty(valid=True)
    pattern.flatten(empty_val, free=False)
    empty_val = pattern.empty(valid=False)

    random_val = pattern.random()
    pattern.flatten(random_val, free=False)

    str(pattern)

    # Make sure to test != using a custom test.
    testcase.assertTrue(pattern == pattern)

    #pattern_serial = pattern.serialize()
    #pattern.unserialize(pattern_serial)

    for free in [True, False]:
        flat_val = pattern.flatten(valid_value, free=free)
        testcase.assertEqual(len(flat_val), pattern.flat_length(free))
        folded_val = pattern.fold(flat_val, free=free)
        check_equal(valid_value, folded_val)


class TestPatterns(unittest.TestCase):
    def test_numeric_array_patterns(self):
        for test_shape in [(2, ), (2, 3), (2, 3, 4)]:
            valid_value = np.random.random(test_shape)
            pattern = numeric_array_patterns.NumericArrayPattern(test_shape)
            _test_pattern(self, pattern, valid_value)

            pattern = numeric_array_patterns.NumericArrayPattern(test_shape, lb=-1)
            _test_pattern(self, pattern, valid_value)

            pattern = numeric_array_patterns.NumericArrayPattern(test_shape, ub=2)
            _test_pattern(self, pattern, valid_value)

            pattern = numeric_array_patterns.NumericArrayPattern(test_shape, lb=-1, ub=2)
            _test_pattern(self, pattern, valid_value)

            # Test equality comparisons.
            self.assertTrue(
                numeric_array_patterns.NumericArrayPattern((1, 2)) !=
                numeric_array_patterns.NumericArrayPattern((1, )))

            self.assertTrue(
                numeric_array_patterns.NumericArrayPattern((1, 2)) !=
                numeric_array_patterns.NumericArrayPattern((1, 3)))

            self.assertTrue(
                numeric_array_patterns.NumericArrayPattern((1, 2), lb=2) !=
                numeric_array_patterns.NumericArrayPattern((1, 2)))

            self.assertTrue(
                numeric_array_patterns.NumericArrayPattern((1, 2), lb=2, ub=4) !=
                numeric_array_patterns.NumericArrayPattern((1, 2), lb=2))


    def test_pdmatrix_patterns(self):
        dim = 3
        valid_value = np.eye(dim) * 3 + np.full((dim, dim), 0.1)
        pattern = pdmatrix_patterns.PDMatrixPattern(dim)
        _test_pattern(self, pattern, valid_value)

        pattern = pdmatrix_patterns.PDMatrixPattern(dim, diag_lb=0.5)
        _test_pattern(self, pattern, valid_value)

        self.assertTrue(
            pdmatrix_patterns.PDMatrixPattern(3) !=
            pdmatrix_patterns.PDMatrixPattern(4))

        self.assertTrue(
            pdmatrix_patterns.PDMatrixPattern(3, diag_lb=2) !=
            pdmatrix_patterns.PDMatrixPattern(3))

        # TODO: test the autodiff stuff.


    def test_dictionary_patterns(self):
        def check_dict_equal(dict1, dict2):
            self.assertEqual(dict1.keys(), dict2.keys())
            for key  in dict1:
                assert_array_almost_equal(dict1[key], dict2[key])

        dict_pattern = base_patterns.OrderedDictPattern()
        dict_pattern['a'] = \
            numeric_array_patterns.NumericArrayPattern((2, 3, 4), lb=-1, ub=2)
        dict_pattern['b'] = \
            numeric_array_patterns.NumericArrayPattern((5, ), lb=-1, ub=10)
        dict_pattern['c'] = \
            numeric_array_patterns.NumericArrayPattern((5, 2), lb=-1, ub=10)

        self.assertEqual(list(dict_pattern.keys()), ['a', 'b', 'c'])

        dict_val = dict_pattern.random()
        _test_pattern(self, dict_pattern, dict_val, check_dict_equal)

        # Check that it works with ordinary dictionaries, not only OrderedDict.
        plain_dict_val = dict(dict_val)
        _test_pattern(self, dict_pattern, plain_dict_val, check_dict_equal)

        # Check deletion and non-equality.
        old_dict_pattern = copy.deepcopy(dict_pattern)
        del dict_pattern['b']
        self.assertTrue(dict_pattern != old_dict_pattern)
        dict_val = dict_pattern.random()
        _test_pattern(self, dict_pattern, dict_val, check_dict_equal)

        # Check adding a new element.
        dict_pattern['d'] = \
            numeric_array_patterns.NumericArrayPattern((4, ), lb=-1, ub=10)
        dict_val = dict_pattern.random()
        _test_pattern(self, dict_pattern, dict_val, check_dict_equal)


if __name__ == '__main__':
    unittest.main()

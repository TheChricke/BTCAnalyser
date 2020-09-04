import unittest

import DataHelper


class TestDataHelper(unittest.TestCase):

    def test_calculate_hypothetical_s2f(self):
        DataHelper.HypotheticalS2FCalculator.calculateHypotheticalS2F()
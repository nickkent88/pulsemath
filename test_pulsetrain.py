import unittest

from pulsetrain import *

class TestPulseMethods(unittest.TestCase):

    def setUp(self):
        self.low_pulse = Pulse(0, 2)
        self.mid_pulse1 = Pulse(1, 3)
        self.mid_pulse2 = Pulse(2.5, 4.5)
        self.mid_pulse3 = Pulse(4, 6)
        self.high_pulse = Pulse(5, 7)

    def tearDown(self):
        pass

    def test_eq_with_lower(self):
        pass

    def test_eq_with_higher(self):
        pass

    def test_eq_with_equal(self):
        pass

    def test_lt_with_lower(self):
        pass

    def test_lt_with_higher(self):
        pass

    def test_lt_with_equal(self):
        pass

    def test_le_with_lower(self):
        pass

    def test_le_with_higher(self):
        pass

    def test_le_with_equal(self):
        pass

    def test_absolute_overlap_0_percent(self):
        pass

    def test_absolute_overlap_50_percent(self):
        pass

    def test_absolute_overlap_100_percent(self):
        pass


class TestPulseTrainMethods(unittest.TestCase):

    def test___iter___(self):
        pass

    def test___getitem___(self):
        pass

    def test_shift_phase_0(self):
        pass

    def test_shift_phase_negative(self):
        pass

    def test_shift_phase_positive(self):
        pass



    def test_coincidence_fraction(self):
        pass

if __name__ == '__main__':
    unittest.main()
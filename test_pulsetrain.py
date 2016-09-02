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

    def test_eq_with_overlapping(self):
        self.assertFalse(self.low_pulse == self.mid_pulse1)

    def test_eq_with_nonoverlapping(self):
        self.assertFalse(self.low_pulse == self.mid_pulse2)

    def test_eq_with_equal(self):
        self.assertTrue(self.low_pulse == self.low_pulse)

    def test_lt_with_lower(self):
        self.assertTrue(self.low_pulse < self.mid_pulse2)

    def test_lt_with_higher(self):
        self.assertFalse(self.high_pulse < self.mid_pulse2)

    def test_lt_with_equal(self):
        self.assertFalse(self.mid_pulse2 < self.mid_pulse2)

    def test_le_with_lower(self):
        self.assertTrue(self.low_pulse <= self.mid_pulse2)

    def test_le_with_higher(self):
        self.assertFalse(self.high_pulse <= self.mid_pulse2)

    def test_le_with_equal(self):
        self.assertFalse(self.mid_pulse2 <= self.mid_pulse2)

    def test_overlap_0(self):
        overlap = Pulse.overlap(self.low_pulse, self.high_pulse)
        self.assertEqual(overlap, 0)

    def test_overlap_1(self):
        overlap = Pulse.overlap(self.low_pulse, self.mid_pulse1)
        self.assertEqual(overlap, 1)

    def test_overlap_2(self):
        overlap = Pulse.overlap(self.low_pulse, self.low_pulse)
        self.assertEqual(overlap, 2)

    def test_proportional_overlap_0_percent(self):
        overlap = Pulse.proportional_overlap(self.low_pulse, self.high_pulse)
        self.assertEqual(overlap, 0)

    def test_proportional_overlap_50_percent(self):
        overlap = Pulse.proportional_overlap(self.low_pulse, self.mid_pulse1)
        self.assertEqual(overlap, .5)

    def test_proportional_overlap_100_percent(self):
        overlap = Pulse.proportional_overlap(self.low_pulse, self.low_pulse)
        self.assertEqual(overlap, 1)


class TestPulseTrainMethods(unittest.TestCase):

    def setUp(self):
        self.train = PulseTrain(1000, Pulse(0,10))
        self.train1 = PulseTrain(1000, Pulse(0,10), 6000)
        self.train2 = PulseTrain(1000, Pulse(0,10), 6000)
        self.pulses = (Pulse(0, .2),
                  Pulse(37.5, 37.7),
                  Pulse(75, 75.2),
                  Pulse(112.5, 112.5),
                  Pulse(150, 162),
                  Pulse(300, 312),
                  Pulse(450, 570))
        self.train3 = PulseTrain(1200, self.pulses, 6000)

    def tearDown(self):
        pass

    def test_train_lengths(self):
        self.assertEqual(len(self.train1), 6)
        self.assertEqual(len(self.train3), 35)

    def test___iter___(self):
        count = 0
        for pulse1, pulse2 in zip(self.train3, self.pulses*5):
            self.assertEqual(pulse1, pulse2)
            count += 1
        self.assertEqual(count, 35)

    def test___getitem___with_integer(self):
        self.assertEqual(self.train3[4], self.pulses[4])

    def test___getitem___with_slice(self):
        self.assertEqual(self.train3[0:4], NotImplemented)

    def test_shift_phase_by_0(self):
        self.assertEqual(self.train1, self.train2)
        self.train2.shift_phase(0)
        self.assertEqual(self.train1, self.train2)

    def test_shift_phase_by_duration(self):
        self.assertEqual(self.train1, self.train2)
        self.train2.shift_phase(6000)
        self.assertEqual(len(self.train2), len(self.train1))
        self.assertEqual(self.train1, self.train2)

    def test_shift_phase_so_a_pulse_overlaps(self):
        train = PulseTrain(1000, (Pulse(0, 10), Pulse(500, 510)))
        train.shift_phase(995)   
        should_equal = PulseTrain(1000, (Pulse(0, 5),
                                         Pulse(495, 505),
                                         Pulse(995, 1000)))
        self.assertEqual(train, should_equal)

    def test_shift_phase_of_train_that_already_has_circular_overlap(self):
        train1 = PulseTrain(1000, (Pulse(0, 10), Pulse(500, 510)))
        train2 = PulseTrain(1000, (Pulse(0, 10), Pulse(500, 510)))
        train1.shift_phase(995)   
        should_equal = PulseTrain(1000, (Pulse(0, 5),
                                         Pulse(495, 505),
                                         Pulse(995, 1000)))
        self.assertEqual(train1, should_equal)
        print(train1)
        train1.shift_phase(5)
        print(train1)
        self.assertEqual(train1, train2)

    def test_shift_phase_negative(self):
        pass

    def test_shift_phase_positive(self):
        pass

    def test_coincidence_fraction(self):
        pass


class TestUtilityMethods(unittest.TestCase):

    def setUp(self):
        EPSILON = .000001

    def tearDown(self):
        pass

    def test_eq_float_neq(self):
        self.assertFalse(eq_float(0.0, 2.5))

    def test_eq_float_eq(self):
        self.assertTrue(eq_float(2.5, 2.5))
        pass

if __name__ == '__main__':
    unittest.main()
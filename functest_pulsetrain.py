import unittest

from pulsetrain import *

class CoincidenceFraction(unittest.TestCase):

    def test_coincidence_fraction(self):
        # Make pulse for simple magnetron train, with width=1
        pulse = Pulse(0, 1)
        self.assertIsInstance(pulse.start_time, float)
        self.assertIsInstance(pulse.end_time, float)
        self.assertIsInstance(pulse.width, float)
        self.assertEqual(pulse.start_time, 0)
        self.assertEqual(pulse.end_time, 1)
        self.assertEqual(pulse.width, 1)

        # Make simple magnetron train
        s_train = PulseTrain(1000, 6000, pulse)
        self.assertIsInstance(s_train.pri, float)
        self.assertIsInstance(s_train.duration, float)
        self.assertEqual(s_train.pri, 1000)
        self.assertEqual(s_train.duration, 6000)
        self.assertEqual(len(s_train), 1) 

        # Make pulses for general solid-state train
        pulses = (Pulse(0, .2),
                  Pulse(37.5, 37.7),
                  Pulse(75, 75.2),
                  Pulse(112.5, 112.5),
                  Pulse(150, 162),
                  Pulse(300, 312),
                  Pulse(450, 570))

        # Make solid state train
        c_train = PulseTrain(1200, 6000, pulses)
        self.assertEqual(len(c_train), 7) 

        # Compute coincidence fraction via sim
        f_c = PulseTrain.coincidence_fraction(s_train, c_train, 'sim')
        f_c_actual = .1265
        self.assertAlmostEqual(f_c, f_c_actual, 7)

        # Finish tests
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
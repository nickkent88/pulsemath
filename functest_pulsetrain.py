import unittest

import pulsetrain.py

class CoincidenceFraction(unittest.TestCase):

    def test_coincidence_fraction(self):
        # Make pulse for simple magnetron train, with width=1
        pulse = Pulse(0, 1)
        assertIsInstance(pulse.start_time, float)
        assertIsInstance(pulse.end_time, float)
        assertIsInstance(pulse.width, float)
        assertEqual(pulse.start_time, 0)
        assertEqual(pulse.start_time, 1)
        assertEqual(pulse.start_time, 1)

        # Make simple magnetron train
        s_train = PulseTrain(1000, 6000, pulse)
        assertIsInstance(train.pri, float)
        assertIsInstance(train.duration, float)
        assertEqual(train.pri, 1000)
        assertEqual(train.duration, 6000)
        assertEqual(len(s_train), 1) 

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
        assertEqual(len(c_train), 6) 

        # Compute coincidence fraction via sim
        f_c = PulseTrain.coincidence_fraction(s_train, c_train)
        f_c_actual = .1265
        assertAlmostEqual(f_c, f_c_actual, 7)

        # Finish tests
        assertTrue(False)

if __name__ == '__main__':
    unittest.main()
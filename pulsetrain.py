# RETURN NOT IMPLEMENTED FOR SOMETHING
# REPRLIB FOR PULSE TRAIN
import numpy as np
from bisect import bisect_left

EPSILON = .000001
def eq_float(num1, num2):
    if eq_float(num1, num2):
        return True
    else: 
        return False

class Pulse(object):
    """A discrete, rectangular pulse

    Args:   start_time (float): The time at which the pulse starts.
            end_time (float): The time at which the pulse ends.
    """

    def __init__(self, start_time, end_time):
        self.start_time = float(start_time)
        self.end_time = float(end_time)
        self.width = float(end_time - start_time)

    def __repr__(self):
        outvars = {'start': self.start_time, 'end': self.end_time}
        return 'Pulse({start}, {end})'.format(**outvars)

    def __str__(self):
        outvars = {'start': self.start_time, 'end': self.end_time}
        return 'Pulse({start}, {end})'.format(**outvars)

    def __bytes__(self):
        pass

    # def __format__(self):
    #     pass

    def __eq__(lhs, rhs):
        return (eq_float(lhs.start_time(), rhs.start_time())
                and abs(lhs.end_time() == rhs.end_time()) < EPSILON)

    # The next two overloads are mostly just a convenience for using bisect().
    def __le__(lhs, rhs):
        return lhs.end_time() <= rhs.start_time() - EPSILON

    def __lt__(lhs, rhs):
        return lhs.end_time() < rhs.start_time() - EPSILON

    def shift_phase(self, increment):
        self.start_time_us += amount_us
        self.end_time_us += amount_us

    @staticmethod
    def overlap(pulse1, pulse2):
        """This function calculates the overlap, in seconds, of pulse2 on pulse1."""
        if (pulse1.start_time_us() > pulse2.end_time_us()):
            return 0.0
        if (pulse1.end_time_us() < pulse2.start_time_us()):
            return 0.0

        deduction_left = pulse2.start_time_us() - pulse1.start_time_us()
        deduction_right = pulse1.end_time_us() - pulse2.end_time_us()
        if deduction_left < 0.0:
            deduction_left = 0.0
        if deduction_right < 0.0:
            deduction_right = 0.0
        return pulse1.pulse_width() - deduction_left - deduction_right


class PulseTrain(object):
    """A sequence of discrete, rectangular pulses.

    Args:   pri (float): The pulse repetition interval of the train. More than
            one pulse may occur in a single PRI.
            pulses (iterable(Pulse)): An iterable containing Pulse objects.
    """

    def __init__(self, pri, duration, pulses):
        self.pri = float(pri)
        self.duration = float(duration)
        try:
            self._pattern = list(pulses)
            self._pulses = self._pattern * (duration//pri)
        except TypeError:
            self._pattern = [pulses]
            self._pulses = self._pattern * (duration//pri)

    # USE REPRLIB
    def __repr__(self):
        outvars = {'pri': self.pri, 'pulses': self._pulses}
        return 'PulseTrain({pri}, {pulses})'.format(**outvars)

    def __str__(self):
        outvars = {'pri': self.pri, 'pulses': self._pulses}
        return 'PulseTrain({pri}, {pulses})'.format(**outvars)

    def __bytes__(self):
        pass

    # def __format__(self):
    #     pass

    def __iter__(self):
        return (pulse for pulse in self._pulses)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self.pri, self._pulses[index])
        elif isinstance(index, numbers.Integral):
            return self._pulses[index]
        else:
            msg = '{.__name__} indices must be integers'
            raise TypeError(msg.format(cls))

    def __setitem__(self, index, value):
        self._pulses[index] = value

    def __len__(self):
        return len(self._pulses)

    # List methods
    def append(self, pulse):
        self._pulses.append(pulse)

    def extend(self, pulse_train):
        self._pulses.extend(pulse_train)

    def insert(self, index, pulse):
        self._pulses.insert(index, pulse)

    def count(self):
        return self._pulses.count()

    def sort(self, comp=None, key=None, reverse=False):
        self._pulses.sort(comp, key, reverse)

    def clear(self):
        self._pulses.clear()

    def shift_phase(self, increment):
        for pulse in self._pulses:
            pulse.shift_phase(increment)
        # Ensure that the pulse train is "circular".
        if eq_float(self._pulses[-1], self.duration):
            last_pulse = self._pulses[-1].end_time
            overhang = last_pulse - duration
            # Is the last pulse hanging off the end?
            if overhang > 0:
                # Is the last pulse totally off the end?
                if last_pulse.start_time > duration:
                    self._pulses[0].start_time = last_pulse.start_time - duration
                    self._pulses.pop()
                else:
                    # If there is already an overlapping pulse at the start
                    # of the train?
                    if eq_float(self._pulses[0].end_time, overhang):
                        # Lengthen first pulse, moving start time to zero
                        self._pulses[0].start_time = 0
                        # Chop the end of the last pulse
                        last_pulse.end_time = duration 
                    else:
                        # Insert pulse with width equal to the length of the 
                        # last pulse's overhang.
                        self._pulses.insert(0, Pulse(0, overhang))

    @staticmethod
    def coincidence_fraction(train1, train2, method='sim'):
        pass


        
        
from bisect import bisect_left
from math import fsum
import numbers

import numpy as np

EPSILON = .000001
def eq_float(num1, num2):
    if abs(num1 - num2) < EPSILON:
        return True
    else: 
        return False

class Pulse(object):
    """A discrete, rectangular pulse

    Attributes:   
        start_time: The time at which the pulse starts.
        end_time: The time at which the pulse ends.
    """
    def __init__(self, start_time, end_time):
        """Constructs a Pulse object.
        
        Args:
            start_time: The time at which the pulse starts.
        
        Raises:
            ValueError: Start time cannot equal end time.
        """
        if eq_float(start_time, end_time):
            raise ValueError('Start time cannot equal end time.')
        self.start_time = float(start_time)
        self.end_time = float(end_time)

    @property
    def width(self):
        return self.end_time - self.start_time

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
        return (eq_float(lhs.start_time, rhs.start_time)
                and eq_float(lhs.end_time, rhs.end_time))

    # The next two overloads are mostly just a convenience for using bisect().
    def __le__(lhs, rhs):
        return lhs.end_time <= rhs.start_time + EPSILON

    def __lt__(lhs, rhs):
        return lhs.end_time < rhs.start_time + EPSILON

    def shift_phase(self, increment):
        self.start_time += increment
        self.end_time += increment

    @staticmethod
    def overlap(pulse1, pulse2):
        """Returns the overlap in units of time between two pulses. It is
        assumed that both pulses use the same units of time.
        """ 
        if (pulse1.start_time > pulse2.end_time):
            return 0.0
        if (pulse1.end_time < pulse2.start_time):
            return 0.0

        deduction_left = pulse2.start_time - pulse1.start_time
        deduction_right = pulse1.end_time - pulse2.end_time
        if deduction_left < 0.0:
            deduction_left = 0.0
        if deduction_right < 0.0:
            deduction_right = 0.0
        return pulse1.width - deduction_left - deduction_right

    @staticmethod
    def proportional_overlap(desired, other):
        """Returns the proportion of pulse1 overlapped by pulse 2.""" 
        overlap = Pulse.overlap(desired, other)
        return overlap/desired.width


class PulseTrain(object):
    """A sequence of discrete, rectangular pulses.

    Attributes:   
        duration: The duration of the train.
        pattern: A list containing the pulses that occur in a single PRI of the
            train.
        pulses: An iterable containing Pulse objects.
        pri: The pulse repetition interval of the train. More than one pulse may
            occur in a single PRI.
    """
    def __init__(self, pri, pulses, duration=None):
        """Constructs a pulse train.

        Arguments:   
            pri: The pulse repetition interval of the train. More than one pulse may
                occur in a single PRI.
            pulses: An iterable containing Pulse objects.
            duration: The duration of the train. If unspecified the 
                default duration is equal to the specified PRI.

        Raises:
            ValueError: Pulses in train cannot overlap.
        """
        self.pri = float(pri)
        if not duration == None:
            self.duration = float(duration)
        else:
            self.duration = float(pri)
        try:
            self.pattern = list(pulses)
            self._pulses = []
            for i in range(int(self.duration//self.pri)):
                for pulse in self.pattern:
                    start_time = pulse.start_time + i*pri
                    end_time = pulse.end_time + i*pri
                    self._pulses.append(Pulse(start_time, end_time))
        except TypeError:
            self.pattern = [pulses]
            self._pulses = []
            for i in range(int(self.duration//self.pri)):
                for pulse in self.pattern:
                    start_time = pulse.start_time + i*pri
                    end_time = pulse.end_time + i*pri
                    self._pulses.append(Pulse(start_time, end_time))
        for i in range(1, len(self.pattern)):
            if not self.pattern[i - 1] < self.pattern[i]:
                raise ValueError('Pulses in train cannot overlap.')

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
    def __eq__(lhs, rhs):
        if not len(lhs) == len(rhs):
            return False
        return all((lhs_pulse == rhs_pulse) 
                   for lhs_pulse, rhs_pulse in zip(lhs, rhs))

    def __iter__(self):
        return (pulse for pulse in self._pulses)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            # If a user wants to take a slice of the pulses, they should slice
            # the pattern and make a new train with the sublist.
            # return NotImplemented 
            print(self._pulses)
            return PulseTrain(self.pri, self._pulses[index], self.pri)
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
    def extend(self, pulse_train):
        """Identical to list.extend"""
        self._pulses.extend(pulse_train)

    def insert(self, index, pulse):
        """Similar to list.insert, but pulses must be ordered and not overlap
        after insertion.

            Raises:
                IndexError: Pulse must end before the pulse it is being inserted
                    before begins.
        """
        if pulse < self._pulses[index]:
            self._pulses.insert(index, pulse)
        else: 
            raise IndexError("""Pulse must end before the pulse it is being
                             inserted before begins.""")

    def clear(self):
        self._pulses.clear()

    def shift_phase(self, increment):
        """Shifts the phase of each pulse in the train.

        Moves the orientation of the pulse train in time by a specified increment.
        Guaranteed to keep the train "circular". That is, if a pulse shifts past
        the end of the train, a new pulse is inserted at the beginning
        representing the part of that same pulse stretching into the current 
        period of time by a pulse in the last PRI.
        
        Arguments:
            increment: The amount by which to shift the phase of the train.
        
        Returns:
            N/A
        
        Raises:
            N/A
        """
        if not len(self._pulses) == len(self.pattern) * int(self.duration//self.pri):
            # Concatenate the pulse that "stretches around" from the end to the 
            # beginning.
            self._pulses[-1].end_time += self._pulses[0].width
            self._pulses.remove(self._pulses[0])

        # Shift pulses to appropriate orientations
        for pulse in self._pulses:
            width = pulse.width
            pulse.start_time = (pulse.start_time + increment) % self.duration
            pulse.end_time = pulse.start_time + width

        # Make sure pulses are still in order from earliest to latest
        self._pulses.sort(key=lambda pulse: pulse.start_time)
        
        # Ensure that the pulse train is "circular".
        last_pulse = self._pulses[-1]
        overhang = last_pulse.end_time - self.duration

        # Is the last pulse hanging off the end?
        if overhang > 0 + EPSILON:
            # After the sort earlier, there should only be
            assert all(pulse.end_time < self.duration for pulse in self._pulses[:-1])
            if eq_float(self._pulses[0].end_time, overhang):
                # Lengthen first pulse, moving start time to zero
                self._pulses[0].start_time = 0
                # Chop the end of the last pulse
                last_pulse.end_time = self.duration 
            else:
                # Insert pulse with width equal to the length of the 
                # last pulse's overhang.
                assert(not overhang == 0)
                self._pulses.insert(0, Pulse(0, overhang))
                last_pulse.end_time -= overhang

    def to_vector(self):
        pass

    @staticmethod
    def coincidence_fraction(train1, train2, method='sim', increment=1, threshold=0):
        """Returns the coincidence fraction between two possibly asynchronous
        pulse trains.

        Computes the probability of overlap by pulses of pulse train on those of another
        during a given period of time. By default, the probability of any
        overlap, no matter how infinitesimally small is returned, but different
        thresholds of overlap can be specified by the user.
        
        Detail
        
        Argumenst:
            train1: The pulse train whose fraction is to be computed.
            train2: The 'overlapping' pulse train.
            method: The way to compute the fraction:
                        'sim' == computation by simulation
                        'formula' == computation by formula
            increment: The granularity of shifts in each simulation. The simulation
                is done by brute force, computing the overlap in a single orientation
                of the two trains, then shifting the overlapping train by the amount
                specified in increment. In general, the smaller the increment,
                the greater the precision (allowing of course for machine
                precision limitations and roundoff error).
            threshold: The proportion of an 'overlapped' pulse that must be
                overlapped in order to be counted as a coincident event.
        
        Returns:
            The probability of overlap between pulses of the two trains.

        Raises:
            ValueError: Pulse train durations must be equal.
        """


        # USE FSUM
        

        if not int(train1.duration) == int(train2.duration):
            raise ValueError('Pulse train durations must be equal.')
        for i in range(int(train1.duration/increment)):
            # Check overlaps
            tally_of_overlaps = 0
            for pulse1 in train1:
                # Search for the index of the pulse in train2 AFTER the
                # RIGHTMOST pulse less than pulse.
                index = bisect_left(train2, pulse1)
                for pulse2 in train2[index:]:
                    if (Pulse.proportional_overlap(pulse1, pulse2) > 
                        float(threshold) + EPSILON):
                        tally_of_overlaps += 1
                        break
        return tally / float(len(self.pulses()))


        # Sum overlaps
        # Shift
        return 1000 * (10 + 10)


        
        
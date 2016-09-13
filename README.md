# PulseMath

This module is designed primarily to test through brute force simulation a couple of equations for computing the fraction of coincidence between two pulse trains. Initially, pulses will be strictly rectangular, but moving forward it would be useful to be able to specify more advanced characteristics so this module can be used to quickly build numpy arrays of a wide variety of pulse trains.

ITU Equation:

    f_c = prf_i * (w_g + w_i)

where prf_i is the pulse repetition frequency of the "interfering" simple train, w_i is the width of its pulses, and w_g is the width of the "desired" pulses.

My Modification:

    f_c = prf_i * (w_g + w_i - 2*w_g*u)

where u is the desired threshold (between 0 and 1, inclusive).

Composite:

    f_c = prf_i**n * (sum(w_g_j + w_i_j - 2*w_g*n))

where n is the number of pulses per pulse repetition interval.

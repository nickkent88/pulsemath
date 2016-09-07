# PulseMath

This module is designed primarily to test through brute force simulation a couple of equations for computing the fraction of coincidence between two pulse trains. Initially, pulses will be strictly rectangular, but moving forward it would be useful to be able to specify more advanced characteristics so this module can be used to quickly build numpy arrays of a wide variety of pulse trains.

ITU Equation:

    f_c = prf_i * (w_g + w_i)

My Modification:

    f_c = prf_i * (w_g + w_i - 2*w_g*n)

Composite:

    f_c = prf_i * (sum(w_g_j + w_i_j - 2*w_g*n))
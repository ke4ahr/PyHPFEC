#
# Copyright (C) 2025 Kris Kirby
#
# This file is part of PyHPFEC.
#
# PyHPFEC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with PyHPFEC. If not, see <http://www.gnu.org/licenses/>.
#

import numpy as np
from numba import njit, float64, uint8

# --- Numba JIT-Compiled LLR Utilities ---

@njit(uint8[:](float64[:]), cache=True)
def llr_to_hard_bits(llrs: np.ndarray) -> np.ndarray:
    """
    Converts LLRs to hard decisions (0 or 1).
    LLR > 0 -> Bit 0 (more likely to be +1 symbol, which maps to bit 0)
    LLR < 0 -> Bit 1 (more likely to be -1 symbol, which maps to bit 1)
    """
    # Equivalent to (llrs < 0).astype(np.uint8)
    hard_bits = np.empty_like(llrs, dtype=uint8)
    for i in range(len(llrs)):
        if llrs[i] < 0.0:
            hard_bits[i] = 1
        else:
            hard_bits[i] = 0
    return hard_bits

@njit(float64(float64, float64), cache=True)
def log_map_approx(L_a: float, L_b: float) -> float:
    """
    Calculates log(e^La + e^Lb) using the Log-MAP approximation (often called Min-Sum).
    
    Formula: log(e^La + e^Lb) = max(La, Lb) + log(1 + e^(-|La - Lb|))
    The Min-Sum approximation is: min(|La|, |Lb|)
    """
    # Min-Sum Approximation (used in LDPC/Turbo Check Node Update for simplification)
    abs_sum = np.abs(L_a + L_b)
    abs_diff = np.abs(L_a - L_b)
    
    # This is the exact Log-MAP calculation (requires look-up table or function for the correction term)
    # The actual Min-Sum approximation is simply: np.sign(L_a) * np.sign(L_b) * np.min(np.abs(L_a), np.abs(L_b))
    
    # Using the standard approximate form (Min-Sum with sign):
    L_out = np.sign(L_a) * np.sign(L_b) * np.min(np.abs(L_a), np.abs(L_b))
    
    # Note: For high-performance, the correction term is often omitted, making the result the Min-Sum.
    # We will return the result of the signs multiplied by the minimum of the magnitudes.
    return L_out

# --- Class implementation is omitted as this file only contains utility functions ---


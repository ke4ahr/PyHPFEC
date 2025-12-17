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
from numba import njit

# --- Numba JIT-Compiled Rate Matching Kernels ---

@njit
def _numba_puncturing(codeword: np.ndarray, puncturing_pattern: np.ndarray) -> np.ndarray:
    """
    Removes bits from the codeword according to a binary pattern (1=keep, 0=remove).
    The pattern is usually repeated cyclically.
    """
    codeword_len = len(codeword)
    pattern_len = len(puncturing_pattern)
    
    # Estimate max size for pre-allocation
    max_output_len = codeword_len 
    punctured_codeword = np.empty(max_output_len, dtype=codeword.dtype)
    
    idx = 0
    for i in range(codeword_len):
        if puncturing_pattern[i % pattern_len] == 1:
            punctured_codeword[idx] = codeword[i]
            idx += 1
            
    return punctured_codeword[:idx] # Return the trimmed array

@njit
def _numba_depuncturing(received_llrs: np.ndarray, puncturing_pattern: np.ndarray, N: int, LLR_null: float = 0.0) -> np.ndarray:
    """
    Inserts dummy LLRs (usually 0.0) back into the received LLR sequence 
    where bits were punctured.
    
    :param N: The original length of the unpunctured codeword.
    :param LLR_null: The LLR value used for punctured bits (0.0 means equal probability).
    """
    received_len = len(received_llrs)
    pattern_len = len(puncturing_pattern)
    
    depunctured_llrs = np.full(N, LLR_null, dtype=received_llrs.dtype)
    
    rx_idx = 0
    for i in range(N):
        if puncturing_pattern[i % pattern_len] == 1:
            # This index was transmitted
            if rx_idx < received_len:
                depunctured_llrs[i] = received_llrs[rx_idx]
                rx_idx += 1
            # else: Should not happen if inputs are sized correctly
            
    return depunctured_llrs

# --- Rate Matcher Class ---

class RateMatcher:
    """
    Handles puncturing and depuncturing based on a predefined pattern.
    """
    
    def __init__(self, code_rate: float, original_N: int, target_N: int, puncturing_pattern: np.ndarray):
        """
        :param puncturing_pattern: Binary array (1=keep, 0=remove).
        """
        self.original_N = original_N
        self.target_N = target_N
        self.puncturing_pattern = puncturing_pattern

    def puncture(self, codeword: np.ndarray) -> np.ndarray:
        """Applies puncturing."""
        return _numba_puncturing(codeword, self.puncturing_pattern)

    def depuncture(self, received_llrs: np.ndarray) -> np.ndarray:
        """Applies depuncturing, inserting 0 LLRs for punctured positions."""
        # Note: target_N is the length of the *unpunctured* codeword, which is the output size.
        return _numba_depuncturing(received_llrs, self.puncturing_pattern, self.original_N)


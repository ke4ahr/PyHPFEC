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

# --- Numba JIT-Compiled Kernels ---

@njit(float64[:](uint8[:]), cache=True)
def _numba_bpsk_modulate(bits: np.ndarray) -> np.ndarray:
    """BPSK modulation: maps bit 0 -> +1.0, bit 1 -> -1.0."""
    return 1.0 - 2.0 * bits

@njit(float64[:](float64[:], float64), cache=True)
def _numba_bpsk_demodulate_llr(rx_symbols: np.ndarray, noise_variance: float) -> np.ndarray:
    """
    BPSK Demodulation: Calculates LLRs for AWGN channel.
    
    LLR(b=0|y) = log(P(b=0|y) / P(b=1|y))
    For AWGN: LLR approx (2 * y) / (sigma^2)
    Assuming E_b = 1.0 (since symbol energy is 1.0), sigma^2 = N0/2.
    LLR approx (4 * E_b / N0) * y = (2 / sigma^2) * y
    """
    # Assuming symbol energy is 1.0, N0 = noise_variance * 2
    # LLR = (4 * E_b / N0) * y. Here, 4/N0 = 2/sigma^2.
    
    # If noise_variance (sigma^2) is 0, set to small epsilon to prevent division by zero.
    if noise_variance == 0.0:
        return 1e10 * rx_symbols # Very confident decision
        
    return (2.0 / noise_variance) * rx_symbols


# --- BPSK Modulator/Demodulator ---

class BPSKUnguided:
    """
    Binary Phase-Shift Keying (BPSK) Modulation and Demodulation.
    Assumes unguided detection (channel state information is perfect/known).
    """
    
    def modulate(self, bits: np.ndarray) -> np.ndarray:
        """
        Modulates input bits (0/1) to real symbols (+1/-1).
        """
        return _numba_bpsk_modulate(bits)

    def demodulate(self, rx_symbols: np.ndarray, noise_variance: float = 1.0) -> np.ndarray:
        """
        Demodulates received symbols to LLRs.
        
        :param rx_symbols: Received real symbols.
        :param noise_variance: Noise variance (sigma^2) of the AWGN channel.
        :returns: LLRs.
        """
        return _numba_bpsk_demodulate_llr(rx_symbols, noise_variance)

# --- QPSK Modulator/Demodulator (Placeholder) ---

class QPSKUnguided:
    """
    Quadrature Phase-Shift Keying (QPSK) Modulator and Demodulator.
    """
    
    def modulate(self, bits: np.ndarray) -> np.ndarray:
        """Modulates pairs of bits to complex symbols."""
        # Placeholder for QPSK logic
        return np.zeros(len(bits) // 2, dtype=np.complex128)

    def demodulate(self, rx_symbols: np.ndarray, noise_variance: float = 1.0) -> np.ndarray:
        """Demodulates complex symbols to LLRs (size 2 * len(rx_symbols))."""
        # Placeholder for QPSK LLR calculation
        return np.zeros(len(rx_symbols) * 2, dtype=np.float64)


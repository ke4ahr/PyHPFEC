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
# PyHPFEC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyHPFEC. If not, see <http://www.gnu.org/licenses/>.
#

import numpy as np
from numba import njit, int32, uint8

# --- Numba JIT-Compiled GF Arithmetic Functions ---

@njit(int32(int32, int32, uint8[:], uint8[:], int32), cache=True)
def gf_multiply(a: int, b: int, log_table: np.ndarray, anti_log_table: np.ndarray, M: int) -> int:
    """
    Performs GF(2^M) multiplication using Log/Anti-Log tables.
    The tables MUST be pre-calculated and passed from GFContext.
    """
    if a == 0 or b == 0:
        return 0
    
    # Indices are based on non-zero elements (alpha^index)
    log_a = log_table[a]
    log_b = log_table[b]
    
    # Exponent addition (modulo Q-1, where Q-1 = 2^M - 1)
    # The modulus is 2^M - 1. We use (1 << M) - 1.
    result_idx = (log_a + log_b) % ((1 << M) - 1)
    
    return anti_log_table[result_idx]

@njit(int32(int32, uint8[:]), cache=True)
def gf_inverse(a: int, inv_table: np.ndarray) -> int:
    """
    Performs GF(2^M) inverse using a pre-calculated inverse table.
    """
    if a == 0:
        return 0 # No inverse for zero
    return inv_table[a]

# --- GF Context Class ---

class GFContext:
    """
    Galois Field Context. Pre-calculates Log, Anti-Log, and Inverse tables
    for GF(2^M) to enable high-speed, thread-safe arithmetic.
    
    M must be <= 16 due to table size limits.
    """
    
    def __init__(self, M: int, P_poly: int = None):
        """
        Initializes the GF(2^M) context.
        
        :param M: The power of the field (2^M).
        :param P_poly: The primitive polynomial value (optional, uses standard if None).
        """
        if not 2 <= M <= 16:
            raise ValueError("M must be between 2 and 16.")
            
        self.M = M
        self.Q = 1 << M # Q = 2^M
        
        # Determine the primitive polynomial if not specified
        if P_poly is None:
            # Standard primitive polynomials (often used in communication standards)
            # Example: GF(16) uses x^4 + x + 1 (binary 10011, value 19)
            # This list should be defined and verified for all supported M.
            standard_polys = {
                4: 0b10011,  # x^4 + x + 1
                6: 0b1000011, # x^6 + x + 1
                8: 0b100011101, # x^8 + x^4 + x^3 + x^2 + 1 (standard)
            }
            if M not in standard_polys:
                raise NotImplementedError(f"Standard primitive polynomial for M={M} not defined.")
            self.P_poly = standard_polys[M]
        else:
            self.P_poly = P_poly
            
        self._build_tables()

    def _build_tables(self):
        """
        Builds the Log, Anti-Log, and Inverse tables for the defined GF(2^M).
        """
        Q_minus_1 = self.Q - 1
        
        # Initialize tables
        self.anti_log_table = np.zeros(self.Q, dtype=uint8)
        self.log_table = np.zeros(self.Q, dtype=uint8)
        self.inv_table = np.zeros(self.Q, dtype=uint8)
        
        # Galois Field element alpha^i (current field element)
        alpha_i = 1 
        
        # --- Main Table Generation Loop ---
        for i in range(Q_minus_1):
            if alpha_i >= self.Q:
                # This should not happen if the polynomial is primitive.
                raise RuntimeError("Polynomial is not primitive or table overflow.")

            # Map the power (i) to the element (alpha_i)
            self.anti_log_table[i] = alpha_i
            # Map the element (alpha_i) to the power (i)
            self.log_table[alpha_i] = i
            
            # Calculate the next element: alpha^(i+1) = alpha^i * alpha
            # This is done by left shift (multiplication by x)
            alpha_i <<= 1
            
            # Reduction: If the high bit is set (overflow beyond Q-1), 
            # XOR with the primitive polynomial P(x).
            if alpha_i & self.Q:
                alpha_i ^= self.P_poly
                
        # Handle zero element
        self.log_table[0] = Q_minus_1 # Log(0) is undefined, use Q-1 as sentinel
        
        # --- Inverse Table Generation ---
        # The inverse of alpha^i is alpha^(Q-1 - i)
        for i in range(1, self.Q):
            inv_power = (Q_minus_1 - self.log_table[i]) % Q_minus_1
            self.inv_table[i] = self.anti_log_table[inv_power]


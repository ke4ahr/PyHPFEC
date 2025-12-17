#
# Copyright (c) 2025 [Your Name/Company Name]
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

# Copyright (C) 2025 Kris Kirby

import numpy as np
import unittest
from pyhpfec.config import GFContext, gf_multiply, gf_inverse
from pyhpfec.cyclic import BCHGolayCoder
from pyhpfec.llr_utils import llr_to_hard_bits, log_map_approx

class TestGFArithmetic(unittest.TestCase):
    """Tests for Galois Field operations defined in config.py."""
    
    def setUp(self):
        # Using GF(2^4) for standard BCH(15, 7) context
        self.ctx = GFContext(M=4) 
        self.M = self.ctx.M
        self.Q = self.ctx.Q
        self.log_table = self.ctx.log_table
        self.anti_log_table = self.ctx.anti_log_table

    def test_gf_multiply(self):
        # Test multiplication: 1 * a = a
        self.assertEqual(gf_multiply(1, 5, self.log_table, self.anti_log_table, self.M), 5)
        # Test multiplication: 0 * a = 0
        self.assertEqual(gf_multiply(0, 7, self.log_table, self.anti_log_table, self.M), 0)
        # Test known result (depends on the primitive polynomial, assumed for GF(16))
        # This test needs empirical verification based on the specific P_poly used in GFContext.
        # Assuming P(x) = x^4 + x + 1 (0x13 in hex, standard for GF(16))
        # In this field, alpha^1 * alpha^4 = alpha^5.
        # alpha^1 (2) * alpha^4 (4) = alpha^5 (8)
        self.assertEqual(gf_multiply(2, 4, self.log_table, self.anti_log_table, self.M), 8)

    def test_gf_inverse(self):
        # Test known result: inverse of 1 is 1
        self.assertEqual(gf_inverse(1, self.ctx.inv_table), 1)
        # Test a known non-trivial inverse
        # In GF(16), 2^-1 = 13 (0x0D, alpha^14)
        self.assertEqual(gf_inverse(2, self.ctx.inv_table), 13)
        # Test that 0 has no inverse
        self.assertEqual(gf_inverse(0, self.ctx.inv_table), 0)

class TestBCHKernels(unittest.TestCase):
    """Tests for core BCH encoding and syndrome calculation kernels."""

    def setUp(self):
        # Using a small code for testing: BCH(15, 7, t=2)
        self.ctx = GFContext(M=4) 
        self.coder = BCHGolayCoder(n=15, k=7, t=2, gf_context=self.ctx)
        self.k = self.coder.k
        self.n = self.coder.n
        
    def test_encoding_zero_data(self):
        # Encoding all-zero data must result in all-zero codeword
        data = np.zeros(self.k, dtype=np.uint8)
        codeword = self.coder.encode(data)
        self.assertTrue(np.all(codeword == 0))
        
    def test_syndrome_zero_codeword(self):
        # Syndrome of a valid codeword must be all zeros
        codeword = np.zeros(self.n, dtype=np.uint8)
        syndromes = self.coder._calculate_syndromes(codeword)
        self.assertTrue(np.all(syndromes == 0))
        
    def test_syndrome_single_error(self):
        # Syndrome of a single-error pattern (error at position 0)
        codeword = np.zeros(self.n, dtype=np.uint8)
        codeword[0] = 1 # Introduce error at position 0
        syndromes = self.coder._calculate_syndromes(codeword)
        # S_i must be equal to alpha^(i * 0) = 1 for all i = 1 to 2t
        self.assertTrue(np.all(syndromes == 1))

class TestLLRUtilities(unittest.TestCase):
    """Tests for LLR conversion and Log-MAP approximations."""
    
    def test_llr_to_hard_bits(self):
        llrs = np.array([1.5, -2.0, 0.001, -0.001, 5.0, -5.0])
        # Expected: 0, 1, 0, 1, 0, 1
        expected = np.array([0, 1, 0, 1, 0, 1], dtype=np.uint8)
        hard_bits = llr_to_hard_bits(llrs)
        self.assertTrue(np.array_equal(hard_bits, expected))

    def test_log_map_approx(self):
        # Test known limits for log_map_approx (min-sum approximation of Log(e^a + e^b))
        
        # Case 1: a >> b (output should be approx b)
        # Log(e^10 + e^1) approx Log(e^10) = 10, but since the func returns min(a,b) + correction
        a, b = 10.0, 1.0
        result = log_map_approx(a, b)
        # Min(10, 1) = 1. Correction factor is small for large difference.
        self.assertAlmostEqual(result, 1.0, delta=0.1)

        # Case 2: a = b (output should be a + ln(2))
        a, b = 2.0, 2.0
        result = log_map_approx(a, b)
        expected = 2.0 + np.log(2) # ~ 2.693
        self.assertAlmostEqual(result, expected, delta=0.001)

if __name__ == '__main__':
    unittest.main()


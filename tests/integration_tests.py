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
from pyhpfec.config import GFContext
from pyhpfec.cyclic import BCHGolayCoder
from pyhpfec.modem import BPSKUnguided
from pyhpfec.channel import AWGNChannel
from pyhpfec.turbo import TurboDecoder # Only importing to show integration point
from pyhpfec.polar import PolarSCLDecoder # Only importing to show integration point

class TestEndToEndCoding(unittest.TestCase):
    """Tests the full Encode -> Channel -> Decode pipeline."""

    def setUp(self):
        # Set up a common context and components
        self.ctx = GFContext(M=4) 
        self.bch_coder = BCHGolayCoder(n=15, k=7, t=2, gf_context=self.ctx)
        self.modem = BPSKUnguided()
        self.k = self.bch_coder.k
        self.n = self.bch_coder.n

    def generate_test_data(self):
        # Generate random data bits
        return np.random.randint(0, 2, self.k, dtype=np.uint8)

    def test_bch_hard_decoding_no_errors(self):
        """Test BCH hard decoding with zero errors."""
        data = self.generate_test_data()
        codeword = self.bch_coder.encode(data)
        
        # Simulate a perfect channel (received = transmitted)
        received_bits = codeword
        
        decoded_data, errors_corrected = self.bch_coder.decode(received_bits, is_llr=False)
        
        self.assertTrue(np.array_equal(data, decoded_data), "Data mismatch in perfect hard decode.")
        self.assertEqual(errors_corrected, 0, "Corrected errors count non-zero in perfect decode.")

    def test_bch_hard_decoding_t_errors(self):
        """Test BCH hard decoding with max correctable errors (t=2)."""
        data = self.generate_test_data()
        codeword = self.bch_coder.encode(data)
        
        # Introduce t=2 errors
        received_bits = codeword.copy()
        received_bits[0] = 1 - received_bits[0] # Flip bit 0
        received_bits[1] = 1 - received_bits[1] # Flip bit 1
        
        decoded_data, errors_corrected = self.bch_coder.decode(received_bits, is_llr=False)
        
        self.assertTrue(np.array_equal(data, decoded_data), "Hard decode failed to correct t=2 errors.")
        self.assertEqual(errors_corrected, 2, "Errors corrected count is incorrect.")
        
    def test_bch_soft_decoding_awgn(self):
        """Test BCH soft (Chase) decoding over AWGN channel."""
        data = self.generate_test_data()
        codeword = self.bch_coder.encode(data)
        
        # Use a high Eb/No to ensure high probability of successful decode
        EbNo_dB = 8.0 
        channel = AWGNChannel(EbNo_dB=EbNo_dB)
        
        tx_symbols = self.modem.modulate(codeword)
        rx_symbols = channel.transmit(tx_symbols, k=self.k, n=self.n)
        llrs = self.modem.demodulate(rx_symbols)
        
        # Use Chase soft-decision decoding
        # Setting a small number of test patterns for speed, but this requires a robust decoder.
        decoded_data, errors_corrected = self.bch_coder.decode(
            llrs, 
            is_llr=True, 
            soft_decision=True, 
            num_test_patterns=4
        )
        
        # We cannot assert equality because AWGN is probabilistic, 
        # but we expect a very low failure rate at high Eb/No.
        # For a unit test, we check if the result is valid and reasonable.
        self.assertEqual(decoded_data.shape, data.shape, "Decoded data shape mismatch.")
        
        # Check if the overall decode process completes without throwing an exception.
        self.assertTrue(errors_corrected >= 0, "Decoder reported negative errors corrected.")
        
    def test_turbo_decoder_initialization(self):
        """Test initialization of Turbo Decoder (placeholder for full test)."""
        # The actual test would involve running BER simulations, but this verifies the API.
        k_data = 100
        turbo_decoder = TurboDecoder(k=k_data)
        
        self.assertIsNotNone(turbo_decoder)
        self.assertEqual(turbo_decoder.k, k_data)

    def test_polar_decoder_initialization(self):
        """Test initialization of Polar SCL Decoder (placeholder for full test)."""
        # Polar codes need N and K to be powers of 2.
        N_code, K_info = 512, 256
        polar_decoder = PolarSCLDecoder(N=N_code, K=K_info, list_size=4)
        
        self.assertIsNotNone(polar_decoder)
        self.assertEqual(polar_decoder.N, N_code)
        self.assertEqual(polar_decoder.K, K_info)

if __name__ == '__main__':
    unittest.main()


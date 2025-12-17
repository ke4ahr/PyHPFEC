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

class AWGNChannel:
    """
    Additive White Gaussian Noise (AWGN) Channel Model.
    Calculates noise variance based on Eb/No ratio.
    """
    
    def __init__(self, EbNo_dB: float):
        """
        :param EbNo_dB: Energy per bit to Noise Power Spectral Density ratio in dB.
        """
        self.EbNo_dB = EbNo_dB
        self.EbNo = 10**(EbNo_dB / 10.0)

    def _calculate_noise_power(self, R: float) -> float:
        """
        Calculates the required noise power spectral density (N0) or variance (sigma^2).
        
        Relationships:
        1. E_b/N0 = (E_s / R) / N0
        2. E_s (Symbol Energy) is often normalized to 1.0.
        3. If E_s = 1, then E_b/N0 = 1 / (R * N0).
        4. N0 = 1 / (R * E_b/N0).
        5. Noise Variance (sigma^2) = N0 / 2 (for real-valued symbols).
        """
        # Assuming symbol energy E_s = 1.0 (standard normalization)
        
        # N0
        N0 = 1.0 / (R * self.EbNo)
        
        # Noise variance (sigma^2) for the real-valued AWGN channel
        sigma_sq = N0 / 2.0
        
        return sigma_sq

    def transmit(self, tx_symbols: np.ndarray, k: int, n: int) -> np.ndarray:
        """
        Adds Gaussian noise to transmitted symbols.
        
        :param tx_symbols: Transmitted symbols (+1/-1).
        :param k: Number of information bits.
        :param n: Number of coded bits (codeword length).
        :returns: Received symbols (tx_symbols + noise).
        """
        if k <= 0 or n <= 0:
            raise ValueError("k and n must be positive.")
            
        # Calculate code rate
        R = k / n
        
        # Calculate noise variance (sigma^2)
        sigma_sq = self._calculate_noise_power(R)
        
        # Generate Gaussian noise (mean 0, variance sigma^2)
        noise_std_dev = np.sqrt(sigma_sq)
        noise = np.random.normal(0.0, noise_std_dev, tx_symbols.shape)
        
        # Received symbols
        rx_symbols = tx_symbols + noise
        
        # Attach noise variance to symbols for accurate LLR demodulation
        rx_symbols.noise_variance = sigma_sq
        return rx_symbols


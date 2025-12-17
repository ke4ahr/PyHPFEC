# PyHPFEC: High-Performance Forward Error Correction Library

PyHPFEC is a comprehensive, Numba-optimized Python library for advanced coding theory,
focused on high-speed algebraic and iterative decoding. It is designed for reliability
in multi-threaded environments through a unique thread-safe architecture.

## 🚀 Key Features

* **Thread-Safe Architecture:** Uses the `GFContext` object to manage Galois Field arithmetic and look-up tables. This architecture ensures that concurrent decoding operations (common in multi-core environments) are safe and efficient. 
* **High Performance:** Critical decoding kernels (e.g., Log-MAP, Berlekamp-Massey, SCL) are accelerated using Numba JIT compilation, providing near C/Fortran performance.
* **Comprehensive Code Support:** Includes optimized implementations of:
    * **Algebraic Codes:** BCH (with Chase Soft-Decision decoding), Hamming.
    * **Iterative Codes:** Turbo, Polar (Successive Cancellation List - SCL), and LDPC.
* **Soft-Decision Decoding:** Supports the advanced Chase Algorithm 2 for BCH codes and native $\text{LLR}$-based iterative decoding for all other codes.

## 📝 Installation

```bash
# Recommended installation for PyPI release
pip install pyhpfec


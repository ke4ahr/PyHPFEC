.. pyhpfec documentation master file.

PyHPFEC: High-Performance Forward Error Correction
==================================================

PyHPFEC is a comprehensive, Numba-optimized Python library for advanced coding theory,
focused on high-speed algebraic and iterative decoding. It is designed for reliability
in multi-threaded environments through a unique thread-safe configuration architecture.

.. note::
   This library implements state-of-the-art algorithms including Berlekamp-Massey, 
   Sum-Product, Successive Cancellation List (SCL), and Chase soft-decision decoding.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Architecture Overview <architecture>
   API Reference <api/index>
   Installation <install>

Architecture Overview
---------------------
The core difference in PyHPFEC is the use of the :py:class:`~pyhpfec.config.GFContext`
object to manage Galois Field arithmetic parameters and lookup tables. This ensures 
that all decoding operations are thread-safe and utilize the fastest possible 
Log/Anti-Log table methods. 

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


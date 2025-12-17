.. automodule:: pyhpfec.config

Galois Field Configuration (config)
===================================

The ``config`` module manages the environment for all Galois Field (GF) dependent codes 
(BCH, NB-LDPC). The core structure is the thread-safe :py:class:`~pyhpfec.config.GFContext`.

.. autoclass:: pyhpfec.config.GFContext
   :members: M, Q, P_poly, inv_table, log_table, anti_log_table
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__

   .. rubric:: Example Usage (Thread-Safe Initialization)

   .. code-block:: python

      from pyhpfec.config import GFContext

      # Create a context for GF(2^6)
      ctx_6 = GFContext(M=6)
      
      # The context holds all tables and parameters internally
      print(f"Field Size: {ctx_6.Q}") # Output: 64

.. rubric:: Core Numba Arithmetic

These functions are Numba-JIT compiled and require the GF parameters to be passed 
explicitly from a :py:class:`~pyhpfec.config.GFContext` instance.

.. autofunction:: pyhpfec.config.gf_multiply
   :noindex:
   
.. autofunction:: pyhpfec.config.gf_inverse
   :noindex:


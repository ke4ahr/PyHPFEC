.. automodule:: pyhpfec.cyclic

Cyclic Codes: BCH and Hamming
=============================

This module contains the optimized implementations of algebraic codes.

.. autoclass:: pyhpfec.cyclic.BCHGolayCoder
   :members: encode, decode
   :undoc-members:
   :show-inheritance:
   
   .. automethod:: __init__

   .. rubric:: Decoding Modes

   The :py:meth:`~pyhpfec.cyclic.BCHGolayCoder.decode` method supports two modes:

   1. **Algebraic (Hard-Decision):** Default mode when ``soft_decision=False``. This corrects up to *t* errors perfectly, but ignores channel reliability.
   
   2. **Chase (Soft-Decision):** Enabled by setting ``soft_decision=True``. This uses the Maximum Likelihood (ML) metric based on received LLRs, achieving significantly better performance near the correction boundary by testing low-reliability bits. 

   .. rubric:: Example Usage (Chase Soft-Decision)

   .. code-block:: python

      from pyhpfec.cyclic import BCHGolayCoder
      from pyhpfec.config import GFContext
      import numpy as np
      
      ctx = GFContext(M=4)
      coder = BCHGolayCoder(n=15, k=7, t=2, gf_context=ctx)
      
      # LLR input array (Example: one bit is unreliable/close to zero)
      received_llrs = np.array([5.0, -0.5, 5.0, 5.0, -5.0, ...]) 
      
      # Decode using soft-decision, testing a small number of patterns
      decoded_data = coder.decode(received_llrs, is_llr=True, soft_decision=True, num_test_patterns=4)
      
      # ...

.. autoclass:: pyhpfec.cyclic.HammingEncoder
   :members: encode
   :undoc-members:

.. autoclass:: pyhpfec.cyclic.HammingDecoder
   :members: decode
   :undoc-members:


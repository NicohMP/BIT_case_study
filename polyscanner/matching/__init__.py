"""Signal-family matching (Step 3).

Implements a 2-stage matcher:
1) Discovery (high recall): lexical + optional embeddings
2) Classification (high precision): deterministic gated rules
"""


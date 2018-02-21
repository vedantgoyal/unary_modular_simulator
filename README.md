Unary bit-streams, like stochastic bit-streams, use equally weighted bits to perform computation but do not require randomness to perform logic. This representation, while not compact like binary, is useful because it can lead to extremely low complexity
circuits and added benefits like fault tolerance. I designed methods to do arithmetic operations,multiplicative inverse and gaussian elimination in modular unary. The paper demonstrated designs for logic circuits with much lower complexity compared to those used conventionally.

This program creates a simulation for modular unary circuits.

connector.py : defines basic connectors between components
basic_blocks.py : defines basic logic gates
advanced_components : Addes simulations for more advanced circuits
testers.py : Defines tests to check all blocks and run simulations

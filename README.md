## ChaCha permutation on ARM M-series

The purpose of this repository is to make the ChaCha implementation presented in [1] more easily available, and to present benchmarks for other round numbers. When referring to this implementation, please refer to the canonical white-paper source in which the original ChaCha12 version was published:

> [1] Andreas Hülsing, Joost Rijneveld, and Peter Schwabe. ARMed SPHINCS – Computing a 41 KB signature in 16 KB of RAM. _Public-Key Cryptography – PKC 2016_, LNCS 9614, pp. 446-470, Springer, 2016.

## Compiling

TODO: explain compilation steps, including getting libopencm3

## Measuring

TODO: explain setup with STM32 board (pin connections, ttyUSB0)

TODO: explain how to run the measurements using Pyserial

## Benchmarks

TODO: include benchmarks for Cortex M3 and M4, for ChaCha{8, 12, 20}

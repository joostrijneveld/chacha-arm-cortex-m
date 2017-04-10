# ChaCha permutation on ARM Cortex-M3 and Cortex-M4

The purpose of this repository is to make the ChaCha implementation presented in [1] more easily available, and to present benchmarks for other round numbers. When referring to this implementation, please refer to the paper in which it was originally published:

> [1] Andreas Hülsing, Joost Rijneveld, and Peter Schwabe. ARMed SPHINCS – Computing a 41 KB signature in 16 KB of RAM. _Public-Key Cryptography – PKC 2016_, LNCS 9614, pp. 446-470, Springer, 2016. https://joostrijneveld.nl/papers/armedsphincs/

Note that this code only concerns the ChaCha permutation (i.e. the composition of quadrounds), and not the full ChaCha stream cipher. The latter would require some additional administration for the key and nonce, as well as adding the keystream to plaintext.

## Compiling

Summarizing, compiling the code comes down to the following command sequence;

```
git submodule update --init
cd m4
make lib
make
```

This project relies on the [arm-none-eabi toolchain](https://launchpad.net/gcc-arm-embedded) and the [libopencm3](https://github.com/libopencm3/libopencm3/) firmware. See [this repository](https://github.com/joostrijneveld/STM32-getting-started) for some more detailed setup instructions and troubleshooting hints. Assuming the before-mentioned is installed, compiling benchmarking binaries can be done by calling e.g. `make measure_chacha12.bin` in the `m3` or `m4` directories. This also generates the assembly implementation as an intermediate result. In order to be able to use the host-side Python script to display the output, make sure the [pyserial](https://github.com/pyserial/pyserial) package is installed.

## Measuring

Connect an USB-to-serial connector (such as the popular PL2303) to `/dev/ttyUSB0`. The code assumes `TX` is connect to `PA3` and `RX` is connected to `PA2`. Run the host-side script `unidirectional.py` to display the output that is received over the serial connection. To flash the binary onto the board using [stlink](https://github.com/texane/stlink): `st-flash write measure_chacha12.bin 0x8000000`.

## Benchmarks

Running the above produces the following cycle counts for a single ChaCha permutation. Recall that such a permutation processes 64 bytes of input to produce 64 bytes of output. ROM usage is measured by inspecting the memory footprint of the `chacha{8,12,20}_perm_asm` function in an object dump.

|            | Cortex-M3 (STM32L100C), cycles | Cortex-M4 (STM32F407), cycles | ROM usage, bytes
| ---------: | :----------------------------: | :---------------------------: | :--------------:
|  π-ChaCha8 |               390              |              414              |       1188
| π-ChaCha12 |               542              |              572              |       1748
| π-ChaCha20 |               846              |              888              |       2868

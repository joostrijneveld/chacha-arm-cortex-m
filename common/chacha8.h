#ifndef CHACHA8_H
#define CHACHA8_H

#define ROUNDS "8"
#define CHACHA_PERMUTATION chacha8_perm_asm

extern void chacha8_perm_asm(unsigned char* out, const unsigned char* in);

#endif

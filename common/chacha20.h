#ifndef CHACHA20_H
#define CHACHA20_H

#define ROUNDS "20"
#define CHACHA_PERMUTATION chacha20_perm_asm

extern void chacha20_perm_asm(unsigned char* out, const unsigned char* in);

#endif

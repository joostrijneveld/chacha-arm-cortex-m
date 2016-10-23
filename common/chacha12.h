#ifndef CHACHA12_H
#define CHACHA12_H

#define ROUNDS "12"
#define CHACHA_PERMUTATION chacha12_perm_asm

extern void chacha12_perm_asm(unsigned char* out, const unsigned char* in);

#endif

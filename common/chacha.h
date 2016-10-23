#ifndef CHACHA_H
#define CHACHA_H

#define u8 uint8_t
#define u32 uint32_t

#define U8V(v) ((u8)(v) & 0xFF)
#define U32V(v) ((u32)(v) & 0xFFFFFFFF)
#define U8TO32_LITTLE(p)   \
        (((u32)((p)[0])      ) | ((u32)((p)[1]) <<  8) | \
         ((u32)((p)[2]) << 16) | ((u32)((p)[3]) << 24)   )
#define U32TO8_LITTLE(p, v) \
  do { \
    (p)[0] = U8V((v)      ); \
    (p)[1] = U8V((v) >>  8); \
    (p)[2] = U8V((v) >> 16); \
    (p)[3] = U8V((v) >> 24); \
  } while (0)

void ECRYPT_keysetup(u32 *input, const u8 *k, u32 kbits, u32 ivbits);
void ECRYPT_ivsetup(u32 *input, const u8 *iv);
void ECRYPT_encrypt_bytes(u32 *input, const u8 *m, u8 *c, u32 bytes);
void ECRYPT_decrypt_bytes(u32 *x, const u8 *c, u8 *m, u32 bytes);
void ECRYPT_keystream_bytes(u32 *x, u8 *stream, u32 bytes);

#endif
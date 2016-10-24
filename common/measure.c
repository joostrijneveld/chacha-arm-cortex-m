#include <stdio.h>
#include "../common/stm32wrapper.h"

int main(void)
{
    unsigned char data[64];
    unsigned char digest[64];
    char output[128];
    unsigned int oldcount, newcount;
    int i;

    clock_setup();
    gpio_setup();
    usart_setup(921600);

    SCS_DEMCR |= SCS_DEMCR_TRCENA;
    DWT_CYCCNT = 0;
    DWT_CTRL |= DWT_CTRL_CYCCNTENA;

    for(i=0; i<64; i++) {
        data[i] = i;
    }

    sprintf(output, "Benchmarking ChaCha"ROUNDS"..");
    send_USART_str(output);

    oldcount = DWT_CYCCNT;
    CHACHA_PERMUTATION(digest, data);
    newcount = DWT_CYCCNT-oldcount;

    for(i=0; i < 64; i++) {
       sprintf(output + 2*i, "%02X", digest[i]);
    }
    send_USART_bytes((unsigned char *)output, 128);
    sprintf(output, "\nChaCha"ROUNDS" cost: %d", newcount);
    send_USART_str(output);

    while(1);
    return 0;
}

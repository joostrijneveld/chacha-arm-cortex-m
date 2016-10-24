# This file contains common Makefile content for all platforms;
# it is referenced from the individual Makefiles

ifneq (,$(findstring chacha8,$(MAKECMDGOALS)))
	OBJS += ../common/chacha8.s
else ifneq (,$(findstring chacha12,$(MAKECMDGOALS)))
	OBJS += ../common/chacha12.s
else
	OBJS += ../common/chacha20.s
endif

PREFIX	?= arm-none-eabi
CC		= $(PREFIX)-gcc
LD		= $(PREFIX)-gcc
OBJCOPY	= $(PREFIX)-objcopy
OBJDUMP	= $(PREFIX)-objdump
GDB		= $(PREFIX)-gdb
OPENCM3_DIR = ../libopencm3

CFLAGS		+= -O3 \
		   -Wall -Wextra -Wimplicit-function-declaration \
		   -Wredundant-decls -Wmissing-prototypes -Wstrict-prototypes \
		   -Wundef -Wshadow \
		   -I$(OPENCM3_DIR)/include \
		   -fno-common $(ARCH_FLAGS) -MD $(DEFINES)
LDFLAGS		+= --static -Wl,--start-group -lc -lgcc -lnosys -Wl,--end-group \
		   -T$(LDSCRIPT) -nostartfiles -Wl,--gc-sections,--print-gc-sections \
		   $(ARCH_FLAGS) \
		   -L$(OPENCM3_DIR)/lib

.DEFAULT_GOAL := measure_chacha20.bin
# .PRECIOUS: %.s  # uncomment this to preserve assembly files

lib:
	@if [ ! "`ls -A $(OPENCM3_DIR)`" ] ; then \
		printf "######## ERROR ########\n"; \
		printf "\tlibopencm3 is not initialized.\n"; \
		printf "\tPlease run (in the root directory):\n"; \
		printf "\t$$ git submodule update --init\n"; \
		printf "\tbefore running make.\n"; \
		printf "######## ERROR ########\n"; \
		exit 1; \
		fi
	make -C $(OPENCM3_DIR)

%.bin: %.elf
	$(OBJCOPY) -Obinary $(*).elf $(*).bin

%.elf: %.o $(OBJS) $(LDSCRIPT)
	$(LD) -o $(*).elf $(*).o $(OBJS) $(LDFLAGS) -l$(LIBNAME)

measure_chacha%.o: measure_chacha%.c ../common/measure.c
	$(CC) $(CFLAGS) -o $@ -c $<

%.o: %.c
	$(CC) $(CFLAGS) -o $@ -c $<

%.s:
	python3 ../common/chacha_gen.py $(patsubst chacha%,%,$(basename $(notdir $*))) > $*.s

clean:
	rm -f ../common/{*.elf,*.bin,*.d,*.o,*.s}
	rm -f {*.elf,*.bin,*.d,*.o,*.s}

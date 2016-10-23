#!/usr/bin/env python3

"""Generate asm code for the chacha_perm_asm function"""
import sys

rounds = 12

if len(sys.argv) == 1:
    rounds = 12
elif len(sys.argv) == 2 and int(sys.argv[1]) in [8, 12, 20]:
    rounds = int(sys.argv[1])
else:
    print("Syntax: chacha_gen.py [8|12|20]")
    sys.exit(1)

print("""
// THIS FILE WAS GENERATED USING chacha_gen.py
// DO NOT MODIFY DIRECTLY

.global chacha{rounds}_perm_asm
.type chacha{rounds}_perm_asm, %function

.syntax unified
.cpu cortex-m3

// operates on r0 as output and r1 as input pointer
// assumes space of 64 bytes following both pointers
chacha{rounds}_perm_asm:""".format(rounds=rounds))
print("push {r0, r4-r12, r14} // preserve r0 + other values (r1-r3 are args)")

print("ldm r1!, {r0, r2-r12, r14}")
rmap = ['r0',  'r2',  'r3',  'r4',  'r5',  'r6',  'r7',  'r8',
        'r9', 'r10', 'r11', 'r12', 'r14',  '--',  '--',  '--']

print("push {r9, r14}  // store 8 and 12 on the stack")
rmap[8], rmap[12] = 's0', 's1'

print("ldm r1!, {r9, r14}  // get 13, 14")
rmap[13], rmap[14] = 'r9', 'r14'

print("ldr.W r1, [r1, #0]  // get 15")
rmap[15] = 'r1'

ror = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def ROR(a, n):
    ror[a] = (ror[a] + n) % 32


def print_op(op, a, b):
    print("{op} {a}, {a}, {b}, ROR #{ror}".format(
          op=op, a=rmap[a], b=rmap[b], ror=(ror[b]-ror[a]) % 32))


def QUARTERROUND(a, b, c, d):
    print_op("add", a, b)
    print_op("eor", d, a)
    ROR(d, 16)
    print_op("add", c, d)
    print_op("eor", b, c)
    ROR(b, 20)
    print_op("add", a, b)
    print_op("eor", d, a)
    ROR(d, 24)
    print_op("add", c, d)
    print_op("eor", b, c)
    ROR(b, 25)

stackflag = False  # this could probably be nicer, using a closure


def stackswitch(a, b):
    """places a and b on the stack, replaces with currently stored values"""
    global stackflag
    c, d = sorted([i for i, x in enumerate(rmap) if x[0] == 's'])
    if stackflag:
        print("str {a}, [sp, #8]\n"
              "str {b}, [sp, #12]\n"
              "pop {{{a}, {b}}}".format(a=rmap[a], b=rmap[b]))
    else:
        print("push {{{a}, {b}}}\n"
              "ldr {a}, [sp, #8]\n"
              "ldr {b}, [sp, #12]".format(a=rmap[a], b=rmap[b]))
    rmap[a], rmap[c] = rmap[c], rmap[a]
    rmap[b], rmap[d] = rmap[d], rmap[b]
    stackflag = not stackflag


for i in range(rounds // 2):
    QUARTERROUND(1, 5,  9, 13)
    QUARTERROUND(2, 6, 10, 14)
    QUARTERROUND(3, 7, 11, 15)
    stackswitch(9, 10)
    QUARTERROUND(0, 4,  8, 12)
    QUARTERROUND(1, 6, 11, 12)
    QUARTERROUND(2, 7,  8, 13)
    stackswitch(8, 12)
    QUARTERROUND(0, 5, 10, 15)
    QUARTERROUND(3, 4,  9, 14)

for i, x in enumerate(ror):
    # TODO also make it fixable when values on stack end up rotated
    if rmap[i][0] == 'r' and x > 0:
        print("ror {r}, {r}, #{x}".format(r=rmap[i], x=x))

# TODO make this dynamic, based on rmap
print("""
push {r1} // save the value in r1 to make room for the output address
ldr r1, [sp, #12] // load the output address back to r1
stm r1!, {r0, r2-r8}
ldm sp, {r2-r4} // load three registers that are temporarily on the stack
stm r1!, {r3, r10-r12}
stm r1!, {r4, r9, r14}
str r2, [r1, #0]

add sp, #16
pop {r4-r12, r14} // restore potential other values
bx lr""")

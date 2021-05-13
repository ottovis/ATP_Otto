.cpu cortex-m0
.align 4
.global start print_asciz uart_print_int uart_get_int divide

.bss
stack_alt: 1024
var_lut: 64

.data

.text

start:
PUSH {LR, R4, R5, R6, R7}
MOV R4, SP
MOV SP, =stack_alt

MOV R0, #5
PUSH R0

BL macro1

macro1:
MOV R7, LR






marco1_end:
MOV PC R7



MOV SP, R4
POP {PC, R4, R5, R6, R7}




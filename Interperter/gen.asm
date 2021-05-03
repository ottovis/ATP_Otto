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

MOV R0 #1 
PUSH R0
MOV R0 #2
PUSH R0
MOV R0 #3
PUSH R0
MOV R0 #4
PUSH R0
POP {R0, R1}
ADD R2, R0, R1
PUSH R2
POP {R0, R1}
ADD R2, R0, R1
PUSH R2
POP R0
MOV R5, SP
MOV SP, R4
BL uart_print_int
MOV R5, SP
MOV SP, R4
POP R0
MOV R5, SP
MOV SP, R4
BL uart_print_int
MOV R5, SP
MOV SP, R4

MOV SP, R4
POP {PC, R4, R5, R6, R7}




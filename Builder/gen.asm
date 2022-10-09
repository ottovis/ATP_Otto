.cpu cortex-m0
.align 4
.global application, start, print_asciz, uart_print_int, uart_get_int, divide

.bss
stack_alt:
.skip 1024
var_lut:
.skip 64

.data
text1: .asciz "Hallo wereld"

.text

application:
PUSH {R4, R5, R6, R7, LR}
MOV R4, SP
LDR R6, =stack_alt
MOV SP, R6

MOV R0, #1
PUSH {R0}
MOV R0, #2
PUSH {R0}
MOV R0, #3
PUSH {R0}
MOV R0, #4
PUSH {R0}
MOV R0, #5
PUSH {R0}
MOV R5, SP
MOV SP, R4
BL uart_get_int
MOV R5, SP
MOV SP, R4
PUSH {R0}
POP {R0}
MOV R5, SP
MOV SP, R4
BL uart_print_int
MOV R5, SP
MOV SP, R4
LDR R0, =text1
MOV R5, SP
MOV SP, R4
BL print_asciz
MOV R5, SP
MOV SP, R4

MOV SP, R4
POP {R4, R5, R6, R7, PC}


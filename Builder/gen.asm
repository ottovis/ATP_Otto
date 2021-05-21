.cpu cortex-m0
.align 4
.global application, start, print_asciz, uart_print_int, uart_get_int, divide

.bss
stack_alt:
.skip 1024
var_lut:
.skip 64

.data
text1: .asciz "Printing first 10 in fibonacci:"
text2: .asciz "0"

.text

application:
PUSH {R4, R5, R6, R7, LR}
MOV R4, SP
LDR R6, =stack_alt
MOV SP, R6

LDR R0, =text1
MOV R5, SP
MOV SP, R4
BL print_asciz
MOV R5, SP
MOV SP, R4
MOV R0, #20
PUSH {R0}
LDR R0, =0
PUSH {R0}
POP {R0, R1}
LDR R2, =var_lut
STR R1, [R2, R0]
MOV R0, #1
PUSH {R0}
MOV R0, #1
PUSH {R0}
LDR R0, =text2
MOV R5, SP
MOV SP, R4
BL print_asciz
MOV R5, SP
MOV SP, R4
BL macro_A
BL macro_A

MOV SP, R4
POP {R4, R5, R6, R7, PC}

macro_A:
MOV R7, LR

LDR R0, =1
PUSH {R0}
POP {R0, R1}
LDR R2, =var_lut
STR R1, [R2, R0]
LDR R0, =2
PUSH {R0}
POP {R0, R1}
LDR R2, =var_lut
STR R1, [R2, R0]
LDR R0, =1
PUSH {R0}
POP {R0}
LDR R2, =var_lut
LDR R1, [R2, R0]
PUSH {R1}
LDR R0, =1
PUSH {R0}
POP {R0}
LDR R2, =var_lut
LDR R1, [R2, R0]
PUSH {R1}
LDR R0, =2
PUSH {R0}
POP {R0}
LDR R2, =var_lut
LDR R1, [R2, R0]
PUSH {R1}
POP {R0, R1}
ADD R2, R0, R1
PUSH {R2}
LDR R0, =2
PUSH {R0}
POP {R0}
LDR R2, =var_lut
LDR R1, [R2, R0]
PUSH {R1}
POP {R0}
MOV R5, SP
MOV SP, R4
BL uart_print_int
MOV R5, SP
MOV SP, R4
LDR R0, =0
PUSH {R0}
POP {R0}
LDR R2, =var_lut
LDR R1, [R2, R0]
PUSH {R1}
MOV R0, #1
PUSH {R0}
POP {R0, R1}
SUB R2, R0, R1
PUSH {R2}
LDR R0, =0
PUSH {R0}
POP {R0, R1}
LDR R2, =var_lut
STR R1, [R2, R0]
LDR R0, =0
PUSH {R0}
POP {R0}
LDR R2, =var_lut
LDR R1, [R2, R0]
PUSH {R1}
BL conditinal0
BL macro_A

macro_A_end:
MOV PC, R7

conditinal0:
PUSH {LR}
POP {R0}
CMP R0, #0
BEQ conditinal0_end

MOV R5, SP
MOV SP, R4
MOV R5, SP
MOV SP, R4
MOV R5, SP
MOV SP, R4
MOV R5, SP
MOV SP, R4

conditinal0_end:
MOV PC, R7


.cpu cortex-m0
.align 4
.text
.global application

text1: .asciz "Hello world, the aANSWERzZ is 42! @[]`{}~" 


application:
    push {R4, R5, R6, R7, LR}
    MOV R4, SP

    MOV R0, #1
    push {R0}

    MOV R0, #2
    push {R0}

    MOV R0, #3
    push {R0}

    MOV R0, #4
    push {R0}

    MOV R0, #5
    push {R0}

    BL uart_get_int
    push {R0}

    pop {R0}
    BL uart_print_int

    LDR R0, =text1
    BL uart_print_string

    pop {R4, R5, R6, R7, LR}

    
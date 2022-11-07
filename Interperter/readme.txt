Mouse

Mouse is in deze form volgens de Mouse79 specifiecatie geimpementeert


Operator symbols:
    +
    -
    *
    /

IO symbols:
    ? input int
    ! output int
    "" print bevantende tekst

Speciale tekens:
    $ einde programma
    $$ exit programma
    = assignment, pop 2 waardes, plaats waarde 1 in var bij naam van waarde 2
    . dereference, pop waarde en push waarde bij naam van de eerste waarde
    [ ] pop waarde van stack, als deze == 0 voer het [] blok uit
    ( ) loop tussen de twee haken 
    ^ exit loop 
    #AtmZ definiteerd/roept een Macro, eerste loop over wordt deze niet uitgevoerd maar alleen geregisteerd
    @ exit conditie van een Macro
    

Type support
    Mouse++ opereert alleen met ints, let dus op met deel operators, discards achter de comma waarde

Usage:
    > python3 mouse_interperter.py <name of file to execute>
    Example programs are provided to show some of the syntax and capabilities of the language 


Example code:
    B [ S ] is equivalent to:  if not B then S

    a simple program to input a number from the terminal and print it at the terminal would be:
        ? ! $$

    Within a mouse program, two numbers are separated by a space. The following program adds 2 + 3:
        2 3 + $$

    The following program reads a number from the terminal, adds 3 to it, and prints the result to the terminal:
        ? 3 + ! $$

    Loop example that prints 10 to 1 and then exits:
    10 i = ( i . [ ^ ] i . ! i . 1 - i = )
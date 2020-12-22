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

Speciale tekens:
    $ einde programma
    $$ exit programma
    (in "" blok) ! is new line
    = assignment, pop 2 waardes, plaats waarde 1 at waarde 2
    . dereference, pop waarde en push waarde at locatie van de eerste waarde
    [ ] pop waarde van stack, als deze <= 0 is skip alles in het [] blok
    ( ) loop tussen de twee haken 
    ^ exit loop 
    #AtmZ definiteerd/roept een Macro, eerste loop over wordt deze niet uitgevoerd maar geregisteerd
    @ exit conditie van een Macro

    ABC etc kan worden gebruikt als vervanging van 0 t/m 25
    



Type support
    Mouse++ opereert alleen met ints, let dus op met deel operators, discards achter de comma waarde

Example code:
    B [ S ]  ~ equivalent to:  if B then S

    a simple program to input a number from the terminal and print it at the terminal would be:
        ?!$$

    Within a mouse program, two numbers are separated by a space. The following program adds 2 + 3:
        2 3 + $$

    The following program reads a number from the terminal, adds 3 to it, and prints the result to the terminal:
        ? 3 + ! $$
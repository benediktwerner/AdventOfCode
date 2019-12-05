# Intcode assembler

This is my version of an intcode assembler. It supports all the opcodes from day 5
and a number of additional high-level instructions.

## Example

This program computes Day 1 Part 1 in intcode:

```
# Comments start with '#'
start:                  # Label for jump
    in x                # Read to memory location x. The assembler automatically 'allocates' this memory after the program.
    eq x 0 tmp          # Check if input == 0. If yes, stop and print the result.
    jtrue tmp :end      # Label targets must be prefixed with a ':'
    div x 3 x
    sub x 2 x
    add total x total
    jmp :start

end:
    out total
    hlt

# Initialize 'total' to 0. The assembler does this automatically so
# this isn't really neccessary, but it shows the concept.
total = 0
```

## Instructions

|        Operation         |            Effect             |                          Note                          |
| :----------------------: | :---------------------------: | :----------------------------------------------------: |
|      `mov a target`      |         `target = a`          |                                                        |
|     `add a b target`     |       `target = a + b`        |                                                        |
|     `sub a b target`     |       `target = a - b`        |                                                        |
|     `mul a b target`     |       `target = a * b`        |                                                        |
|     `div a b target`     |       `target = a // b`       | Can be quite slow, only works for positive numbers atm.  |
|     `mod a b target`     |       `target = a % b`        | Can be quite slow, only works for positive numbers atm |
| `divmod a b target rest` | `target, rest = divmod(a, b)` | Can be quite slow, only works for positive numbers atm |
|       `in target`        |      `target = input()`       |                                                        |
|         `out a`          |          `print(a)`           |                                                        |
|       `jmp target`       |         `goto target`         |                                                        |
|      `jnz a target`      |   `if a != 0: goto target`    |                     Alias: `jtrue`                     |
|      `jz a target`       |   `if a == 0: goto target`    |                    Alias: `jfalse`                     |
|     `eq a b target`      |       `target = a == b`       |                                                        |
|     `lt a b target`      |       `target = a < b`        |                                                        |
|     `leq a b target`     |       `target = a <= b`       |                                                        |
|     `gt a b target`      |       `target = a > b`        |                                                        |
|     `geq a b target`     |       `target = a >= b`       |                                                        |
|     `and a b target`     |      `target = a and b`       |                                                        |
|     `or a b target`      |      `target = a and b`       |                                                        |
|      `not a target`      |       `target = not a`        |                                                        |
|          `hlt`           |           `exit()`            |                     Alias: `halt`                      |

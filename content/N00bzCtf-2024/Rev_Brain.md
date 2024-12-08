Title: Brain
Date: 2024-08-04

We are presented a string in [brainfuck](https://en.wikipedia.org/wiki/Brainfuck) language. The first thing we notice that it is not outputting anything (not a single '.' character in it).

```brainfuck
>+++++++++++[<++++++++++>-]<[-]>++++++++[<++++++>-]<[-]>++++++++[<++++++>-]<[-]
>++++++++++++++[<+++++++>-]<[-]>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[<++>-]<[-]
>+++++++++++++++++++++++++++++++++++++++++[<+++>-]<[-]>+++++++[<+++++++>-]<[-]
>+++++++++++++++++++[<+++++>-]<[-]>+++++++++++[<+++++++++>-]<[-]>+++++++++++++[<++++>-]<[-]
>+++++++++++[<++++++++++>-]<[-]>+++++++++++++++++++[<+++++>-]<[-]>+++++++++++[<+++++++++>-]<[-]
>++++++++[<++++++>-]<[-]>++++++++++[<++++++++++>-]<[-]>+++++++++++++++++[<+++>-]<[-]
>+++++++++++++++++++[<+++++>-]<[-]>+++++++[<+++++++>-]<[-]>+++++++++++[<++++++++++>-]<[-]
>+++++++++++++++++++[<+++++>-]<[-]>++++++++++++++[<+++++++>-]<[-]
>+++++++++++++++++++[<++++++>-]<[-]>+++++++++++++[<++++>-]<[-]>+++++++[<+++++++>-]<[-]
>+++++++++++[<++++++++++>-]<[-]>+++++++++++++++++[<++++++>-]<[-]>+++++++[<++++++>-]<[-]
>+++++++++++[<+++++++++>-]<[-]
>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[<+>-]<[-]
>+++++++++++[<+++>-]<[-]>+++++++++++++++++++++++++[<+++++>-]<[-]
```

The next thing that jumps into ones eye are these `<[-]`. The `<` jumps right back into the previous memory cell while `[-]` is equal to

```c
while (cell_value[i] != 0) {
    cell_value[i]--;
}
```

and causes whatever value was written into that cell before to be decreased to 0 again.

Since we are curious we want to output each of these values before they get neutralized again. So our task here is to simply insert a `.` command into each of the `<[-]` commands:  `<.[-]`

Putting the resulting `brainfuck` code into a brainfuck interpreter will now give us the flag.
Title: Numbers2
Date: 2024-08-04

Numbers2 is the successor of an older challenge presented at [N00bzCtf 2023](https://github.com/n00bzUnit3d/n00bzCTF2023-OfficalWriteups/tree/master/Misc/Numbers) with a few differences:

- It outputs and additional welcome message
- It asks for three different challenge questions
- successful solving attempts are being answered with different responses

We have to solve several programming challenges here:

1. Challenge inputs do not end on EOL but on ': ' instead. So we cannot simply use the `input()` function to read the questions from stdin
2. We have to parse two integers from within a line of text
3. Questions for the least common multiple or the greatest common divisor can be answered using the builtin methods from the math module `math.lcm()` / `math.gcd()`. But to answer the question asking for the largest prime factor we must implement an algorithm or an appropriate library from pip must be used

`1.` can easily be achieved using the `re.findall()` method:

```python
[x] = re.findall(r'\d+', "Give me the greatest prime factor of 42")
# x = 42

x, y = re.findall(r'\d+', "Give me the least common multiple of 42 and 23")
# x = "42"
# x = "23"
```

To solve `2.` we need to write an own implementation of an input method that stops reading single characters once it sees a ':'. We simply call `sys.stdin.read(1)` in a loop and decide whether to continue reading chars or not.

```python
def input_until_char(sep):
    input_read = ""

    c = sys.stdin.read(1)
    input_read += c
    while c != "" and c != "\n" and c != sep:
        c = sys.stdin.read(1)
        input_read += c
    return input_read
```

For `3.` a naive implementation of using a loop over all prime factor candidates to find out whether a candidate factor is prime is fast enough to find the largest prime factor:

```python
largest_prime_factor = 1
for n in range(1,int(x)+1):
    is_prime = True
    for factor in range(2, n):
        if n%factor == 0:
            is_prime = False
            break
    if is_prime and int(x)%n == 0 and n > largest_prime_factor:
        largest_prime_factor = n
```

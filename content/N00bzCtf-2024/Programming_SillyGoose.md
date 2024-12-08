Title: SillyGoose
Date: 2024-08-04

Simple binary search number guessing game. You guess a number and the challenge tells you whether the goal is lower or higher.

```python
import sys

lower_bound = 1
upper_bound = pow(10, 100)

f = open("sillygoose.log", "w")

found = False
while not found:
    attempt = lower_bound + (upper_bound - lower_bound)//2
    print(str(attempt))
    f.write("> " + str(attempt) + "\n")

    answer = input()
    f.write("< " + answer + "\n")

    if "too small" in answer:
        lower_bound = attempt
        continue
    if "too large" in answer:
        upper_bound = attempt
        continue
    break

flag = input()
f.write("< " + flag + "\n")
print(flag, file=sys.stderr)

print("yay")
f.write("> yay\n")

f.close()
```

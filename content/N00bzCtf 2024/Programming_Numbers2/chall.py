#!/usr/bin/env python3
import random
import math
import time
starting_time=int(time.time())
def solve(x,y,which_question):
	if which_question == 'largest_primefactor':
		# naive and slow implementation
		largest_prime_factor = 1
		for n in range(1,x+1):
			is_prime = True
			for factor in range(2, n):
				if n%factor == 0:
					is_prime = False
					break
			if is_prime and x%n == 0 and n > largest_prime_factor:
				largest_prime_factor = n
		return largest_prime_factor
	elif which_question == 'lcm':
		return math.lcm(x, y)
	else:
		return math.gcd(x, y)

print("Welcome to numbers!")

for i in range(1,101):
	difficulty1 = 25
	difficulty2 = 1000
	print(f'Round {i}!')
	x = random.randrange(0,10)
	y = random.randint(difficulty1,difficulty2)
	current_time = int(time.time())
	if current_time - starting_time > 60:
		print("Time's up!")
		exit()
	which_question = random.choice(['largest_primefactor', 'lcm', 'gcd'])
	if which_question == 'largest_primefactor':
		user_answer =  int(input(f"Give me the greatest prime factor of {x}: "))
	elif which_question == 'lcm':
		user_answer =  int(input(f"Give me the least common multiple of {x} and {y}: "))
	else:
		user_answer = int(input(f"Give me the greatest common divisor of {x} and {y}: "))
	correct_answer = solve(x,y,which_question)
	if user_answer == correct_answer:
		print("Correct!")
		difficulty1 += difficulty1
		difficulty2 += difficulty2
	else:
		print("Incorrect!")
		exit()
	if i == 100:
		print(open('flag.txt').read())
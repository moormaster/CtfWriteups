import math
import re
import sys

# input method that reads characters until a separation character sep or EOL/EOF occurs
# useful for reading inputs that do not end on EOL
def input_until_char(sep):
	input_read = ""

	c = sys.stdin.read(1)
	input_read += c
	while c != "" and c != "\n" and c != sep:
		c = sys.stdin.read(1)
		input_read += c
	return input_read

NUMBER_OF_ROUNDS=100


f = open("numbers2.log", "w")

received_welcome_message = input()
f.write("< " + received_welcome_message + "\n")

read_flag = True
for r in range(NUMBER_OF_ROUNDS):
	received_round = input()
	f.write("< " + received_round + "\n")

	challenge_received = input_until_char(':')
	f.write("< " + challenge_received + "\n")

	if "greatest prime factor" in challenge_received:
		[x] = re.findall(r'\d+', challenge_received)
		# naive and slow implementation
		largest_prime_factor = 1
		for n in range(1,int(x)+1):
			is_prime = True
			for factor in range(2, n):
				if n%factor == 0:
					is_prime = False
					break
			if is_prime and int(x)%n == 0 and n > largest_prime_factor:
				largest_prime_factor = n
		answer = str(largest_prime_factor)
	elif "least common multiple" in challenge_received:
		x,y = re.findall(r'\d+', challenge_received)
		answer = str(math.lcm(int(x), int(y)))
	elif "greatest common divisor" in challenge_received:
		x,y = re.findall(r'\d+', challenge_received)
		answer = str(math.gcd(int(x), int(y)))
	else:
		print("Unknown challenge question received!", file=sys.stderr)
		read_flag = False
		break;

	print(answer)
	f.write("> " + answer + "\n")

	received_reply = input()
	f.write("< " + received_reply + "\n")

	if not "Correct" in received_reply:
		read_flag = False
		break

if read_flag:
	flag = input()
	f.write("< " + flag + "\n")
	print(flag, file=sys.stderr)

f.close()

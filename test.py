import string
import random

d = string.digits
h = string.ascii_letters

u = d + h

code = ''.join(u[random.randint(0,len(u)-1)] for i in range(6))
print(code)
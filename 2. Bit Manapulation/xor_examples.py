from re import X


x = 34
y = 125

print(f'x = {x:8b}')
print(f'y = {y:8b}')

# x, y = y, x

# t = x
# x = y
# y = t

x = x ^ y
y = x ^ y
x = x ^ y

print()

print(f'x = {x:8b}')
print(f'y = {y:8b}')

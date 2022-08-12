from typing import Any


x: Any = 12
x = 'hello'
print(x)

y: int = 12
# y = 'hello'
print(y)

z: int | str = 42
z = 'hello'
print(z)

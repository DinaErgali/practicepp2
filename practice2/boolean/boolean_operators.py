# Arithmetic Operators
x = 15
y = 4

print(x + y)        # 19
print(x - y)        # 11 
print(x * y)        # 60
print(x / y)        # 3.75
print(x % y)        # 3
print(x ** y)       # 50625
print(x // y)       # 3

# The Walrus Operator
numbers = [1, 2, 3, 4, 5]

if (count := len(numbers)) > 3:
    print(f"List has {count} elements")         # List has 5 elements


# Comparison Operators

x = 5
y = 3

print(x == y)
print(x != y)
print(x > y)
print(x < y)
print(x >= y)
print(x <= y)

# Chaining Comparison Operators
x = 5

print(1 < x < 10)
print(1 < x and x < 10)

# Logical Operators
x = 5
print(x > 0 and x < 10)
print(x < 5 or x > 10)
print(not(x > 3 and x < 10))

# Identity Operators
x = [1, 2, 3]
y = [1, 2, 3]

print(x == y)
print(x is y)

# Membership Operators
text = "Hello World"

print("H" in text)
print("hello" in text)
print("z" not in text)

# Bitwise Operators
print(6 & 3)
print(6 | 3)
print(6 ^ 3)

# Operator Precedence
print(100 + 5 * 3)
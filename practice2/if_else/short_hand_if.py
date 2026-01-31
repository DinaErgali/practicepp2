# Short hand if-else
a = 2
b = 330
print("A") if a > b else print("B")

# Assign a value with if-else
a = 10
b = 20
bigger = a if a > b else b
print("Bigger is", bigger)

# Multiple conditions on one line
a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")

# Practical examples
# Example 1
x = 15
y = 20
max_value = x if x > y else y
print("Maximum value:", max_value)
# Example 2
username = ""
display_name = username if username else "Guest"
print("Welcome,", display_name)
 
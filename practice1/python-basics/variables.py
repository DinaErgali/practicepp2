# 1 - A variable is created the moment you first assign a value to it.
x = 5
y = "John"
print(x)
print(y)

# 2 -
x = 4       # x is of type int
x = "Sally" # x is now of type str
print(x)

# 3 - 
x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0

# 4 - Get the data type of a variable with the function
x = 5
y = "John"
print(type(x))
print(type(y))

# 5 -
x = "John"
# is the same as
x = 'John'

# 6 -
a = 4
A = "Sally"
#A will not overwrite a

# 7 - Legal variable names
myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"

# 8 - 
myVariableName = "John" # Camel Case
MyVariableName = "John" # Pascal Case
my_variable_name = "John" # Snake Case

# 9 - Many Values to Multiple Variable
x, y, z = "Orange", "Banana", "Cherry"

print(x)
print(y)
print(z)

# 10 - One Value to Multiple Variables
x = y = z = "Orange"

print(x)
print(y)
print(z)

# 11 - Unpack a Collection
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)

# 12 - Output Variables
x = "Python is awesome"
print(x)

x = "Python"
y = "is"
z = "awesome"
print(x, y, z)

x = "Python "
y = "is "
z = "awesome"
print(x + y + z)

x = 5
y = 10
print(x + y)

x = 5
y = "John"
print(x, y)

# 13 - Global Variables
x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)
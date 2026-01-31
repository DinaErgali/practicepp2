a = 200
b = 33
if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")

# Evaluate values and variables
# First method
print(bool("Hello"))            # True
print(bool(15))                 # True
# Second method
x = "Hello"
y = 15
print(bool(x))                  # True
print(bool(y))                  # True

# Most values are True
# Almost any value is evaluated to True if it has some sort of content
# Any string is True, except empty strings
# Any number is True, except 0
# Any list, tuple, set, and dictionary are True, except empty ones
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

# Some values are False
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})

# One more value, or object in this case, evaluates to False, and that is if you have an object that is made from a class with a __len__ function that returns 0 or False
class myclass():
    def __len__(self):
        return 0

myobj = myclass()
print(bool(myobj))

# Functions can return a Boolean
def myFunction() :
    return True

if myFunction():
    print("YES!")
else:
    print("NO!")

# Python also has many built-in functions that return a boolean value, like the isinstance() function, which can be used to determine if an object is of a certain data type
x = 200
print(isinstance(x, int))
 
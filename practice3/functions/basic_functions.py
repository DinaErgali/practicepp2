#1
def my_function():
  print("Hello from a function")

my_function()       #output Hello from a function

#2 
temp1 = 77
celsius1 = (temp1 - 32) * 5 / 9
print(celsius1)     # output 25.0

temp2 = 95
celsius2 = (temp2 - 32) * 5 / 9
print(celsius2)     # output 35.0

temp3 = 50
celsius3 = (temp3 - 32) * 5 / 9
print(celsius3)     # output 10.0


def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))

#3
def get_greeting():
  return "Hello from a function"
message = get_greeting()
print(message)


def get_greeting():
  return "Hello from a function"
print(get_greeting())

#4
def my_function():
  pass

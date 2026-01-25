# Double quotes and Single
print("Hello")
print('Hello')

# Quotes Inside Quotes
print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"')

# Assign String to a Variable
a = "Hello"
print(a)

# Multiline Strings
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)    # Use three double quotes    

a = '''Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.'''
print(a)    # Use three single quotes

# Strings are Arrays
a = "Hello, World!"
print(a[1])

# Looping Through a String
for x in "banana":
  print(x)

# String Length
a = "Hello, World!"
print(len(a))

# Check String
txt = "The best things in life are free!"
print("free" in txt)

txt = "The best things in life are free!"
if "free" in txt:
  print("Yes, 'free' is present.")

# Check if NOT
txt = "The best things in life are free!"
print("expensive" not in txt)

txt = "The best things in life are free!"
if "expensive" not in txt:
  print("No, 'expensive' is NOT present.")


b = "Hello, World!"
print(b[2:5])   
b = "Hello, World!"
print(b[:5])    
b = "Hello, World!"
print(b[2:])    
b = "Hello, World!"
print(b[-5:-2])
a = "Hello, World!"
print(a.upper())          # output HELLO, WORLD!
a = "Hello, World!"     
print(a.lower())          # output hello, world!
a= " Hello, World! "    
print(a.strip())          # returns "Hello, World!"
a = "Hello, World!"
print(a.replace("H", "J"))# returns Jello, World!
a = "Hello, World!"
print(a.split(","))       # returns ['Hello', ' World!']

a = "Hello"
b = "World"
c = a + b
print(c)                  # output HelloWorld

a = "Hello"
b = "World"
c = a + " " + b
print(c)                  # output Hello World


age = 36
#This will produce an error:
txt = "My name is John, I am " + age
print(txt)                # output TypeError: must be str, not int

age = 36
txt = f"My name is John, I am {age}"
print(txt)                # output My name is John, I am 36

price = 59
txt = f"The price is {price} dollars"
print(txt)                # output The price is 59 dollars

price = 59
txt = f"The price is {price:.2f} dollars"
print(txt)                # output The price is 59.00 dollars

txt = f"The price is {20 * 59} dollars"
print(txt)                #output The price is 1180 dollars

txt = "We are the so-called \"Vikings\" from the north."    # use the escape character :\"



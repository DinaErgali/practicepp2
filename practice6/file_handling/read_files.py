# 1. Simple read entire file
with open("example.txt", "r") as f:
    print(f.read())

#7 Read one line of the file:
with open("example.txt") as f:
  print(f.readline())

with open("example.txt") as f:
  for x in f:
    print(x)

# 2. Read line by line
with open("example.txt", "r") as f:
    for line in f:
        print(line.strip())

# 3. Read first N characters
with open("example.txt", "r") as f:
    print(f.read(10))

# 4. Read all lines into list
with open("example.txt", "r") as f:
    lines = f.readlines()
    print(lines)

# 5. Count words in file
with open("example.txt", "r") as f:
    text = f.read()
    print(len(text.split()))

#6 You can output as many charecters as you show
with open("example.txt") as f:
  print(f.read(5))

#7 Read one line of the file:
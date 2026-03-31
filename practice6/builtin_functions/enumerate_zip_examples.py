# 1. enumerate basic
names = ["Alice", "Bob", "Charlie"]
for i, name in enumerate(names):
    print(i, name)

# 2. enumerate with start
for i, name in enumerate(names, start=1):
    print(i, name)

# 3. zip two lists
a = [1, 2, 3]
b = ["a", "b", "c"]
print(list(zip(a, b)))

# 4. zip loop
for num, char in zip(a, b):
    print(num, char)

# 5. unzip
pairs = [(1, 'a'), (2, 'b')]
nums, chars = zip(*pairs)
print(nums, chars)
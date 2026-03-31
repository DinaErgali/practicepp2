from functools import reduce

# 1. map: square numbers
nums = [1, 2, 3]
print(list(map(lambda x: x**2, nums)))

# 2. filter: even numbers
nums = [1, 2, 3, 4]
print(list(filter(lambda x: x % 2 == 0, nums)))

# 3. reduce: sum
nums = [1, 2, 3, 4]
print(reduce(lambda x, y: x + y, nums))

# 4. map with strings
names = ["a", "b", "c"]
print(list(map(str.upper, names)))

# 5. combined example
nums = [1, 2, 3, 4, 5]
result = reduce(lambda x, y: x + y,
                filter(lambda x: x % 2 == 0,
                       map(lambda x: x*2, nums)))
print(result)
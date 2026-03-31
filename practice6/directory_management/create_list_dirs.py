import os

# 1. Create directory
os.mkdir("new_folder")

# 2. Create nested directories
os.makedirs("parent/child")

# 3. List files and folders
print(os.listdir("."))

# 4. Check if directory exists
print(os.path.exists("new_folder"))

# 5. List only directories
items = os.listdir(".")
dirs = [item for item in items if os.path.isdir(item)]
print(dirs)

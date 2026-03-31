import shutil

# 1. Move file
shutil.move("example.txt", "new_folder/example.txt")

# 2. Move and rename
shutil.move("output.txt", "new_folder/new_output.txt")

# 3. Move multiple files
files = ["a.txt", "b.txt"]
for file in files:
    shutil.move(file, "new_folder/" + file)

# 4. Move folder
shutil.move("parent", "new_folder/parent")

# 5. Move if exists
import os
if os.path.exists("example.txt"):
    shutil.move("example.txt", "new_folder/")
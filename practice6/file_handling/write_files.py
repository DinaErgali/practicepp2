# 1. Write text (overwrite)
with open("example.txt", "a") as f:
  f.write("Now the file has more content!")

#open and read the file after the appending:
with open("example.txt") as f:
  print(f.read())


f = open("file.txt", "w")
f.write("Hello world")
f.close()
  
#2 Open the file "demofile.txt" and overwrite the content
with open("example.txt", "w") as f:
  f.write("Woops! I have deleted the content!")

#open and read the file after the overwriting:
with open("example.txt") as f:
  print(f.read())

#3 Create a new file called "myfile.txt":

f = open("myfile.txt", "x")
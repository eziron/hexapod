import os

files = os.listdir()
print(files)
for x in files:
    print ("remove: ",x) 
    os.remove(x)

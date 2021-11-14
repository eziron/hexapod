import os

for x in os.listdir():
    print ("remove: ",x) 
    os.remove(x)

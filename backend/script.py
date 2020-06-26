import os

for i in range(10):
    first = i*1000000
    second = (i+1)*1000000
    print("processing from %d to %d" %(first,second))
    os.system("python all_artist_event.py %d %d" %(first,second))

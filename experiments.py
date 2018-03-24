#Run the file 100 times
import time
start = time.time()
numSim = 5000
open('results.txt', 'w').close()
for i in range(numSim):
  execfile("snakebattle.py")
end = time.time()
print ("Time elapsed for ",numSim," simulations: ", end-start )

def measureResults():
  with open('results.txt') as f:
    lines = f.readlines()
    lines = lines[0]
    print ("Player 1 won ", lines.count('1'), "times")
    print ("Player 2 won ", lines.count('2'), "times")
    print ("Draw happened ", lines.count('0'), "times")

measureResults()

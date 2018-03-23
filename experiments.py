#Run the file 100 times
open('results.txt', 'w').close()
for i in range(100):
  execfile("snakebattle.py")


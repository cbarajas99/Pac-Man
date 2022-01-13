import util

counter = util.Counter()


import util

test = util.Counter()
test[('A', 'Y')] = 5 # set the value stored at key ('A', 'Y') to 5
print(test[('A', 'Y')]) # should print 5
test[('A', 'Y')] += 1 # increase the value stored at key ('A', 'Y') by 1
print(test[('A', 'Y')]) # should print Answer
test[('B', 'W')] += 1 # increase the value stored at key ('B', 'W') by 1
print(test[('B', 'W')]) # should print Answer
print(test[('C', 'Z')]) 
# print the value stored at key ('C', 'Z'), should print Answer
print("TEST",test)
print(test[['C', 'Z']]) # This line Answer

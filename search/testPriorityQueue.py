import util

queue = util.PriorityQueue()
queue.push('A', 4)
queue.push('A', 2)
queue.update('B', 5)
queue.update('B', 3)

while not queue.isEmpty():
    print queue.pop()

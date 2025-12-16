from collections import deque
from typing import Any


class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("stack is empty")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)


class Queue:
    def __init__(self):
        self._data: deque[Any] = deque()

    def enqueue(self, item):
        self._data.append(item)         

    def dequeue(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        return self._data.popleft()    

    def peek(self):
        if self.is_empty():
            return None
        return self._data[0]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)


if __name__ == "__main__":
    print("Stack")
    stack = Stack()
    stack.push(10)
    stack.push(20)
    stack.push(30)

    print(stack.peek())
    print(stack.pop())
    print(stack.pop())
    print(stack.is_empty())
    print(len(stack))

    print("\nQueue")
    queue = Queue()
    queue.enqueue("a")
    queue.enqueue("b")
    queue.enqueue("c")

    print(queue.peek())
    print(queue.dequeue())
    print(queue.dequeue())
    print(queue.is_empty())
    print(len(queue))

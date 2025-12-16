class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class SinglyLinkedList:
    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None   
        self._size: int = 0

    def append(self, value):
        new_node = Node(value)

        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self._size += 1

    def prepend(self, value):
        new_node = Node(value, next=self.head)
        self.head = new_node
        if self._size == 0:
            self.tail = new_node
        self._size += 1

    def insert(self, idx, value):
        if idx < 0 or idx > self._size:
            raise IndexError("negative index is not supported")

        if idx == 0:
            self.prepend(value)
            return
        if idx == self._size:
            self.append(value)
            return
        
        current = self.head
        # ошибка: нет проверки выхода за границы
        for _ in range(idx - 1):
            current = current.next

        new_node = Node(value, next=current.next)
        current.next = new_node
        self._size+=1 
    
    def remove(self, value) -> None:
        if self.head is None:
            raise ValueError('пусто тут, нечего удалять')
        if self.head.value == value:
            self.head = self.head.next
            if self._size == 1:
                self.tail = None
            self._size -= 1
            return 
        current = self.head
        while current.next is not None:
            if current.next.value == value:
                if current.next == self.tail:
                    self.tail = current
                current.next = current.next.next
                self._size -= 1
                return
            current = current.next
        raise ValueError("value not found")


    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __len__(self):
        return self._size

    def __repr__(self):
        values = list(self)
        return f"SinglyLinkedList({values})"
    
if __name__ == "__main__":
    lst = SinglyLinkedList()

    print("Создали пустой список:")
    print(lst)
    print("Длина:", len(lst))
    print()

    print("добавление элементов")
    lst.append(1)
    lst.append(2)
    lst.append(3)
    print(lst)
    print("Длина:", len(lst))
    print()


    lst.prepend(0)
    print(lst)
    print("Длина:", len(lst))
    print()


    lst.insert(2, 99)
    print(lst)
    print("Длина:", len(lst))
    print()


    for value in lst:
        print(value, end=" ")
    print("\n")

    lst.remove(99)
    print(lst)
    print("Длина:", len(lst))
    print()

  
    lst.remove(0)
    print(lst)
    print("Длина:", len(lst))
    print()


    lst.remove(3)
    print(lst)
    print("Длина:", len(lst))
    print()

    print("Финальное состояние списка:")
    print(lst)

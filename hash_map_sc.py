# Name: Erik Grinn
# OSU Email: grinne@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/13/24
# Description: Separate Chaining HashMap

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        First checks to see if table load is > 1, and calls resize function to doulbe capacity if true.
        If node is present at hash_index, updates value.
        Otherwise, places new node at hash_index.
        """

        # double capacity if load factor >= 1
        if self.table_load() >= 1:
            self.resize_table(self._capacity*2)

        hash_index = self._hash_function(key) % self._capacity  # index of key = hash (using hash function) % array size
        bucket = self._buckets[hash_index]                      # bucket containing index

        # if node with key exists in bucket, update value
        # otherwise, insert new node with key/value pair and increment size
        node = bucket.contains(key)
        if node:
            node.value = value
            return
        bucket.insert(key, value)
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes table to new capacity.
        Sets new_capacity to next prime number (if not already prime) of given new_capacity.
        Creates new_capacity amount of buckets containing empty LinkedLists stored in a Dynamic Array ADT.
        Saves old buckets and updates data members to reflect new values
        Copies/inserts old buckets and nodes into updated structure.
        """

        if new_capacity < 1:
            return

        # create new capacity of next prime number from given value
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # append new_capacity amount of new empty buckets
        # each bucket is a LinkedList that are stored in a Dynamic Array ADT
        new_buckets = DynamicArray()
        for bucket in range(new_capacity):
            new_buckets.append(LinkedList())

        # save old buckets, update data members
        old_buckets = self._buckets
        self._buckets = new_buckets
        self._capacity = new_capacity
        self._size = 0

        # copy/insert old buckets into new buckets (rehashing and sizing is handled in the called 'put' method)
        for idx in range(old_buckets.length()):
            bucket = old_buckets[idx]
            for node in bucket:
                self.put(node.key, node.value)

    def table_load(self) -> float:
        """
        Returns hash table load factor.
        Load factor = total number of elements stored in table / number of buckets.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Counts number of empty buckets, checking to see if each bucket (LinkedList) has size > 0.
        Returns total count of empty buckets.
        """

        count = 0
        for idx in range(self._capacity):
            if self._buckets[idx].length() == 0:
                count += 1
        return count

    def get(self, key: str):
        """
        If bucket at hash_index contains node with key, return value of node with key/value pair.
        Otherwise, returns None.
        """

        hash_index = self._hash_function(key) % self._capacity
        bucket = self._buckets[hash_index]

        node = bucket.contains(key)
        if node:
            return node.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Checks to see if bucket at hash_index contains key.
        Returns Boolean.
        """

        hash_index = self._hash_function(key) % self._capacity
        bucket = self._buckets[hash_index]

        if bucket.contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes key at bucket with hash_index.
        Decrements size.
        """

        hash_index = self._hash_function(key) % self._capacity
        bucket = self._buckets[hash_index]
        if bucket.remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns dynamic array, which is a list of tuples with key/value pairs of nodes within each bucket.
        """

        da = DynamicArray()

        for idx in range(self._capacity):
            bucket = self._buckets[idx]
            for node in bucket:
                da.append((node.key, node.value))
        return da

    def clear(self) -> None:
        """
        Clears each bucket to be an empty LinkedList, and sets the size data member to 0.
        """

        for idx in range(self._capacity):
            self._buckets[idx] = LinkedList()
        self._size = 0

    def get_bucket(self, index: int) -> LinkedList:
        """
        Returns LinkedList (bucket) at index in hash map.
        """

        # if given index is within capacity, return bucket
        if 0 <= index < self._capacity:
            return self._buckets[index]


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Finds mode of a given dynamic array using a separately chained hashmap.
    Creates hashmap with nodes containing keys as element in da, and values as count found at hash_index
    Iterates through hashmap nodes in each bucket and updates a 'modes' da to reflect keys that contain max_frequency.
    Returns a tuple containing the modes da, and max_frequency.
    """

    # initialize new hashmap
    map = HashMap()

    # iterate through da, placing/updating nodes as appropriate
    for idx in range(da.length()):
        key = da[idx]
        if map.contains_key(key):           # if node already in map, increment node value by 1
            map.put(key, map.get(key) + 1)
        else:                               # if no node, place node in map and initialize value to 1
            map.put(key, 1)

    # initialize modes as empty da, and running max_frequency
    modes = DynamicArray()
    max_frequency = 0

    # iterate over each node in each bucket, and update modes as appropriate
    for idx in range(map.get_capacity()):
        bucket = map.get_bucket(idx)
        if bucket:
            for node in bucket:
                if node.value > max_frequency:    # if node found with value > max_frequency, refresh modes da
                    max_frequency = node.value    # ^ignore node.value warning, if present
                    modes = DynamicArray()
                    modes.append(node.key)
                elif node.value == max_frequency:  # if another node found with same max_frequency, append node key
                    modes.append(node.key)

    return modes, max_frequency


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")

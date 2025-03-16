# Name: Erik Grinn
# OSU Email: grinne@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/13/24
# Description: Open Addressing HashMap

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        First checks to see if table load is >= 0.5, and calls resize function to double capacity if true.
        Perform quadratic probing to find HashEntry with key.
        If HashEntry found, updates value.
        Otherwise, insert new entry at last checked index.
        """

        # Double capacity if table load >= 0.5
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # calculate hash index and initialize variables for quadratic probing
        initial_index = self._hash_function(key) % self._capacity
        iter_index = initial_index
        count = 0

        # quadratic probing: while key not found, quadratically probe from initial hash index
        while self._buckets[iter_index] and not self._buckets[iter_index].is_tombstone:
            if self._buckets[iter_index].key == key:
                self._buckets[iter_index].value = value
                return
            count += 1
            iter_index = (initial_index + (count ** 2)) % self._capacity  # quadratic probing

        # if no key found, insert new HashEntry with key/value pair, and increment size
        self._buckets[iter_index] = HashEntry(key, value)
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes table to new_capacity.
        First checks if given new_capacity is < current size (amount of elements), returns if true.
        Sets new_capacity to next prime number of given new_capacity (if not already prime).
        Creates new_capacity amount of buckets containing None stored in a Dynamic Array ADT.
        Saves old buckets and updates data members to reflect new values.
        Copies/inserts old buckets and entries into updated structure.
        """

        if new_capacity < self._size:
            return

        # create new capacity of next prime number from given value
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # append new_capacity amount of new empty buckets
        # each bucket is None, but will be a HashEntry, that is stored in a Dynamic Array ADT
        new_buckets = DynamicArray()
        for bucket in range(new_capacity):
            new_buckets.append(None)

        # save old buckets, update data members
        old_buckets = self._buckets
        self._buckets = new_buckets
        self._capacity = new_capacity
        self._size = 0

        # copy/insert old_buckets and entries
        # 'put' function performs quadratic probing
        for idx in range(old_buckets.length()):
            entry = old_buckets[idx]
            if entry and not entry.is_tombstone:
                self.put(entry.key, entry.value)

    def table_load(self) -> float:
        """
        Load factor = total number of elements stored in table / number of buckets
        """

        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Counts number of empty buckets, checking to see if each bucket (HashEntry) is None or is tombstone
        Returns total count of empty buckets.
        """

        count = 0
        for idx in range(self._capacity):
            if self._buckets[idx] is None or self._buckets[idx].is_tombstone:
                count += 1
        return count

    def get(self, key: str) -> object:
        """
        If key found at bucket with quadratic probing, returns value of entry with key/value pair.
        Otherwise, returns None.
        """

        initial_index = self._hash_function(key) % self._capacity
        iter_index = initial_index
        count = 0

        while self._buckets[iter_index] is not None:
            if (self._buckets[iter_index].key == key) and not self._buckets[iter_index].is_tombstone:
                return self._buckets[iter_index].value
            count += 1
            iter_index = (initial_index + count ** 2) % self._capacity
        return None

    def contains_key(self, key: str) -> bool:
        """
        Checks to see if bucket exists with key using quadratic probing.
        Returns Boolean.
        """

        if self._size == 0:
            return False

        initial_index = self._hash_function(key) % self._capacity
        iter_index = initial_index
        count = 0

        while self._buckets[iter_index]:
            if (self._buckets[iter_index].key == key) and not self._buckets[iter_index].is_tombstone:
                return True
            count += 1
            iter_index = (initial_index + count ** 2) % self._capacity
        return False

    def remove(self, key: str) -> None:
        """
        Performs quadratic probing to find bucket with entry containing key.
        If found, sets is_tombstone data member of entry to True, and decrements size.
        """

        initial_index = self._hash_function(key) % self._capacity
        iter_index = initial_index
        count = 0

        while self._buckets[iter_index]:
            if (self._buckets[iter_index].key == key) and not self._buckets[iter_index].is_tombstone :
                self._buckets[iter_index].is_tombstone = True
                self._size -= 1
                return
            count += 1
            iter_index = (initial_index + count ** 2) % self._capacity

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns dynamic array, which is a list of tuples with key/value pairs of the HashEntry within each bucket.
        """

        da = DynamicArray()

        for idx in range(self._capacity):
            entry = self._buckets[idx]
            if entry and not entry.is_tombstone:
                da.append((entry.key, entry.value))
        return da

    def clear(self) -> None:
        """
        Clears each bucket to be None, and sets the size data member to 0.
        """

        self._buckets = DynamicArray()

        for idx in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def __iter__(self):
        """
        Initializes a data member _iter_index to 0, so that iteration can be performed.
        Returns self.
        """

        self._iter_index = 0
        return self

    def __next__(self):
        """
        Iterates self._iter_index while it is less than capacity.
        Checks each bucket, and increment self._iter_index data member.
        if HashEntry exists and is not tombstone, returns the entry.
        Raise StopIteration once all buckets checked.
        """

        while self._iter_index < self._capacity:
            entry = self._buckets[self._iter_index]
            self._iter_index += 1
            if entry and not entry.is_tombstone:
                return entry
        raise StopIteration

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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
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

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

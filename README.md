# HashMap Implementation

## Overview

This project implements two types of hash maps: Separate Chaining HashMap and Open Addressing HashMap. These data structures are used to store key-value pairs and provide efficient operations for insertion, deletion, and lookup.

## Key Concepts

### Dynamic Array

The `DynamicArray` class is a custom implementation of a dynamic array that supports the following methods:
- `append(value)`: Adds a new element at the end of the array.
- `pop()`: Removes and returns the element from the end of the array.
- `swap(i, j)`: Swaps the elements at indices `i` and `j`.
- `get_at_index(index)`: Returns the value at the specified index.
- `set_at_index(index, value)`: Sets the value at the specified index.
- `length()`: Returns the length of the array.

### Hash Functions

Two hash functions are provided to compute the hash value of a given key:
- `hash_function_1(key)`: Computes the hash value by summing the ASCII values of the characters in the key.
- `hash_function_2(key)`: Computes the hash value by summing the product of the character's ASCII value and its position in the key.

### Separate Chaining HashMap

The `HashMap` class in `hash_map_sc.py` implements a hash map using separate chaining for collision resolution. Key concepts include:
- **Buckets**: Each bucket is a linked list that stores key-value pairs.
- **Insertion**: New key-value pairs are inserted into the appropriate bucket based on the hash value of the key.
- **Collision Resolution**: Collisions are resolved by adding the new key-value pair to the linked list at the corresponding bucket.
- **Resizing**: The hash map is resized when the load factor exceeds a certain threshold to maintain efficient operations.

### Open Addressing HashMap

The `HashMap` class in `hash_map_oa.py` implements a hash map using open addressing with quadratic probing for collision resolution. Key concepts include:
- **Buckets**: Each bucket stores a single key-value pair or a tombstone indicating a deleted entry.
- **Insertion**: New key-value pairs are inserted into the appropriate bucket based on the hash value of the key. Quadratic probing is used to find an empty bucket in case of collisions.
- **Collision Resolution**: Collisions are resolved by probing the next available bucket using a quadratic function.
- **Resizing**: The hash map is resized when the load factor exceeds a certain threshold to maintain efficient operations.

### Linked List

The `LinkedList` class is used in the separate chaining hash map to store key-value pairs in each bucket. Key methods include:
- `insert(key, value)`: Inserts a new node with the given key and value at the front of the list.
- `remove(key)`: Removes the node with the specified key from the list.
- `contains(key)`: Checks if a node with the specified key exists in the list.
- `length()`: Returns the length of the list.

### Hash Entry

The `HashEntry` class is used in the open addressing hash map to store key-value pairs. Each entry also has a `is_tombstone` attribute to indicate if the entry has been logically deleted.

## Usage

The hash maps can be used to store and retrieve key-value pairs efficiently. The provided test cases in the `if __name__ == "__main__":` block demonstrate the usage of various methods and functionalities of the hash maps.

## Conclusion

This project demonstrates the implementation of hash maps using two different collision resolution techniques: separate chaining and open addressing. The key concepts and data structures used in this project provide a solid foundation for understanding hash maps and their operations.
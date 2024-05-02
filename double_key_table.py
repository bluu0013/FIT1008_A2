from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')


class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:
        if sizes is not None:
            self.TABLE_SIZES = sizes

        if internal_sizes is not None:
            self.internal_sizes = internal_sizes
        else:
            self.internal_sizes = self.TABLE_SIZES

        self.size_index = 0
        self.array: ArrayR[tuple[K1, V] | None] | None = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31417
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31417
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2 | None, is_insert: bool) -> tuple[int, int] | int:
        """
        Find the correct position for this key in the hash table using linear probing.

        :Best case complexity: O(hash1(key1)) when key2 is None, and the first position is available.
        :Worst case complexity: O((hash1(key1) + N) * (hash2(key2) + M)) when for both positions, the whole
                                table needs to be probed. N is the Outer table size, and M is the Inner table size.
        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        pos1 = self.hash1(key1)
        
        if key2 is None:
            for _ in range(self.table_size):
                if self.array[pos1] is None:
                    if is_insert:
                        return pos1
                    else:
                        raise KeyError(key1)
                elif self.array[pos1][0] == key1:
                    return pos1
                else:
                    pos1 = (pos1 + 1) % self.table_size
        else:
            for _ in range(self.table_size):
                if self.array[pos1] is None:
                    if is_insert:
                        self.array[pos1] = (key1, LinearProbeTable(self.internal_sizes))
                        sub_table = self.array[pos1][1]
                        sub_table.hash = lambda k, tab = sub_table: self.hash2(k, tab)
                        pos2 = sub_table._linear_probe(key2, is_insert)
                        return (pos1, pos2)
                    else:
                        raise KeyError(key1)
                elif self.array[pos1][0] == key1:
                    sub_table = self.array[pos1][1]
                    pos2 = sub_table._linear_probe(key2, is_insert)
                    return (pos1, pos2)
                else:
                    pos1 = (pos1 + 1) % self.table_size

        if is_insert:
            raise FullError("Outer Table is Full")
        else:
            raise KeyError(key1)

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.

        :Best case complexity: O(N) when key is None. N is the Outer table size.
        :Worst case complexity: O(linear_probe(key) + N) when key is not None. N is the Outer table size.
        """
        res = []
        if key is not None:
            pos1 = self._linear_probe(key, None ,False)
            sub_table = self.array[pos1][1]
            for i in range(sub_table.table_size):
                if sub_table.array[i] is not None:
                    res.append(sub_table.array[i][0])   
        else:
            for i in range(self.table_size):
                if self.array[i] is not None:
                    res.append(self.array[i][0])

        res.reverse()

        def KeysGen():
            for _ in res:
                yield res
            return

        return KeysGen()

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        :Best case complexity: O(linear_probe(key) + N) when key is not None. N is the Outer table size.
        :Worst case complexity: O(N * M) when key is None. N is the Outer table size,
                                and M is the Inner table size.
        """
        res = []
        if key is not None:
            pos1 = self._linear_probe(key, None ,False)
            sub_table = self.array[pos1][1]
            for i in range(sub_table.table_size):
                if sub_table.array[i] is not None:
                    res.append(sub_table.array[i][1])    
        else:
            for i in range(self.table_size):
                if self.array[i] is not None:
                    for j in range(self.array[i][1].table_size):
                        if self.array[i][1].array[j] is not None:
                            res.append(self.array[i][1].array[j][1])

        res.reverse()

        def ValuesGen():
            for _ in res:
                yield res
            return

        return ValuesGen()

    def keys(self, key: K1 | None = None) -> list[K1 | K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        :complexity: See iter_keys.
        """
        if key is not None:
            keyIter = self.iter_keys(key) 
        else:
            keyIter = self.iter_keys()

        return next(keyIter)

    def values(self, key: K1 | None = None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        :complexity: See iter_values.
        """
        res = []
        if key is not None:
            valueIter = self.iter_values(key)
            res = next(valueIter)

        else:
            valueIter = self.iter_values()
            res = next(valueIter)

        return res 

    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """

        position1, position2 = self._linear_probe(key[0], key[1], False)
        return self.array[position1][1].array[position2][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        key1, key2 = key
        position1, position2 = self._linear_probe(key1, key2, True)
        sub_table = self.array[position1][1]

        if sub_table.is_empty():
            self.count += 1

        sub_table[key2] = data

        # resize if necessary
        if len(self) > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :complexity: O(linear_probe(key1, key2) + M) where M is the Inner table size.
        :raises KeyError: when the key doesn't exist.
        """
        pos1, pos2 = self._linear_probe(key[0],key[1], False)
        
        self.array[pos1][1].array[pos2] = None
        self.count -= 1

        empty = True
        for i in range(self.array[pos1][1].table_size):
            if self.array[pos1][1].array[i] != None:
                empty = False
        
        if empty:
            self.array[pos1] = None

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        old_arr = self.array
        self.size_index += 1
        if self.size_index >= len(self.TABLE_SIZES):
            return
        
        self.array = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

        for x in old_arr:
            if x is not None:
                key1, value1 = x
                pos1 = self.hash1(key1)
                self.array[pos1] = (key1, LinearProbeTable(self.TABLE_SIZES))
                sub_table = self.array[pos1][1]
                sub_table.hash = lambda k, tab = sub_table: self.hash2(k, tab)
                for y in value1.array:
                    if y is not None:
                        key2, value2 = y
                        self[key1, key2] = value2

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        :complexity: O(N * M) where N is the Outer table sizes and M is the Inner table sizes
        """
        result = ""
        for item in self.array:
            if item is not None:
                (key, value) = item
                result += "(" + str(key) + ": [" 
                for item2 in value.array:
                    if item2 is not None:
                        (key2, value2) = item2
                        result += "(" + str(key2) + ", " + str(value2) + ")"
                result += "]\n"
        return result
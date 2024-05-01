from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")


class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self, level: int = 0) -> None:
        self.array: ArrayR[tuple[K, V] | None] = ArrayR(self.TABLE_SIZE)
        self.count = 0
        self.level = level
    
    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        pos = self.hash(pos)

        if self.array[pos] is None:
            raise KeyError(key)
        else:
            if self.array[pos][0] == key:
                return self.array[pos][1]
            else:
                sub_table = self.array[pos][1]
                return sub_table[key]

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        pos = self.hash(key)
        self.count += 1

        if self.array[pos] is None:
            self.array[pos] = (key,value)
        else:
            old_key, old_value  = self.array[pos]
            new_level = self.level + 1
            self.array[pos] = (key[self.level], InfiniteHashTable(new_level))
            sub_table = self.array[pos][1]
            sub_table[old_key] = old_value
            sub_table[key] = value          

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        pos = self.hash(key)
        self.count -= 1

        if self.array[pos] is None:
            raise KeyError(key)
        else:
            if self.array[pos][0] == key:
                self.array[pos] = None
            else:
                sub_table = self.array[pos][1]
                del sub_table[key]

    def __len__(self) -> int:
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()

    def get_location(self, key) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        res = []
        pos = self.hash(key)

        if self.array[pos] is None:
            raise KeyError(key)
        else:
            res.append(pos)
            if self.array[pos][0] == key:
                return res
            else:
                sub_table = self.array[pos][1]
                return res + sub_table.get_location(key)

    def __contains__(self, key: K) -> bool:
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

    def sort_keys(self, current=None) -> list[str]:
        """
        Returns all keys currently in the table in lexicographically sorted order.
        """
        raise NotImplementedError()

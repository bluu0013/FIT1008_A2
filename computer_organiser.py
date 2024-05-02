from __future__ import annotations
from computer import Computer
from algorithms.mergesort import *
from algorithms.binary_search import *

class ComputerOrganiser:

    def __init__(self) -> None:
        self.computers = []

    def cur_position(self, computer: Computer) -> int:
        """
        Uses binary search to find the index of the given computer in the list.
        Will raise exception if computer does not exist in current list.

        :complexity: O(log(N)) where N is the length of current list of computers.
        """
        res = binary_search(self.computers, computer)
        try:
            if self.computers[res] == computer:
                return res
            else:
                raise KeyError(computer)
        except:
            raise KeyError(computer)

    def add_computers(self, computers: list[Computer]) -> None:
        """
        Adds new computers to list, then uses mergesort to rank them.

        :complexity: O( (M+N)*(log(M+N)) ) where M is the length of the input
                                            and N is the length of the current list
        """
        for i in computers:
            self.computers.append(i)

        self.computers = mergesort(self.computers)
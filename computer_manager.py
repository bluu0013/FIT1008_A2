from __future__ import annotations
from computer import Computer
from computer_organiser import ComputerOrganiser
from data_structures.hash_table import LinearProbeTable


class ComputerManager:

    def __init__(self) -> None:
        self.organiser = ComputerOrganiser()
        self.count = 0

    def add_computer(self, computer: Computer) -> None:
        """
        Adds new computers to list, utilising computer_organiser class to sort once added.

        :complexity: O(Nlog(N)) where N is the length of the list.
        """
        self.organiser.add_computers([computer])

    def remove_computer(self, computer: Computer) -> None:
        """
        Removes given computer from the list.

        :complexity: O(N) where N is the length of the current computer list.
        """
        self.organiser.computers.remove(computer)
        self.count -= 1

    def edit_computer(self, old: Computer, new: Computer) -> None:
        """
        Removes old computer, then add new computer.

        :complexity: O(N + Nlog(N)) where N is the length of the current computer list.
        """
        self.remove_computer(old)
        self.add_computer(new)

    def computers_with_difficulty(self, diff: int) -> list[Computer]:
        """
        Searches for all computers with given difficulty.

        :complexity: O(N) where N is the length of the current computer list.
        """
        res = []
        for i in self.organiser.computers:
            if i.hacking_difficulty == diff:
                res.append(i)
        return res
    
    def group_by_difficulty(self) -> list[list[Computer]]:
        """
        Group same difficulty value computers into a list, then compiles lists to make
        a list of lists, order by lowest difficulty to highest.

        :complexity: O(N) where N is the length of the current computer list.
        """
        comp_copy = []
        res = []
        for i in self.organiser.computers:
            comp_copy.append(i)

        while len(comp_copy) > 0:
            curr_diff = comp_copy[0].hacking_difficulty
            curr_list = self.computers_with_difficulty(curr_diff)
            for i in curr_list:
                if i in comp_copy:
                    comp_copy.remove(i)
            res.append(curr_list)
            
        return res
        

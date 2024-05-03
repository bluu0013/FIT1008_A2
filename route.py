from __future__ import annotations
from dataclasses import dataclass

from computer import Computer

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from virus import VirusType


@dataclass
class RouteSplit:
    """
    A split in the route.
       _____top______
      /              \
    -<                >-following-
      \____bottom____/
    """

    top: Route
    bottom: Route
    following: Route

    def remove_branch(self) -> RouteStore:  #leaves the top of a split and should just remove a series.
        """Removes the branch, should just leave the remaining following route."""
        
        noBranch = RouteSeries(self.following.store.computer, self.following.store.following) 

        return noBranch
        

        


@dataclass
class RouteSeries:
    """
    A computer, followed by the rest of the route

    --computer--following--

    """

    computer: Computer
    following: Route

    def remove_computer(self) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Removing the computer at the beginning of this series.
        """
        self.computer = None

        return self

    def add_computer_before(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer in series before the current one.
        """
        
        newComputer = RouteSeries(computer, Route(self.computer))
        

        return self

    def add_computer_after(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer after the current computer, but before the following route.
        """
        theSecondComputer = RouteSeries(computer, Route(None))
        self.following = Route(theSecondComputer)

        return self
    

    def add_empty_branch_before(self) -> RouteStore:
        """Returns a route store which would be the result of:
        Adding an empty branch, where the current routestore is now the following path.
        """
        curr = RouteSeries(self.computer, self.following)

        return RouteSplit(None, None, curr)        

    def add_empty_branch_after(self) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding an empty branch after the current computer, but before the following route.
        """
        emptyBranch = RouteSplit(None, None, None)
        self.following = Route(emptyBranch)

        return self


RouteStore = Union[RouteSplit, RouteSeries, None]


@dataclass
class Route:

    store: RouteStore 

    def add_computer_before(self, computer: Computer) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding a computer before everything currently in the route.
        """
        theComputer = RouteSeries(computer, Route(None))
        
        return Route(theComputer)



    def add_empty_branch_before(self) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding an empty branch before everything currently in the route.
        """
        theEmptyBranch = RouteSplit(Route(None), Route(None), Route(None))

        return Route(theEmptyBranch)


def follow_path(self, virus_type: VirusType) -> None:
    """Follow a path and add computers according to a virus_type."""
        #the time complexity is O(n + m) where n is the amount of branches and m is the amount of computers

    while self.store.following != None: 
        if self.store.following == RouteSeries:
            virus_type.add_computer(self.store.computer)
            virus_type.select_branch(self.store.following, None)
        elif self.store.following == RouteSplit:
            self.follow_path_split_solution(virus_type)
            virus_type.select_branch(self.store.top,self.store.bottom)
                

                


def follow_path_split_solution(self, virus_type: VirusType) -> None:
        
    if self.store.following.store == RouteSeries:
        virus_type.add_computer(self.store.following.store.computer)

    elif self.store.following.store== RouteSplit: 
        virus_type.select_branch(self.store.following.store.top , self.store.following.store.bottom)
        self.follow_path_split_solution(self.store.following,virus_type)
            
            
        

def add_all_computers(self) -> list[Computer]:
    """Returns a list of all computers on the route."""
    #O(n) where n is the amount of branches traversed
    
    added_computers = list                              
    branch = self.store

    if type(branch.following.store) == None:
        
        return added_computers.append(branch.computer)
    
    elif type(branch.following.store) == RouteSeries:
        added_computers.append(branch.computer)
        branch = branch.following
        added_computers.extend(self.add_all_computers)
    else:
        added_computers.append(branch.following.store.top.store.computer)
        added_computers.append(branch.following.store.bottom.store.computer)
        branch = branch.following
        added_computers.extend(self.add_all_computers)
    
    
    return added_computers
    

        

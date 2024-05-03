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
        
        newRouteStore = RouteStore(self.top)

        return newRouteStore
        

        


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

        return RouteStore

    def add_computer_before(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer in series before the current one.
        """
        theSecondComputer = RouteSeries(self.computer,self.following)

        fullRoute = RouteSeries(computer,theSecondComputer)

        return fullRoute

    def add_computer_after(self, computer: Computer) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding a computer after the current computer, but before the following route.
        """
        theFirstComputer = RouteSeries(self.computer,self.following)

        fullRoute = RouteSeries(computer,theFirstComputer)

        return fullRoute

    def add_empty_branch_before(self) -> RouteStore:
        """Returns a route store which would be the result of:
        Adding an empty branch, where the current routestore is now the following path.
        """
        theSeriesRoute = RouteSeries(self.computer,self.following)

        theAddedBranch = RouteSeries(None,theSeriesRoute)

        return theAddedBranch

    def add_empty_branch_after(self) -> RouteStore:
        """
        Returns a route store which would be the result of:
        Adding an empty branch after the current computer, but before the following route.
        """
        

        theHead = RouteSeries(self.computer,emptybranch)

        thefollowing = RouteSeries(None,self.following)

        emptybranch = RouteSeries(None,thefollowing)

        

        return theHead


RouteStore = Union[RouteSplit, RouteSeries, None]


@dataclass
class Route:

    store: RouteStore = None

    def add_computer_before(self, computer: Computer) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding a computer before everything currently in the route.
        """
        theComputer = RouteSeries(computer,None)

        return Route(theComputer,self.store)



    def add_empty_branch_before(self) -> Route:
        """
        Returns a *new* route which would be the result of:
        Adding an empty branch before everything currently in the route.
        """
        theEmptyBranch = RouteSeries

        return Route(theEmptyBranch,self.store)

    def follow_path(self, virus_type: VirusType) -> None:
        """Follow a path and add computers according to a virus_type."""
        #the time complexity is O(n + m) where n is the amount of branches and m is the amount of computers

        while type(self.store.following) != None: 
            
            virus_type.add_computer
            virus_type.select_branch
        



    def add_all_computers(self) -> list[Computer]:
        """Returns a list of all computers on the route."""
        #O(n) where n is the amount of branches traversed
        
        added_computers = list                              
        branch = self.store

        if type(branch.following) == None:
            
            return added_computers.append(branch.computer)
        
        else:
            added_computers.append(branch.computer)
            branch = branch.following
            added_computers.extend(self.add_all_computers)
        
        """
        this is for if the list needs no nones in it but otherwise use added_computer 
        no_nones_added_computers = list

        for element in added_computers:         #O(n) where n is the length of added computers
            if element != None:
                no_nones_added_computers.append(element)
        return no_nones_added_computers
                
        """
        return added_computers
    

        

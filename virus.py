from __future__ import annotations
from abc import ABC, abstractmethod
from computer import Computer
from route import Route, RouteSeries, RouteSplit
from branch_decision import BranchDecision
from data_structures.stack_adt import Stack

#if unspecified then the complexity for that line is O(1)


class VirusType(ABC):

    def __init__(self) -> None:
        self.computers = []

    def add_computer(self, computer: Computer) -> None:
        self.computers.append(computer)

    @abstractmethod
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        
        pass

class TopVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        # Always select the top branch
        return BranchDecision.TOP


class BottomVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        # Always select the bottom branch
        return BranchDecision.BOTTOM


class LazyVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        Try looking into the first computer on each branch,
        take the path of the least difficulty.
        """
        top_route = type(top_branch.store) == RouteSeries
        bot_route = type(bottom_branch.store) == RouteSeries

        if top_route and bot_route:
            top_comp = top_branch.store.computer
            bot_comp = bottom_branch.store.computer

            if top_comp.hacking_difficulty < bot_comp.hacking_difficulty:
                return BranchDecision.TOP
            elif top_comp.hacking_difficulty > bot_comp.hacking_difficulty:
                return BranchDecision.BOTTOM
            else:
                return BranchDecision.STOP
        # If one of them has a computer, don't take it.
        # If neither do, then take the top branch.
        if top_route:
            return BranchDecision.BOTTOM
        return BranchDecision.TOP


class RiskAverseVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        This virus is risk averse and likes to choose the path with the lowest risk factor.
        """
        #all lines in this class are O(1)

        top_route = type(top_branch.store)                                  
        bot_route = type(bottom_branch.store) 
        top_comp = top_branch.store.computer
        bot_comp = bottom_branch.store.computer
        
        
        if (top_route == RouteSplit and bot_route != RouteSplit):
            return BranchDecision.TOP
        if (top_route != RouteSplit and bot_route == RouteSplit):
            return BranchDecision.BOTTOM
        
        if (top_comp.risk_factor == 0.0 and bot_comp.risk_factor != 0.0):
            return BranchDecision.TOP
        if (bot_comp.risk_factor == 0.0 and top_comp.risk_factor != 0.0):
            return BranchDecision.BOTTOM
        
        if top_comp.risk_factor == 0.0 and bot_comp.risk_factor == 0.0:
            
            if top_comp < bot_comp:
                return BranchDecision.TOP
            
            if bot_comp.hacking_difficulty < top_comp.hacking_difficulty:
                return BranchDecision.BOTTOM
            
            if top_comp.hacking_difficulty == bot_comp.hacking_difficulty:

                top_hacked_combine = top_comp.hacking_difficulty + top_comp.hacked_value/2 
                bot_hacked_combine = bot_comp.hacking_difficulty + bot_comp.hacked_value/2

                if top_comp.risk_factor > 0:
                
                    top_hack_risk_combine = top_hacked_combine / top_comp.risk_factor

                    if top_hack_risk_combine > bot_hack_risk_combine:
                    
                        return BranchDecision.TOP

                if bot_comp.risk_factor > 0:

                    bot_hack_risk_combine = bot_hacked_combine / bot_comp.risk_factor
                    
                    if bot_hack_risk_combine > top_hack_risk_combine:

                        return BranchDecision.BOTTOM
                   
               
                    if top_hack_risk_combine == bot_hack_risk_combine:
        
                        if top_comp.risk_factor < bot_comp.risk_factor:
                            return BranchDecision.TOP
                        if bot_comp.risk_factor < top_comp.risk_factor:
                            return BranchDecision.BOTTOM
                
                    return BranchDecision.STOP

        return BranchDecision.TOP
            


class FancyVirus(VirusType):
    CALC_STR = "7 3 + 8 - 2 * 2 /"

    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        This virus has a fancy-pants and likes to overcomplicate its approach.
        """
        #unless specified the lines have a time complexity of O(1)

        calc_string = FancyVirus.CALC_STR

        calc_string_list = calc_string.split()  #O(n) where n is the length of the input string (calc_string)

        temp_stack = Stack

        for element in calc_string_list:        #O(n) where n is the length of the input string (calc_string)

            if element not in "/*+-":
                temp_stack.push(int(element))
            
            else:
                right = temp_stack.pop() 
                left = temp_stack.pop() 
                    
                
                if element == '+': 
                    temp_stack.push(left + right) 
                    
                elif element == '-': 
                    temp_stack.push(left - right) 
                    
                elif element == '*': 
                    temp_stack.push(left * right) 
                    
                elif element == '/': 
                    temp_stack.push(int(left / right)) 
                
            
        threshold =  temp_stack.pop() 


        top_route = type(top_branch.store) 
        bot_route = type(bottom_branch.store) 
        top_comp = top_branch.store.computer
        bot_comp = bottom_branch.store.computer
        
        if (top_route == RouteSplit and bot_route != RouteSplit):
            return BranchDecision.TOP
        if (top_route != RouteSplit and bot_route == RouteSplit):
            return BranchDecision.BOTTOM
        
        if top_comp != None and bot_comp != None:


            if top_comp.hacked_value < threshold:
                BranchDecision.TOP

            if bot_comp.hacked_value > threshold:   
                BranchDecision.BOTTOM
            
            return BranchDecision.STOP
        
        return BranchDecision.TOP

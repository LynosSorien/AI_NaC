# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 23:07:07 2013

@author: David Jorquera Abellan
"""
'''
 Some objects and functions usefull for this project.
'''
class State:
    def __init__(self, grid):
        self.grid = grid
    
    def getGrid(self):
        return self.grid
        
    def setGrid(self,grid):
        self.grid = grid
    
    def __hash__(self):
        val = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                val+=((10*i)+j)*abs(self.grid[i][j])
        return val


def getLegalActions(grid):
    actions = []
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == 0:
                actions.append((i,j))
    return actions

class Grid:
    def __init__(self):
        self.grid = []
        for i in range(0,3):
            self.grid.append([0])
            for j in range(0,2):
                self.grid[i].append(0)
    
    def getGrid(self):
        return self.grid
    
    def placeMovement(self, i,j,value):
        self.grid[i][j] = value
        
    def unplaceMovement(self,i,j):
        self.grid[i][j] = 0
    
    def legalActions(self):
        actions = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j] == 0:
                    actions.append((i,j))
        return actions
    
    def restart(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                self.grid[i][j] = 0
    
    def isTerminalState(self):
        value = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                value+= self.grid[i][j]
            if value == 3 or value == -3:
                return True
            value = 0
        # Now, we will search for the crosses
        for i in range(len(self.grid)):
            value+=self.grid[i][i]
        if value == 3 or value == -3:
            return True
        value = 0
        j = 0
        for i in range(len(self.grid)-1,-1,-1):
            value += self.grid[i][j]
            j+=1
        if value == 3 or value == -3:
            return True
        for j in range(len(self.grid)):
            value = 0
            for i in range(len(self.grid)):
                value+=self.grid[i][j]
            if value == 3 or value == -3:
                return True
        return False
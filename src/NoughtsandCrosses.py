# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 22:59:06 2013

@author: David Jorquera Abellan
"""
from Tkinter import *
import cPickle as pickle
import os.path
import utils
import QLearningAgent
import copy


class NoughtAndCrosses:
    def __init__(self):
        self.WIN_REWARD = 1
        self.LOSE_REWARD = -1
        self.DRAW_REWARD = 0.5
        self.turn = -1
        self.AI = -1
        self.player = self.AI*-1
        self.path = ""
        self.decideFirst()
        self.agent = QLearningAgent.QLearningAgent()
        self.loadLearning()
        self.grid = utils.Grid()
        self.game = False
        self.paction = None
        self.state = utils.State(self.grid.getGrid())
        self.nstate = utils.State(self.grid.getGrid())
        """
        INIT the TKInter interface for NaC game.
        """
        self.root = Tk()
        self.root.geometry(newGeometry = "300x300")
        self.root.title("Noughts and Crosses")
        
        c00 = Button(self.root,command=lambda:self.play(0,0))
        c00.grid(row=1,column=1)
        c00.config(height = 5, width = 10)
        c01 = Button(self.root,command=lambda:self.play(0,1))
        c01.grid(row=1,column=2)
        c01.config(height = 5, width = 10)
        c02 = Button(self.root,command=lambda:self.play(0,2))
        c02.grid(row=1,column=3)
        c02.config(height = 5, width = 10)
        
        c10 = Button(self.root,command=lambda:self.play(1,0))
        c10.grid(row=2,column=1)
        c10.config(height = 5, width = 10)
        c11 = Button(self.root,command=lambda:self.play(1,1))
        c11.grid(row=2,column=2)
        c11.config(height = 5, width = 10)
        c12 = Button(self.root,command=lambda:self.play(1,2))
        c12.grid(row=2,column=3)
        c12.config(height = 5, width = 10)
        
        c20 = Button(self.root,command=lambda:self.play(2,0))
        c20.grid(row=3,column=1)
        c20.config(height = 5, width = 10)
        c21 = Button(self.root,command=lambda:self.play(2,1))
        c21.grid(row=3,column=2)
        c21.config(height = 5, width = 10)
        c22 = Button(self.root,command=lambda:self.play(2,2))
        c22.grid(row=3,column=3)
        c22.config(height = 5, width = 10)
        
        self.buttons = []
        self.buttons.append([])
        self.buttons.append([])
        self.buttons.append([])
        
        self.buttons[0].append(c00)
        self.buttons[0].append(c01)
        self.buttons[0].append(c02)
        
        self.buttons[1].append(c10)
        self.buttons[1].append(c11)
        self.buttons[1].append(c12)
        
        self.buttons[2].append(c20)
        self.buttons[2].append(c21)
        self.buttons[2].append(c22)
        
        self.restart = Button(self.root,command=lambda:self.restartGame(),text="Restart")
        self.restart.grid(row=4,column=2)
        self.restart.config(bg = "gray")
        
        self.learnlabel = Label(self.root,text=self.path)
        self.learnlabel.grid(row=4,column=3)
        
        self.initGame() # Starts the game       
        
        self.root.mainloop()
    
    '''
     View who will play first, and loads the learning vector for attack, or defend.
    '''
    def decideFirst(self):
        self.turn = -1
        self.AI *=-1
        self.player = self.AI*-1
        if self.turn != self.AI:
            self.path = "learningD.dat"
        else:
            self.path = "learningA.dat"
        
    '''
     The player places a movement.
    '''
    def play(self, i,j):
        if not self.game:
            return -2
        if self.turn!= self.player:
            return -1
        cgrid = copy.deepcopy(self.grid)
        flag = False
        if self.turn<0:
            if (i,j) in self.grid.legalActions():
                self.grid.placeMovement(i,j,-1)
                self.buttons[i][j].configure(bg="red")
            else:
                flag = True
        else:
            if (i,j) in self.grid.legalActions():
                self.grid.placeMovement(i,j,1)
                self.buttons[i][j].configure(bg="blue")
            else:
                flag = True
        if not flag:
            if self.grid.isTerminalState() or len(self.grid.legalActions()) == 0:
                cgrid.unplaceMovement(self.paction[0],self.paction[1]) # Unplace the movements to add value to the final state
                if len(self.grid.legalActions()) == 0 and not self.grid.isTerminalState():
                    self.updateAgent(cgrid.getGrid(),self.paction,self.grid.getGrid(),self.DRAW_REWARD)
                else :
                    self.updateAgent(cgrid.getGrid(),self.paction,self.grid.getGrid(),self.LOSE_REWARD) # The previous movement was bad, get LOSE REWARD
                    c2grid= copy.deepcopy(cgrid)
                    c2grid.placeMovement(i,j,self.AI)
                    self.updateAgent(cgrid.getGrid(),(i,j),c2grid.getGrid(),self.DRAW_REWARD) # Add reward to the movement that it doesn't placed
                self.hasVictory() # View if we won the game
                self.saveLearning()
                self.turn*=-1
            else:
                self.turn*=-1
                self.AITurn()
        return 0

    '''
     AI Turn, prepares the AI to choose the movement. It will get the movement
     from the policy that she is creating with the rewards obtained before from
     the previous games. Every state, will have a value as reward. The AI will choose
     the highs values.
    '''
    def AITurn(self):
        self.state.setGrid(self.grid.getGrid())
        action = self.agent.getPolicy(self.state)
        cgrid = copy.deepcopy(self.grid)
        self.AIGame(action[0],action[1]) # Plays the move
        rw = 0 # Set the reward as 0
        if self.grid.isTerminalState(): # If the game ends with the last move it will mean that the AI won or is a draw game.
            rw = self.WIN_REWARD
        if len(self.grid.legalActions()) == 0: # Draw game
            rw=self.DRAW_REWARD
        self.updateAgent(cgrid.getGrid(),action,self.grid.getGrid(),rw) # Update the reward of the state.
        if rw!=0:
            self.saveLearning() # IF the AI obtain reward it means that the game is over, time to save the learning vector.
    
    '''
     The AI plays her move to i,j place.
    '''
    def AIGame(self,i,j):
        if not self.game:
            return -2
        if self.turn!=self.AI:
            return -1
        flag = False
        if self.turn<0:
            if (i,j) in self.grid.legalActions():
                self.grid.placeMovement(i,j,-1)
                self.buttons[i][j].configure(bg="red")
            else:
                flag = True
        else:
            if (i,j) in self.grid.legalActions():
                self.grid.placeMovement(i,j,1)
                self.buttons[i][j].configure(bg="blue")
            else:
                flag = True
        if not flag:
            self.hasVictory()
            self.paction = (i,j)
            self.turn*=-1
        
    def hasVictory(self):
        if self.grid.isTerminalState():
            self.game = False
            if self.turn == self.AI:
                print "The winner is the AI!"
            else:
                print "You are the winner!"
            return 0
        if len(self.grid.legalActions()) == 0:
            self.game = False
            print "Draw game!"
        return 0
        
    
    def initGame(self):
        self.game = True
    
    def loadLearning(self):
        """
        self.agent.loadLearning("learning.dat")
        learning = self.agent.learning
        for learn in learning:
            print learning[(learn[0],learn[1])],
        """
        if not os.path.isfile(self.path):
            return -1
        else :
            f = open(self.path,'r')
            if f == None:
                return -3
            print "Load Learning from",self.path,"..."
            self.state = pickle.load(f)
            self.nstate = pickle.load(f)
            self.agent.learning = pickle.load(f)
            self.agent.n = pickle.load(f)
            f.close()
        for learn in self.agent.learning:
            print self.agent.learning[(learn[0],learn[1])],
        return 0
    def saveLearning(self):
        """
        self.agent.saveLearning("learning.dat")
        """
        f = open(self.path,"w")
        print "Saving Learning to",self.path,"..."
        pickle.dump(self.state,f)
        pickle.dump(self.nstate,f)
        pickle.dump(self.agent.learning,f)
        pickle.dump(self.agent.n,f)
        f.close();
        print "Saved!"
    
    '''
     This function is used to update the reward obtained by the AI agent
     using the action "action" in the state "state" to go to the "nextState".
     Rw = [S0,a,Si]
    '''
    def updateAgent(self, state, action, nextState, reward):
        self.state.setGrid(state)
        self.nstate.setGrid(nextState)
        self.agent.update(self.state,action,self.nstate,reward)
    
    def restartGame(self):
        if self.game:
            return -1
        print "Restarting..."
        self.grid.restart()
        for i in range(len(self.buttons)):
            for j in range(len(self.buttons)):
                self.buttons[i][j].config(bg = "white")
        self.game = True
        self.decideFirst()
        self.loadLearning()
        print ""
        print "--------------------INIT NEW GAME-----------------------"
        if self.turn == self.AI:
            self.AITurn()
        
        

def main():
    NaC = NoughtAndCrosses()

main()
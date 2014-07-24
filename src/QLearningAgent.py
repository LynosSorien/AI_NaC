# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 23:34:24 2013

@author: David Jorquera Abellan
"""
import cPickle as pickle
import random
import os.path
import utils
'''
 QLearning algorithm to let the AI of our Noughts and Crosses learn.
 This learning will be slow. Many times must play with the AI to view how she
 will learn and try to use the movements that has learned.
'''
class QLearningAgent:
    def __init__(self, epsilon = 0.9, alpha = 0.4):
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = 1
        self.n = 1
        self.increment = 0.05
        self.learning = dict()
        
    def getQValue(self,state,action):
        if (state.__hash__(),action) in self.learning:
            return self.learning[(state.__hash__(),action)]
        return 0
        
    def getValue(self,state):
        qvalues = []
        for action in utils.getLegalActions(state.getGrid()):
            qvalues.append(self.getQValue(state,action))
        print qvalues
        if len(qvalues)==0:
            return 0
        value = max(qvalues)
        return value

    '''
     Get the best actions according to the actual state "state".
     With some random chance it will explore other possibilites.
    '''
    def getPolicy(self,state):
        random_number = random.random()
        if random_number<self.gamma/self.n: # Exploration factor!
            print "Exploration"
            actions = []
            for action in utils.getLegalActions(state.getGrid()):
                actions.append(action)
            return random.choice(actions)
        
        value = self.getValue(state)
        actions = [] # We will save all actions that have an optimum value
        for action in utils.getLegalActions(state.getGrid()):
            if self.getQValue(state,action) == value:
                actions.append(action)
        if len(actions)==0:
            return None # If there is no action, then we will return None.
        return random.choice(actions) # We will return any of action with optimum value in order to explore.
    
    '''
     Updates the reward obtained in some state using some action. If this state doesn't
     exists, then it will be added.
     The table will save the pair state->action as a dictionary, where the pair state-action
     will be the key, and the reward the value.
    '''
    def update(self,state,action,nextState,reward):
        if not (state.__hash__(),action) in self.learning:
            print "Adding new Learning state"
            self.learning[(state.__hash__(),action)] = 0 # The states must have a hash function implementated.
        else :
            print "Learning",self.learning[(state.__hash__(),action)]
        a1 = 1-self.alpha
        val = self.getValue(nextState)
        self.learning[(state.__hash__(),action)] = a1*self.learning[(state.__hash__(),action)]+self.alpha*(reward+self.gamma*val)
        self.n+=self.increment
        print "New Value",self.learning[(state.__hash__(),action)]
    
    def loadLearning(self,path):
        if not os.path.isfile(path):
            f = open(path,'w')
            f.close()
        else :
            f = open(path,'r')
            if f == None:
                return -3
            print "Load Learning..."
            self.learning = pickle.load(f)
            self.n = pickle.load(f)
            f.close()
        return 0
        
    def saveLearning(self,path):
        f = open(path,"w")
        print "Saving Learning..."
        pickle.dump(self.learning,f)
        pickle.dump(self.n,f)
        f.close();
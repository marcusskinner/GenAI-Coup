# -*- coding: utf-8 -*-
"""
Created on Sun Feb  8 13:59:28 2026

@author: audrey
"""

class TurnAction:
    
    def __init__(self):
        self.action_map = {
            'income':self.income,
            'foreign_aid':self.foreign_aid,
            'coup':self.coup,
            'tax':self.tax,
            'assassinate':self.assassinate,
            'steal':self.steal,
            'exchange':self.exchange
            }
    
    # take 1 coin, no block, no challenge
    def income():
        pass
    
    # take two coins, block (Duke), no challenge
    def foreign_aid():
        pass
    
    # return 7 coins, no block, no challenge
    def coup():
        pass
    
    # take 3 coins, no block, yes challenge
    def tax():
        pass
    
    # exchange cards, no block, yes challenge
    def exchange():
        pass
    
    # remove 1 player's card, yes block, yes challenge
    def assassinate(opponent):
        pass
    
    # take 2 coins from opp, yes block, yes challenge
    def steal(opponent):
        pass
    
    
    

    
        
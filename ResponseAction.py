# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:57:29 2026

@author: audrey
"""

class ResponseAction:
    
    def __init__(self, player_name, action, response_name):
        # set properties
        self.player_name = player_name
        self.action = action
        self.response_name = response_name
        
        # [function, can_block, can_challenge]
        self.action_map = {
            'block': [self.block, False, False],
            'challenge': [self.challenge, True, False],
            'none':[None, False, False]}
         
        # 
        action_info = self.action_map.get(response_name, [None, False, False])
        self.func, self.can_chal, self.can_block = action_info
    
    
    def block(self):
        pass
    
    
    def challenge(self):
        pass
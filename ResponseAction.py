# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:57:29 2026

@author: audrey
"""

class ResponseAction:
    
    def __init__(self, player_name, action_name, claimed_card=None):
        # set properties
        self.player_name = player_name
        self.action_name = action_name
        self.claimed_card = claimed_card
        self.target_name = None        
        
        # [function, can_block, can_challenge]
        self.action_map = {
            'block': [self.block, False, True],
            'challenge': [self.challenge, False, False],
            'none':[None, False, False]}
         

        action_info = self.action_map.get(action_name, [None, False, False])
        self.func, self.can_block, self.can_chal = action_info
        self.summary = f"Player: {self.player_name}, Response: {self.action_name}"
        
        
    # block applies as long as it hasn't lost being challenged
    def block(self, game_state, blocker, blocked, lost_chal):
        if not lost_chal:
            print(f"{blocker.name} successfully blocks {self.action.player_name}'s {self.action.action_name} with {self.claimed_card}")
            return True
        else:
            print(f'{blocker.name} failed to block {self.action.player_name} with {self.claimed_card}')
            return False
    
            
    
    
    def challenge(self, game_state, challenger, blocked, lost_chal):
        # get action and challenged player name from action attribute
        action = self.action
        p_name = action.player_name
        chal_player = game_state.get_player(p_name)
        
        # if challenged, action player must have claimed a card
        claimed_card = action.claimed_card.capitalize() # fix capitalization
        player_cards = game_state.player_info[chal_player]['facedown']
        
        # if win challenge, replace card and challenger loses card
        if claimed_card in player_cards:
            game_state.replace_card(chal_player,claimed_card)
            game_state.lose_card(challenger)
            print(f"{chal_player.name} had {claimed_card}. {challenger.name} loses a Card")
            return False
        # if lose_challenge, lose card
        else:
            game_state.lose_card(chal_player)
            print(f"{chal_player.name} did not have {claimed_card} and loses a Card")
            return True
    
    
    # this is only relevant for block response
    def validate_claimed(self, action):
        # foreign aid only blocked by Duke
        if action.action_name == 'foreign aid':
            self.claimed_card = 'Duke'
            
        # assassinate only blocked by Contessa
        if action.action_name == 'assassinate':
            self.claimed_card = 'Contessa'
            
        # steal blocked by Captain or Ambassador
        if action.action_name=='steal':
            if self.claimed_card not in ['Captain', 'Ambassador']:
                # default to captial
                self.claimed_card = 'Captain'

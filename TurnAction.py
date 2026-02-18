class TurnAction:
    
    def __init__(self, player_name, action_name, target_name=None):
        # set properties
        self.player_name = player_name
        self.action_name = action_name
        self.target_name = target_name
        
        # [function, can_block, can_challenge, claimed_card]
        self.action_map = {
            'income': [self.income, False, False, None],
            'foreign aid': [self.foreign_aid, True, False, None],
            'coup':[self.coup, False, False, None],
            'tax':[self.tax, False, True, 'Duke'],
            'assassinate':[self.assassinate, True, True, 'Assassin'],
            'steal':[self.steal, True, True, 'Captain'],
            'exchange':[self.exchange, False, True, 'Ambassador']
            }

        # KeyError expected if invalid action name
        action_info = self.action_map[action_name]
        self.func, self.can_block, self.can_chal, self.claimed_card = action_info
        self.summary = f"Player: {self.player_name}, Action: {self.action_name}, Target: {self.target_name}"
        
        
    # take 1 coin, no block, no challenge
    def income(self, game_state, player, blocked, lost_chal):
        game_state.change_coins(player, 1)
        log_str = f"{player.name} took 1 coin with income"
        print(log_str)
        game_state.log.append(log_str)
    
    
    
    # take two coins, block (Duke), no challenge
    def foreign_aid(self, game_state, player, blocked, lost_chal):
        if not blocked: 
            game_state.change_coins(player, 2)
            log_str = f"{player.name} took 2 coins with Foreign Aid"
        else:
            log_str = f"{player.name} was blocked from taking Foreign Aid"
        print(log_str)
        game_state.log.append(log_str)
    
    
    
    # return 7 coins, no block, no challenge
    def coup(self, game_state, player, blocked, lost_chal):
        opponent = game_state.get_player(self.target_name)
        
        # already validated that player had enough coins to coup
        game_state.change_coins(player,-7)
        
        # if player to coup not valid then too bad so sad no coup
        if opponent is not None:
            game_state.lose_card(opponent)
            log_str = f"{player.name} Coups {self.target_name}"
        else:
            log_str = f"{player.name} tried to Coup but did not select a valid player"
        print(log_str)
        game_state.log.append(log_str)   
    
    
    
    # take 3 coins, no block, yes challenge
    def tax(self, game_state, player, blocked, lost_chal):
        if not lost_chal:
            game_state.change_coins(player, 3)
            log_str = f"{player.name} took 3 coins with Tax"
        else:
            log_str = f"{player.name} tried to take 3 with Tax but was challenged and lost"
            
        print(log_str)
        game_state.log.append(log_str)   
    
    # exchange cards, no block, yes challenge
    def exchange(self, game_state, player, blocked, lost_chal):
        if not lost_chal:
            game_state.exchange(player)
            log_str = f"{player.name} swapped cards with Exchange"
        else:
            log_str = f"{player.name} tried to swap cards with Exchange but was challenged and lost"
        
        print(log_str)
        game_state.log.append(log_str)   
        
        
    # remove 1 player's card, yes block, yes challenge
    def assassinate(self, game_state, player, blocked, lost_chal):
        opponent = game_state.get_player(self.target_name)
        game_state.change_coins(player, -3)
        
        if not blocked and not lost_chal:
            if opponent is not None: 
                game_state.lose_card(opponent)
                log_str = "{player.name} Assassinates {self.target_name}."
            else:
                log_str = "{player.name} tried to Assassinate but failed to select a valid target."
        elif blocked:
            log_str = f"{player.name} tried to Assassinate {self.target_name} but was blocked."
        elif lost_chal: 
            log_str = f"{player.name} tried to Assassinate {self.target_name} but was challenged and lost."
        print(log_str)
        game_state.log.append(log_str)   
    
    # take 2 coins from opp, yes block, yes challenge
    def steal(self, game_state, player, blocked, lost_chal):
        log_str = 'DEFAULT VALUE SHOULD BE REPLACED'
        opponent = game_state.get_player(self.target_name)
        if not blocked and not lost_chal:
            if opponent is not None:
                coins_stolen = game_state.change_coins(player, -2)
                game_state.change_coins(player, coins_stolen)
            else:
                log_str = f"{player.name} tried to Steal but failed to select a valid target."
        elif blocked:
            log_str = f"{player.name} tried to Steal from {self.target_name} but was blocked."
        elif lost_chal: 
            log_str = f"{player.name} tried to Steal from {self.target_name} but was challenged and lost."
            
        print(log_str)
        game_state.log.append(log_str)   

    
    

    

    
        
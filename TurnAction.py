class TurnAction:
    
    def __init__(self, player_name, action_name, target_player=None):
        # set properties
        self.player_name = player_name
        self.action_name = action_name
        self.target_player = target_player
        
        # [function, can_block, can_challenge]
        self.action_map = {
            'income': [self.income, False, False],
            'foreign_aid': [self.foreign_aid, True, False],
            'coup':[self.coup, False, False],
            'tax':[self.tax, False, True],
            'assassinate':[self.assassinate, True, True],
            'steal':[self.steal, True, True],
            'exchange':[self.exchange, False, True]
            }

        # KeyError expected if invalid action name
        action_info = self.action_map[action_name]
        self.func, self.can_chal, self.can_block = action_info
        self.summary = f"Player: {self.player_name}, Action: {self.action_name}, Target: {self.target_player}"
        
    # take 1 coin, no block, no challenge
    def income(self, game_state, player):
        game_state.change_coins(player, 1)
    
    
    # take two coins, block (Duke), no challenge
    def foreign_aid(self, game_state, player, blocked=False):
        if not blocked: 
            game_state.change_coins(player, 2)
    
    
    # return 7 coins, no block, no challenge
    def coup(self, game_state, player, opponent):
        # already validated that player had enough coins to coup
        game_state.change_coins(player,-7)
        game_state.lose_card(opponent)
        
    
    # take 3 coins, no block, yes challenge
    def tax(self, game_state, player):
        game_state.change_coins(player, 3)
    
    
    # exchange cards, no block, yes challenge
    def exchange(self, game_state, player):
        game_state.exchange(player)
        
    
    # remove 1 player's card, yes block, yes challenge
    def assassinate(self, game_state, player, opponent, blocked=False):
        game_state.change_coins(player, -3)
        if not blocked:
            game_state.lose_card(opponent)
            
    
    # take 2 coins from opp, yes block, yes challenge
    def steal(self, game_state, player, opponent, blocked=False):
        if not blocked:
            coins_stolen = game_state.change_coins(player, -2)
            game_state.change_coins(player, coins_stolen)
        

    
    

    

    
        
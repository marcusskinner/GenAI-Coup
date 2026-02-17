from GameState import GameState
from TurnAction import TurnAction

class Game:
    
    def __init__(self, players):
        self.game = GameState(players)        
        
    

    def take_turn(self):
        # get player info from game state
        curr_player = self.game.next_player()
        
        # have current player take their turn
        action = curr_player.take_turn(self.game.player_info[curr_player], self.game.public_info)
        
        # check validity of action
        if self.valid_action(action):
            # give other players a chance to respond
            for p in self.game.play_q:
                if p is not curr_player: 
                    resp = p.game_update(self.game.player_info[p], self.game.public_info, action)
                
        
        else:
            # penalize invalid actions
            # action validity handled in player class
            #TODO figure out alternate options for this
            self.game.lose_card(curr_player)
            # somehow inform player they have been penalized
        





    def valid_action(self, action):
        # ensure it is a TurnAction
        if not isinstance(action, TurnAction):
            False
        
        # get the information on the current player
        curr_player_info = self.game.player_info[self.current_player]
        coins = curr_player_info['coins']
        action_name = action.action_name
        
        # if over 10 coins, must coup
        if coins >= 10 and action_name != 'coup':
            return False
        else:
            # must have at least 7 coins for coup
            if coins < 7 and action_name =='coup': 
                return False
            # must have at least 3 coins to assassinate
            elif coins < 3 and action_name == 'assassinate':
                return False
            else:
                # all other options should be valid
                return True
        
    
    def validate_resp(self,action, resp):
        pass
    
    
    
    
    
    
    
    
    
    
    

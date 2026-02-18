from GameState import GameState
from TurnAction import TurnAction

class Game:
    
    def __init__(self, players):
        self.gs = GameState(players)        
    
    
    def run(self):
        while not self.gs.game_over:
            self.take_turn()
        print(self.gs.winner.name, 'Wins!!!!!!!')


    def take_turn(self):
        # get player info from game state
        curr_player = self.gs.next_player()
        
        # have current player take their turn
        action = curr_player.take_turn(self.gs.player_info[curr_player], self.gs.public_info)
        print()
        print(f"It is {curr_player.name}'s Turn. Action: {action.action_name}, Target: {action.target_name}")
        # check validity of turn action
        if self.valid_action(action, curr_player):
            self.action_response(action, curr_player)
        else:
            # penalize invalid actions
            # action validity handled in player class
            #TODO figure out alternate options for this
            print(f"Illegal Action Penalty. {curr_player.name} loses a card.")
            self.gs.lose_card(curr_player)
            # somehow inform player they have been penalized
        

    def valid_action(self, action, player):
        # ensure it is a TurnAction
        if not isinstance(action, TurnAction):
            return False
        
        # get the information on the current player
        curr_player_info = self.gs.player_info[player]
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
        
    
    
    def action_response(self, action, player):
        # Assume not blocked or lost challenge unless blocked / challenged
        is_blocked = False
        lost_chal = False
        
        responses = []
        if action.can_chal or action.can_block: 
            
            # give other players a chance to respond to 
            for p in self.gs.play_q:
                # player cannot respond to themselves
                if p is not player: 
                    resp = p.respond(self.gs.player_info[p], self.gs.public_info, action)
                    # set action for each response
                    resp.action = action
                    responses.append(resp)
            
            # if can challenge, see if anyone challenges
            if action.can_chal: 
                for r in responses: 
                    # only relevant if there is a legit challenge / block
                    if r.action_name == 'challenge':
                        print(f"{r.player_name} challenges {action.player_name}'s {action.action_name}")
                        lost_chal = self.challenge(action, r) 
                        # can only be challenged once per turn
                        break
                    
            # only block if allowed and didn't fail challenge
            if action.can_block and not lost_chal:
                for r in responses:
                    if r.action_name == 'block':
                        r.validate_claimed(action)
                        # if no target, anyone can block
                        if action.target_name is None:
                            print(f"{r.player_name} tries to block {action.player_name}'s {action.action_name}")
                            is_blocked = self.block(action, r)
                            break
                            
                        elif r.player_name == action.target_name: 
                            print(f"{r.player_name} tries to block {action.player_name}'s {action.action_name}")
                            is_blocked = self.block(action, r)
                            break

        # call whatever action function is needed
        return action.func(self.gs, player, is_blocked, lost_chal)
    
        
            
                            

    def challenge(self, action, response):
        # use the player names to get the player objects
        chal_name = response.player_name
        challenger = self.gs.get_player(chal_name)
        return self.action_response(response, challenger)
    
                
        
    
    def block(self, action, response):
        # use the player names to get the player objects
        blocker_name = response.player_name
        blocker = self.gs.get_player(blocker_name)
        # print(f"{blocker_name} is trying to block {action.player_name} with {response.claimed_card}")
        # recursively call action response but this time on the response
        # because blocking is a challengable action
        return self.action_response(response, blocker)
  
        #TODO: There may still be a bug that if block and then block challenged and lose
        # the block may still block when it shouldn't
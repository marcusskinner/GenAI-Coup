import random

DECK = ['Duke','Duke','Duke',
        'Captain','Captain','Captain',
        'Ambassador','Ambassador','Ambassador',
        'Contessa','Contessa','Contessa',
        'Assassin','Assassin','Assassin']

class Game:
    
    def __init__(self, players):
        # shuffle the deck
        random.shuffle(DECK)
        
        # dictionary of player info
        self.player_info = {}
        self.num_players = len(players)
        
        # iterate through players dealing cards
        for p in players:
            card1 = DECK.pop()
            card2 = DECK.pop()
            p.set_cards(card1, card2)
            # add player info to the dictionary
            self.player_info.put(p.name,{'cards':[p.card1, p.card2], 
                                         'coins':2,
                                         'alive':True})
            
        # queue of active player for tracking turns
        self.play_q = self.player_info.keys()
        
        
    def take_turn(self):
        # get player from the queue
        player = self.play_q.pop()
        
        # check that the player is alive at the start of their turn
        if self.player_info[player.name]['alive']:
            
            # TODO: figure out how to retry a few times if action invalid
            # player takes their action
            action = player.take_turn()
            if self.validate_action(action):
                pass
                # Call function for action
                
                
            else:
                pass
                #Handle what to do if the action is not valid
          
            self.play_q.insert(0, player)
        

    def validate_action(self, action):
        pass
    
    
    
    
    
    
    
    
    
    
    
    

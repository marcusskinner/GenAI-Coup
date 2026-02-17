import random
import numpy as np

DECK = ['Duke','Duke','Duke',
        'Captain','Captain','Captain',
        'Ambassador','Ambassador','Ambassador',
        'Contessa','Contessa','Contessa',
        'Assassin','Assassin','Assassin']


# handle the deck, players, cards, and coins
class GameState:
    def __init__(self, players):
        # set properties
        self.players = players # list of player objects
        self.num_players = len(players)
        self.game_over = False
        self.winner = None
        
        # create and shuffle deck
        self.deck = DECK.copy()
        self.shuffle_deck()
        
        # dictionaries of player info
        self.player_info = {}
        self.public_info = {}
        
        # iterate through players dealing cards
        for p in self.players:
            card1 = self.deck.pop()
            card2 = self.deck.pop()
            
            # add player info to the dictionary
            self.player_info.update({p:{'facedown':[card1, card2],
                                    'faceup':[],
                                    'coins':2,
                                    'alive':True
                                    }})
            
            # add player info to public dictionary
            self.public_info.update({p.name:{'facedown':['?','?'],
                                          'faceup':[],
                                          'coins':2,
                                          'alive':True}})
            
        # queue of active player for tracking turns
        self.play_q = list(self.player_info.keys())
        
    
    
    def shuffle_deck(self):
        random.shuffle(self.deck)
    
    
    # iterate through queue without removing players
    def next_player(self):
        # get player from the queue
        player = self.play_q.pop()
        self.play_q.insert(0, player)
        return player
    
    
    # to remove player from turn queue
    def remove_player(self, player):
        # remove player from queue
        self.play_q.remove(player)
        
        # update information in dictionaries
        self.player_info[player]['alive'] = False
        self.public_info[player.name]['alive'] = False
        
        if len(self.play_q) == 1:
            self.game_over = True
            self.winner = self.play_q[0]
        

    def lose_card(self, player):
        # get cards currently in play
        player_cards = self.player_info[player]['facedown']
        
        # default to losing card at index 0 
        card_idx = 0
        
        # if two cards are left, player chooses which card to lose
        if len(player_cards) > 1:
            # should be a 0 or 1 for index of card, if not default to 0
            card_idx = player.lose_card(self.game.player_info[player], self.game.public_info)
            if card_idx not in [0,1]:
                card_idx = 0
        
        # get the card and remove it from the list
        card = player_cards[card_idx]
        player_cards.remove(card)
        
        # update private information
        self.player_info[player]['facedown'] = player_cards
        self.player_info[player]['faceup'].append(card)
        
        # update public info
        self.public_info[player.name]['facedown'].pop()
        self.public_info[player.name]['faceup'].append(card)
        
        # if no cards left, player is out of the game
        if len(player_cards) == 0:
            self.remove_player(player)
        
      
    def replace_card(self, player, card):
        # remove card from hand
        cards = self.player_info[player]['facedown']
        cards.remove(card)
        
        # shuffle card into deck
        self.deck.append(card)
        self.shuffle_deck()
        
        # get a new card from the deck
        new_card = self.deck.pop()
        cards = cards.append(new_card)
        
        # update player info
        self.player_info[player]['facedown'] = cards
        
        
    def exchange(self, player):
        # get the cards in player's hand
        cards = self.player_info[player]['facedown']
        
        # get two new cards from the deck
        c1 = self.deck.pop()
        c2 = self.deck.pop()
        drawn = [c1, c2]
        
        keep, discard = player.exchange(self.game.player_info[player], 
                                        self.game.public_info, 
                                        drawn)

        # check that player responded with lists
        if isinstance(keep,list) and isinstance(discard,list):
            # ensure the player selected valid cards to keep and discard
            # the cards provided should be the same as the cards returned
            initial_cards = sorted(cards + drawn)
            final_cards = sorted(keep + discard)
            
            # the player should keep the same number of cards as in their hand
            if len(cards) == len(keep) and initial_cards == final_cards:
                # player gets to keep the cards they selected
                self.player_info[player]['facedown'] = keep
                self.deck = self.deck+discard
                self.shuffle_deck()
            else: 
                error = True
        else:
            error = True
            
        # if exchange failed, return to original state
        if error:
            # fail to exchange, return cards to deck, shuffle
            self.player_info[player]['facedown'] = cards
            self.deck = self.deck+cards
            self.shuffle_deck()           
            
            
    
    def change_coins(self, player, n_coins):
        
        # get player_info from game state
        player_info = self.player_info[player]
        public_info = self.public_info[player.name]
        
        # can only lose as many coins as they have
        if n_coins < 0 and -1*n_coins > player_info['coins']:
            n_coins = -1* player_info['coins']
            
        # update player info
        player_info['coins'] = player_info['coins'] + n_coins
        public_info['coins'] = public_info['coins'] + n_coins
        
        # set player info
        self.player_info[player] = player_info
        self.public_info[player.name] = public_info
        
        # return the number of coins gained/lost
        return np.abs(n_coins)
    


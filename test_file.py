# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 08:19:23 2026

@author: audrey
"""

from OllamaPlayer import OllamaPlayer
from Game import Game

# p1 = OllamaPlayer('chill dude', 'You are a casual player')
# p2 = OllamaPlayer('hardcore gamer', 'You are an aggressive player, deadset on winning')
# p3 = OllamaPlayer('silly', 'You like to switch things up and occasionally make the game interesting')
# p4 = OllamaPlayer('cautious', 'You are a careful player and avoid taking unnecessary risks')
p1 = OllamaPlayer('A')
p2 = OllamaPlayer('B')
p3 = OllamaPlayer('C')
p4 = OllamaPlayer('D')


game = Game([p1,p2,p3, p4])
game.run()
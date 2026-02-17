# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 08:19:23 2026

@author: audrey
"""

from GameState import GameState
from OllamaPlayer import OllamaPlayer


p1 = OllamaPlayer('p1')
p2 = OllamaPlayer('p2')
p3 = OllamaPlayer('p3')

gs = GameState([p1,p2,p3])

print(gs.player_info)
print(gs.public_info)

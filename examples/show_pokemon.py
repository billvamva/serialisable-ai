"""
Print out pokemon in the players party
"""
from pkmai.save import Save
import os

save = Save.from_file("/Users/vasvamva1/Documents/pkm-ai/data/emerald.sav")


game = save.to_game()

for pokemon in game.party:

    print(f"\n------------ {pokemon.nickname} ------------")
    print(pokemon)

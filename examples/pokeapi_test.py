from pokeapi.wrapper import PokemonAPIWrapper
from pokeapi.util import calculate_exp_from_level, calculate_level_from_exp


api_wrapper = PokemonAPIWrapper()

print(api_wrapper.get_pokemon_growth_rate('bulbasaur'))
print(api_wrapper.get_pokemon_attributes('Iron Boulder'))

print(calculate_exp_from_level(100, "medium"))
print(calculate_level_from_exp(125, "medium"))

print(api_wrapper.get_item_attributes(2155))

ITEM_NAME_TO_INDEX= {} 

for i in range(25):
        ITEM_NAME_TO_INDEX[i] = api_wrapper.get_item_attributes(i)['name']

print(ITEM_NAME_TO_INDEX)

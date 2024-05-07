from pkmai.pokemon_info import PokemonInfo
from pkmai.level import Level
from pkmai.pokemon import PCPokemon
from pkmai.moves import Move

print(PokemonInfo.from_name("charmander"))
print(PokemonInfo.from_id(15))
print(Level("charmander").get_level_from_exp(15))

flygon = PCPokemon.from_name(
    name="Flygon",
    level=48,
    move_1=Move.from_name("Thunder"),
    move_2=Move.from_name("Thunder Punch"),
    move_3=Move.from_name("Ice Beam"),
    move_4=Move.from_name("Fly"),
)

print(flygon.pokemon_info)
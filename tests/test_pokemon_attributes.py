from pokeapi.wrapper import PokemonAPIWrapper
import pytest

POKEMON_INFO = [
    {
        "name" : "bulbasaur",
        "id": 1,
        "types": ['grass', 'poison'],
        "hp": 45,
        "attack": 49,
        "defense": 49,
        "speed": 45,
        "sp_attack": 65,
        "sp_defense": 65,
    },
    {
        "name" : "ivysaur",
        "id": 2,
        "types": ['grass', 'poison'],
        "hp": 60,
        "attack": 62,
        "defense": 63,
        "speed": 60,
        "sp_attack": 80,
        "sp_defense": 80,
    },
    {
        "name" : "venusaur",
        "id": 3,
        "types": ['grass', 'poison'],
        "hp": 80,
        "attack": 82,
        "defense": 83,
        "sp_attack": 100,
        "sp_defense": 100,
        "speed": 80
    }
]

@pytest.mark.parametrize(
    "pokemon",
    POKEMON_INFO
)

def test_pokemon_attributes(pokemon):
        apiWrapper = PokemonAPIWrapper()
        attributes = apiWrapper.get_pokemon_attributes(pokemon['name'])
        assert attributes == pokemon
        attributes = apiWrapper.get_pokemon_attributes(pokemon['id'])
        assert attributes == pokemon





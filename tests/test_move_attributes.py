from pokeapi.wrapper import PokemonAPIWrapper
import pytest

MOVE_INFO = [
    {
        "name": "pound",
        "id" : 1,
        "type": "normal",
        "category": "physical",
        "power": 40,
        "accuracy": 100,
        "pp": 35,
        "priority": 0,
        'description': 'Inflicts regular damage with no additional effect.'
    },
    {
        "name": "karate-chop",
        "id" : 2,
        "type": "fighting",
        "category": "physical",
        "power": 50,
        "accuracy": 100,
        "pp": 25,
        "priority": 0,
        'description': 'Has an increased chance for a critical hit.'
    },
    {
        "name": "double-slap",
        "id" : 3,
        "type": "normal",
        "category": "physical",
        "power": 15,
        "accuracy": 85,
        "pp": 10,
        "priority": 0,
        'description': 'Hits 2-5 times in one turn.'
    }
]

@pytest.mark.parametrize(
    "move",
    MOVE_INFO
)

def test_move_attributes(move):
        apiWrapper = PokemonAPIWrapper()
        attributes = apiWrapper.get_move_attributes(move['name'])
        assert attributes == move
        attributes = apiWrapper.get_move_attributes(move['id'])
        assert attributes == move
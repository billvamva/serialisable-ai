from pokeapi.wrapper import PokemonAPIWrapper
import pytest

@pytest.mark.parametrize(
    "item",
    [
        {
                "id" : 0,
                "name" : "Nothing"
        },
        {
                "id" : 1,
                "name" : "master-ball"
        },
    ],
)

def test_item_attributes(item):
    api_wrapper = PokemonAPIWrapper()
    item_attributes = api_wrapper.get_item_attributes(item['index'])
    assert item_attributes == item
    item_attributes = api_wrapper.get_item_attributes(item['name'])
    assert item_attributes == item
    
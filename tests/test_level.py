from pokeapi.wrapper import PokemonAPIWrapper
from pokeapi.util import calculate_level_from_exp, calculate_exp_from_level
import pytest

@pytest.mark.parametrize(
    "pokemon",
    [
        "Nincada",  # Erratic
        "Jigglypuff",  # Fast
        "Zubat",  # Medium Fast
        "Oddish",  # Medium Slow
        "Growlithe",  # Slow
        "Wailmer",  # Fluctuating
    ],
)

def test_level_reverse_calc(pokemon):
    api_wrapper = PokemonAPIWrapper()
    growth_rate_name = api_wrapper.get_pokemon_growth_rate(pokemon)
    
    for level in range(1, 101):
        exp = calculate_exp_from_level(level, growth_rate_name)
        assert calculate_level_from_exp(exp, growth_rate_name) == level
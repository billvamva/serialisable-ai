from math import floor, sqrt, ceil
import pytest

def calculate_exp_from_level(level, growth_rate_name):
    # Define the experience values for each level for different growth rates
    if growth_rate_name == 'slow-then-very-fast':
        return level_slow_then_very_fast(level)
    elif growth_rate_name == 'fast':
        return level_fast(level)
    elif growth_rate_name == 'medium':
        return level_medium(level)
    elif growth_rate_name == 'medium-slow':
        return level_medium_slow(level)
    elif growth_rate_name == 'slow':
        return level_slow(level)
    elif growth_rate_name == 'fast-then-very-slow':
        return level_fast_then_very_slow(level)
    else:
        raise ValueError("Invalid growth rate name.")


def level_slow_then_very_fast(level: int) -> int:
    if level == 1:
        return 0
    elif level < 50:
        res = level**3 * (100 - level) / 50
    elif level >= 50 and level < 68:
        res = level**3 * (150 - level) / 100
    elif level >= 68 and level < 98:
        res = level**3 * int((1911 - 10 * level) / 3) / 500
    elif level >= 98 and level < 100:
        res = level**3 * (160 - level) / 100
    else:
        res = 600_000
    return int(res)


def level_fast(level: int) -> int:
    if level == 1:
        return 0
    return int(4 * level**3 / 5)


def level_medium(level: int) -> int:
    if level == 1:
        return 0
    return int(level**3)


def level_medium_slow(level: int) -> int:
    if level == 1:
        return 0
    return int(6 / 5 * level**3 - 15 * level**2 + 100 * level - 140)


def level_slow(level: int) -> int:
    if level == 1:
        return 0
    return int(5 / 4 * level**3)


def level_fast_then_very_slow(level: int) -> int:
    if level == 1:
        return 0
    elif level < 15:
        res = level**3 * (int((level + 1) / 3) + 24) / 50
    elif level >= 15 and level < 36:
        res = level**3 * (level + 14) / 50
    elif level >= 36 and level < 100:
        res = level**3 * (int(level / 2) + 32) / 50
    else:
        res = 1_640_000
    return int(res)


LEVEL_FROM_EXP = {}

growth_rates = ['slow', 'medium', 'medium-slow', 'fast', 'fast-then-very-slow', 'slow-then-very-fast']

for level in range(1, 101):
    for growth_rate_name in growth_rates:
        total_exp = calculate_exp_from_level(level, growth_rate_name)
        LEVEL_FROM_EXP[(total_exp, growth_rate_name)] = level

def calculate_level_from_exp(total_exp: int, growth_rate_name: str) -> int:
    # Check if the exact key exists
    if (total_exp, growth_rate_name) in LEVEL_FROM_EXP:
        return LEVEL_FROM_EXP[(total_exp, growth_rate_name)]
    
    
    # Find the closest lower available key
    lower_keys = [(exp, rate) for (exp, rate) in LEVEL_FROM_EXP.keys() if exp < total_exp]
    if lower_keys:
        closest_key = max(lower_keys)
        return LEVEL_FROM_EXP[closest_key]
    
    # If no lower key is available, return 0
    return 0
from pokeapi.client import APIClient
from pokeapi.util import calculate_level_from_exp

import json
from typing import Optional, Dict, Any, Union


class PokemonAPIWrapper:
    api_client = APIClient('https://pokeapi.co/api/v2')
    smogon_api_client = APIClient('https://smogonapi.herokuapp.com')

    @classmethod
    def get_pokemon_data(cls,pokemon: Union[int, str]) -> Optional[Dict[str, Any]]:
        if type(pokemon) == str:
            return cls.api_client.get('/pokemon/{}'.format(pokemon.replace(" ", "-").lower()))
        elif type(pokemon) == int:
            return cls.api_client.get('/pokemon/{}'.format(pokemon))

    @classmethod
    def get_move_data(cls,move: Union[int, str] ) -> Optional[Dict[str, Any]]:
        if type(move) == str:
            return cls.api_client.get('/move/{}'.format(move.replace(" ", "-").lower()))
        elif type(move) == int:
            return cls.api_client.get('/move/{}'.format(move))

    @classmethod
    def get_item_data(cls, item: Union[int,str]):
        if type(item) == int:
            if item == 0:
                return {
                    'id':0,
                    'name' : 'Nothing'
                }
            return cls.api_client.get('/item/{}'.format(item))
        elif type(item) == str:
            if item == 'Nothing':
                return {
                    'id':0,
                    'name' : 'Nothing'
                }
            return cls.api_client.get('/item/{}'.format(item.replace(" ", "-").lower()))
    
    @classmethod
    def get_smogon_data(cls, pokemon: str, generation:Optional[str]='rs') -> Optional[Dict[str, Any]]:

        if generation not in ['rb', 'gs', 'rs', 'dp', 'bw', 'xy', 'sm', 'ss', 'sv']:
          print("Error: Failed to fetch data for generation '{}'".format(pokemon))
          return None

        return cls.smogon_api_client.get(f'/{generation}/{pokemon.replace(" ", "-").lower()}')

    @classmethod
    def get_pokemon_growth_rate(cls, pokemon: Union[str, int]) -> Optional[str]:
        
        # Get information about the Pokemon
        pokemon_data = cls.get_pokemon_data(pokemon)
        if not pokemon_data:
          print("Error: Failed to fetch data for Pokemon '{}'".format(pokemon))
          return None
    
        
        # Extract the growth rate URL from the Pokemon data
        species_url = pokemon_data['species']['url']
        
        # Fetch species data to get the growth rate URL
        species_data = cls.api_client.get(species_url)
        if not species_data:
            print("Error: Failed to fetch species data for Pokemon '{}'".format(pokemon))
            return None
        
        # Extract the growth rate URL from the species data
        growth_rate_data = species_data['growth_rate']
        
        if not growth_rate_data:
            print("Error: Failed to fetch growth rate data for Pokemon '{}'".format(pokemon))
            return None
        
        return growth_rate_data['name']
    
    @classmethod
    def get_pokemon_level(cls, pokemon: Union[str,int], total_exp: int) -> int: 

        growth_rate_name: str = cls.get_pokemon_growth_rate(pokemon)

        pokemon_level: int = calculate_level_from_exp(total_exp, growth_rate_name)

    @classmethod
    def get_pokemon_attributes(cls, pokemon: Union[str, int]) -> Optional[Dict[str, Any]]:
        pokemon_data = cls.get_pokemon_data(pokemon) 

        if not pokemon_data:
            print("Error: Failed to fetch data for Pokemon '{}'".format(pokemon))
            return None
        
        pokemon_attributes = {
            'name' : pokemon_data['name'],
            'id': pokemon_data['id'],
            'types': [pokemon_data['types'][0]['type']['name']]
        }
        
        if len(pokemon_data['types']) > 1:
            pokemon_attributes['types'].append(pokemon_data['types'][1]['type']['name'])
        
        pokemon_attributes.update({
            'hp': pokemon_data['stats'][0]['base_stat'],
            'attack': pokemon_data['stats'][1]['base_stat'],
            'defense': pokemon_data['stats'][2]['base_stat'],
            'sp_attack': pokemon_data['stats'][3]['base_stat'],
            'sp_defense': pokemon_data['stats'][4]['base_stat'],
            'speed': pokemon_data['stats'][5]['base_stat']
        })
        
        return pokemon_attributes


    @classmethod
    def get_move_attributes(cls, move: Union[str, int]) -> Optional[Dict[str, Any]]:
        move_data = cls.get_move_data(move)  # Assuming you have a method to fetch move data
        
        if not move_data:
            print("Error: Failed to fetch data for move '{}'".format(move_data))
            return {'name': 'none', 'id': 0, 'type': '-', 'category': '-', 'power': 0, 'accuracy': 0, 'pp': 0, 'priority': 0, 'description': "-"}
        
        move_attributes = {
            'name' : move_data['name'],
            'id': move_data['id'],
            'type': move_data['type']['name'],
            'category': move_data['damage_class']['name'],
            'power': move_data.get('power', 0),
            'accuracy': move_data.get('accuracy', 100),
            'pp': move_data['pp'],
            'priority': move_data.get('priority', 0),
            'description': move_data['effect_entries'][0]['short_effect']
        }
        
        return move_attributes

 
    @classmethod
    def get_item_attributes(self, item: Union[int, str]) -> Optional[Dict[str, Any]]:
        item_data = self.get_item_data(item)
        
        if not item_data:
            print(f"Error: Item {item} is not valid.")
            return None
        
        item_id = item_data.get('id')
        item_name = item_data.get('name')
        
        if not item_name:
            print(f"Error: Item name not found for item number {item_number}.")
            return None
        
        return {
            'id': item_id,
            'name': item_name
        }

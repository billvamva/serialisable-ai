from typing import Type, List, Union, ClassVar, Optional, Dict

from pokeembedding.connection import Node, Connection, NNet
from pokeembedding.codec import Codec, Serializable

class NodeCodec(Codec):
        def __init__(self, section_class: Serializable):
                self.field_dict = {
                        "id": {"data_type": int, "offset": 0, "size": 4},
                        "bias": {"data_type": float, "offset": 4, "size": 4},
                        "z": {"data_type": float, "offset": 8, "size": 4},
                }
                self.object_class = section_class

                super.__init__(self.field_dict)
        
        def to_object(self):
                pass
        

class ConnectionCodec(Codec):
        def __init__(self, section_class: Serializable):
                self.field_dict = {
                "id": {"data_type": int, "offset": 0, "size": 4},
                "input_node_id": {"data_type": int, "offset": 4, "size": 4},
                "output_node_id": {"data_type": int, "offset": 8, "size": 4},
                "weight": {"data_type": float, "offset": 8, "size": 4}
                } 
                self.object_class = section_class
                super.__init__(self.field_dict)

class NNetCodec(Codec):
        def __init__(self, section_class: Serializable):
                field_dict = {
                "int_field": {"data_type": int, "offset": 0, "size": 4},
                "str_field": {"data_type": str, "offset": 4, "size": 8}
                } 
                self.object_class = section_class
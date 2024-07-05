from typing import Type, List, Union, ClassVar, Optional, Dict
from random import random

from pokeembedding.class_codecs import ConnectionCodec

class Connection(Serializable):
        _codec: ClassVar[Codec] = ConnectionCodec
        total_connections: ClassVar[int] = 0

        def __init__(self, input_node: "Node", output_node: "Node"):
                self.id = Connection.total_connections 
                Connection.total_connections += 1
                self.input_node = input_node
                self.output_node = output_node
                self.weight = random() 
                input_node.output_connections.append(self)
                output_node.input_connections.append(self)
                self.delta_sum = 0.0
        
        def set_delta(self, delta):
                self.delta_sum += delta * self.input_node.get_value()
        
        def learn(self, batch_step:float)-> None:
                """
                """
                self.weight -= batch_step * self.delta_sum
                self.delta_sum = 0

        
from typing import Type, List, Union, ClassVar, Optional, Dict
from random import random

class Connection:

        def __init__(self, input_node: "Node", output_node: "Node"):
                self.input_node = input_node
                self.output_node = output_node
                self.weight = random() 
                input_node.output_connections.append(self)
                output_node.input_connections.append(self)
                self.delta_sum = 0.0
        
        def set_delta(self, delta):
                self.delta_sum += delta * self.input_node.get_value()
        
        def learn(self, batch_step:float)-> None:
                self.weight -= batch_step * self.delta_sum
                self.delta_sum = 0

        
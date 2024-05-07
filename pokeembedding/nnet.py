from typing import Type, List, Union, ClassVar, Optional, Dict, Any
import numpy as np

from pokeembedding.node import Node

class NNet:

        def __init__(self, input_size: int, step: int = 3, batch_size: int = 10, epoch = 3):
                self.count = 0
                self.training_count = 0
                self.epoch = epoch
                self.step = step
                self.batch_size = batch_size
                self.all_nodes: List[Node] = []
                self.all_layers: List[List[Node]] = []
                self.output_layer: List[Node] = [] 
                self.hidden_output_nodes: List[Node] = []
                self.input_layer: List[Node] = self.add_layer(input_size)

        def add_layer(self, input_size: int) -> List[Node]:
                layer = [Node() for _ in range(input_size)] 
                for curr_node in layer:
                        self.all_nodes.append(curr_node)
                        if self.output_layer != []:
                                curr_node.connect_layers(self.output_layer)
                self.hidden_output_nodes.extend(filter(lambda n: not n.is_input(), layer))
                self.all_layers.append(layer)
                self.output_layer = layer
                return layer
        
        def reset(self) -> None:
                [curr_node.reset() for curr_node in self.all_nodes]

        def feed(self, input_array: List[int]) -> None:
                self.count += 1
                self.reset()
                for idx, input_node in enumerate(self.input_layer):
                        input_node.value = float(input_array[idx])
                for (idx, curr_node) in enumerate(self.hidden_output_nodes):
                        curr_node.feed_forward()


        def get_output(self) -> List[Node]:
                return [curr_node.get_value() for curr_node in self.output_layer]
        
        def translate_input(self, value: Any) -> List[Any]:
                return value
        
        def translate_output(self, value: Any) -> List[Any]:
                return value
        
        def check_output(self, input_element: Any) -> List[Node]:
                self.feed(self.translate_input(input_element))
                return self.translate_output(self.get_output())
        
        def get_cost(self):
                total_cost = 0
                epsilon = 1e-15  # Small value to avoid taking the log of zero
                for output_node in self.output_layer:
                        expected = output_node.expected
                        output = output_node.value
                        output = np.clip(output, epsilon, 1.0 - epsilon)  # Clip output to avoid log(0)
                        total_cost += -(expected * np.log(output) + (1.0 - expected) * np.log(1.0 - output))
                return total_cost / len(self.output_layer)
        
        def translate_expected(self, expected: Any) -> List[Any]:
                return expected
        
        def train(self, input_element, expected_output) -> None:
                self.training_count += 1
                expected_vector = self.translate_expected(expected_output)   
                output_vector = self.check_output(input_element)
                for idx, curr_output in enumerate(output_vector):
                        self.output_layer[idx].expected = expected_vector[idx]
                
                cost = self.get_cost()

                for idx in range(len(self.hidden_output_nodes)):
                        self.hidden_output_nodes[idx].get_delta()
                
                if (self.training_count % self.batch_size == 0) :
                        for curr_node in self.hidden_output_nodes:
                                curr_node.learn(self.step/self.batch_size)
                
        def summary(self) -> None:
                # Prints a textual summary of the neural network including connections
                print(f'{"Layer (type)":<20}{"Output Shape":<20}Param #')
                print('=' * 60)
                for i, layer in enumerate(self.all_layers, 1):
                        output_shape = f'[-1, {len(layer)}]'
                        if i == 1:  # Input layer
                                layer_type = 'Input'
                                param_count = 0
                        else:
                                layer_type = 'Hidden' if i < len(self.all_layers) else 'Output'
                                param_count = len(self.all_layers[i - 2]) * len(layer)
                        print(f'{layer_type:<20}{output_shape:<20}{param_count:>8}')

         



             
             
        



        
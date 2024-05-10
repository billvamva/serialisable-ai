from typing import Type, List, Union, ClassVar, Optional, Dict
import numpy as np 
from random import random

from pokeembedding.connection import Connection
from pokeembedding.codec import Codec, Serializable
from pokeembedding.class_codecs import NodeCodec

class Node(Serializable):
        total_nodes:ClassVar[int] = 0
        _codec: ClassVar[Codec] = NodeCodec

        def __init__(self, bias: Optional[float] = random()):
                self.id = Node.total_nodes
                Node.total_nodes = self.id + 1
                self.input_connections: List[Connection] = []
                self.output_connections: List[Connection] = []
                self.activate = Node.sig
                self.activation_derivative = Node.sig_deriv
                self.bias = bias
                self.z: float = None
                self.value: float = None
                self.expected:float = None
                self.delta: float = None
                self.delta_sum: float = 0.0

        @staticmethod
        def sig(x: float) -> float:
                return 1/(1 + np.exp(-x))

        @staticmethod
        def sig_deriv(x: float) -> float:
                return Node.sig(x) * (1 - Node.sig(x))

        @staticmethod
        def apply_threshold(sigmoid_output:float, threshold=0.5) -> float:
                # Thresholding step
                binary_output = np.where(sigmoid_output >= threshold, 1.0, 0.0)
                return binary_output
        
        def connect_layers(self, prev_nodes: List["Node"], weights: Optional[List[float]] = None):
                """
                """
                if weights and len(prev_nodes) != len(weights):
                        raise Exception("Include all or no weights, will be randomly initialised.")
                
                for idx, prev_node in enumerate(prev_nodes):
                       curr_conn = Connection(prev_node, self) 
                       if weights is not None:
                        curr_conn.weight = weights[idx]

        def reset(self) -> None:
                self.value = None
                self.delta = None
        
        def feed_forward(self) -> None:
                """
                """
                z  = self.bias

                for conn in self.input_connections:
                        z += conn.weight * conn.input_node.get_value()

                self.z = z
                self.value = Node.apply_threshold(self.activate(self.z))

        
        def get_value(self) -> float:
                if self.value is None: 
                        self.feed_forward()
                return self.value
        
        def is_input(self) -> bool:
                return self.input_connections == []

        def is_output(self) -> bool:
                return self.output_connections == []
        
        def get_delta(self):
                """
                """
                if self.delta is None:
                        if self.is_output():
                                # output neurons
                                self.delta = (self.value - self.expected) * self.sig_deriv(self.z)
                        else:
                                # hidden neurons
                                self.delta = sum(conn.output_node.get_delta() * conn.weight for conn in self.output_connections) 
                        for conn in self.input_connections:
                                conn.set_delta(self.delta)
                        self.delta_sum += self.delta
                return self.delta
        
        def learn(self, batch_step:float)-> None:
                """
                """
                if self.delta:
                        # adjust bias
                        self.bias -= batch_step * self.delta_sum
                        # adjust input weights
                        for conn in self.input_connections:
                                conn.learn(batch_step) 
                        
                        self.delta_sum = 0
                        self.delta = None

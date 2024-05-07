import pytest
from pokeembedding.node import Node

class TestNeuron:
        @pytest.fixture
        def setup(self):
                hidden_node = Node()
                hidden_node.bias = 0.2
                weights = [0.5, 0.6, 0.7]
                values = [1, 0, 1]
                input_nodes = [Node() for _ in range(3)]
                for input_node, value in zip(input_nodes, values):
                        input_node.value = value
                print(f'{[node.value for node in input_nodes]}')
                hidden_node.connect_layers(input_nodes, weights)
                return hidden_node

        def test_instantiate_node(self, setup):
                assert isinstance(setup, Node)
        
        def test_reset_method(self, setup):
                setup.value = 5
                setup.delta = 3
                setup.reset()
                assert setup.value is None
                assert setup.delta is None

        def test_is_input_false_if_node_has_input(self, setup):
                assert not setup.is_input()

        def test_is_input_true_if_node_has_no_input(self):
                node = Node()
                assert node.is_input()

        def test_is_output_true_if_Node_has_no_output(self):
                node = Node()
                assert node.is_output()

        def test_calculate_correct_value(self, setup):
                setup.feed_forward()
                expected_z = 1.4  # (0.5 * 1 + 0.7 * 1 + 0.2)
                expected_a = 0.8021838885585817  # 1 / (1 + exp(-(0.5 * 1 + 0.7 * 1 + 0.2)))
                assert setup.z == expected_z
                assert setup.value == pytest.approx(expected_a, abs=1e-9)
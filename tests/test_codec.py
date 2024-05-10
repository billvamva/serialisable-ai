import pytest

# Import the classes to be tested
from pokeembedding.codec import ByteField, Codec

# Define test cases
class TestByteField:
    def test_to_value_with_int(self):
        field = ByteField("test_field", int, 0, 4)
        print(field.to_value(b'\x01\x00\x00\x00'))
        assert field.to_value(b'\x01\x00\x00\x00') == 1

    def test_to_bytes_with_int(self):
        field = ByteField("test_field", int, 0, 4)
        assert field.to_bytes(1) == b'\x01\x00\x00\x00'

    def test_to_value_with_str(self):
        field = ByteField("test_field", str, 0, 8)
        assert field.to_value(b'hello\x00\x00\x00') == 'hello'

    def test_to_bytes_with_str(self):
        field = ByteField("test_field", str, 0, 8)
        assert field.to_bytes('hello') == b'hello\x00\x00\x00'
    
    def test_to_bytes_with_float(self):
        # Define a ByteField instance for a float
        field = ByteField("test_field", float, 0, 4)  # Assuming 4 bytes for float representation

        # Test case: Convert float to bytes
        float_value = 3.14 
        bytes_data = field.to_bytes(float_value)
        assert bytes_data == b'\xc3\xf5H@'

    def test_to_value_with_float(self):
        # Define a ByteField instance for a float
        field = ByteField("test_field", float, 0, 4)  # Assuming 4 bytes for float representation

        # Test case: Convert float to bytes
        float_value = b'\xc3\xf5H@'
        bytes_data = field.to_value(float_value)
        assert "{:.2f}".format(bytes_data) == '3.14'


    # Add more test cases for other data types and scenarios


class TestCodec:
    def test_generate_fields(self):
        field_dict = {
            "int_field": {"data_type": int, "offset": 0, "size": 4},
            "str_field": {"data_type": str, "offset": 4, "size": 8}
        }
        codec = Codec(field_dict)
        assert len(codec.fields) == 2
        assert isinstance(codec.fields[0], ByteField)
        assert codec.fields[0].name == "int_field"
        assert codec.fields[1].name == "str_field"

    # Add more test cases for other methods and scenarios

# Execute tests by running pytest in the terminal

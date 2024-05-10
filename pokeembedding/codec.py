from typing import Union, List, Dict, Optional, Any
from dataclasses import dataclass
import struct


class ByteField:
        def __init__(
                self,
                name: str,
                data_type: Union[str, int, bytes],
                offset: int,
                size: int,
                deserialize_skip: bool = False,
                serialize_skip: bool = False,
        ):
                """
                deserialize_skip if this is True when creating object from bytes it will
                just set the raw bytes. 

                serialize_skip will set the given field will be filled with
                the maximum value.
                """
                self.name = name
                self.data_type = data_type
                self.offset = offset
                self.size = size
                self.deserialize_skip = deserialize_skip
                self.serialize_skip = serialize_skip
        
        def to_value(self, data: bytes) -> Union[str, int, float, bytes]:
                """
                Convert bytes to a typed python value
                """

                blob = data[self.offset : self.offset + self.size]

                if self.deserialize_skip:
                        return blob
                else:

                        if self.data_type is int:
                                value = Codec.bytes_to_int(blob)
                        elif self.data_type is float:
                                value = Codec.bytes_to_float(blob)
                        elif self.data_type is str:
                                value = Codec.bytes_to_str(blob)
                        elif self.data_type is bytes:
                                value = blob
                        elif isinstance(self.data_type, type(Serializable)):
                                # Let the object itself deserialize the bytes to a value
                                value = self.data_type.from_bytes(data)
                        elif self.data_type in (list, List):
                                
                                for _object in value:
                                        buffer += self.to_bytes(_object)
                                return bytes(buffer)
                        else:
                                raise ValueError(f"Invalid type {self.data_type=}")

                        return value

        def to_bytes(self, value: Union[str, int, float, bytes, list]) -> bytes:
                """
                Convert a value to bytes (Can be used recursively)
                """
                if self.serialize_skip:
                        value = Codec.int_to_bytes(256**self.size - 1, self.size)
                        return value

                if self.data_type is int:
                        return Codec.int_to_bytes(value, self.size)
                elif self.data_type is float:
                        _bytes =  Codec.float_to_bytes(value, self.size)
                        return _bytes
                elif self.data_type is str:
                        raw_bytes = Codec.str_to_bytes(value)
                        _bytes = raw_bytes.ljust(self.size, b"\x00")
                        return _bytes
                elif self.data_type is bytes:
                        return value
                elif self.data_type is list:
                        if isinstance(value, bytes):
                                return value
                        else:
                                buffer = bytearray()
                                for _object in value:
                                        buffer += self.to_bytes(_object)
                                return bytes(buffer)
                elif isinstance(self.data_type, type(Serializable)):
                        # Let the object serialize itself to bytes
                        return value.to_bytes()
                else:
                        raise ValueError(f"Type {self.data_type} is not supported!")

        def add_offset(self, offset):
                self.offset += offset


class Codec:
        def __init__(self, field_dict: Dict[str, Any]):
                self.fields = self.generate_fields(field_dict)

        @staticmethod
        def bytes_to_int(val: bytes) -> int:
                return int.from_bytes(val, byteorder="little")

        @staticmethod
        def int_to_bytes(val: int, length: int) -> bytes:
                return int.to_bytes(val, length, byteorder="little")
        
        @staticmethod
        def bytes_to_float(val: bytes) -> float:
                return struct.unpack("<f", val)[0]

        @staticmethod
        def float_to_bytes(val: int, length: int) -> bytes:
                return struct.pack(f"<{length}s", struct.pack("<f", val))

        @staticmethod
        def bytes_to_str(val: bytes) -> str:
                return val.split(b'\x00')[0].decode()

        @staticmethod
        def str_to_bytes(val: str) -> bytes:
                return val.encode()

        @staticmethod
        def create_byte_field(name: str, data_type: type, offset: int, size: int, **kwargs) -> ByteField:
                return ByteField(name, data_type, offset, size, **kwargs)

        def generate_fields(self, field_dict: Dict[str, Any]) -> List[ByteField]:
                """
                Generate ByteFields from dict of fields
                """
                fields = []

                for field_name, field_info in field_dict.items():
                        field = self.create_byte_field(
                                field_name,
                                field_info.get("data_type"),
                                field_info.get("offset"),
                                field_info.get("size"),
                                deserialize_skip=field_info.get("deserialize_skip", False),
                                serialize_skip=field_info.get("serialize_skip", False),
                        )
                        fields.append(field)
                return fields

        def to_values(self, data: bytes) -> Dict[str, Union[str, int]]:
                """
                Convert data to dict of typed python values using the ByteField
                fields defined in the codec
                """
                res = {}
                for field in self.fields:
                        res[field.name] = field.to_value(data)

                return res

        def to_object(self, data: bytes) -> "Object":
                """
                Create instance of an object based on the dict of python values
                """
                values = self.to_values(data)
                object_class = self.object_class
                obj = object_class(**values)

                return obj

        
        def to_bytes(self, _object: "Serializable") -> bytes:
                """
                Convert python object to byte stream based on ByteFields
                """
                buffer = bytearray()

                fields_by_offset = self.fields.sort(lambda x: x.offset)

                for field in fields_by_offset:
                        buffer.extend(b"\x00" * (field.offset - len(buffer)))
                        value = getattr(_object, field_name)
                        
                        value_to_bytes = field.to_bytes(value)
                        buffer.extend(value)
                
                return bytes(buffer)

                

@dataclass
class Serializable:

        @property
        def codec(self) -> Codec:
                # Retrieve the codec instance associated with the current class
                return self._codec(type(self))
    
        @classmethod
        def from_bytes(cls, data: bytes):
                return cls._codec(cls).to_object(data)

        def to_bytes(self) -> bytes:
                return self.codec.to_bytes(self)
        
        def save_byte_stream(self) -> None:
                with open("output/neural_net", "wb") as f:
                        f.write(self.to_bytes())




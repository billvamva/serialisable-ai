from typing import Union, List, Dict, Optional
from dataclasses import dataclass

def bytes_to_int(val: bytes) -> int:
    return int.from_bytes(val, byteorder="little")


def int_to_bytes(val: int, length: int) -> bytes:
    return int.to_bytes(val, length, byteorder="little")

class ByteField:
        def __init__(self, ):
                pass

class Codec:
        def __init__(self, fields: List[ByteField]):
                pass

        @staticmethod
        def create_byte_field(name: str, data_type: type, offset: int, size: int, **kwargs) -> ByteFieldCodec:
                return ByteField(name, data_type, offset, size, **kwargs)

        def generate_fields(self, field_dict: Dict[str, Any]) -> List[ByteFieldCodec]:
                fields = []

                for field_name, field_info in fields_dict.items():
                        field = self.create_byte_field(
                                field_name,
                                field_info.get("data_type"),
                                field_info.get("offset"),
                                field_info.get("size"),
                                value_map=field_info.get("value_map"),
                                reverse_value_map=field_info.get("reverse_value_map"),
                                deserialize_skip=field_info.get("deserialize_skip", False),
                                serialize_skip=field_info.get("serialize_skip", False),
                                bytes_to_value=field_info.get("bytes_to_value"),
                                value_to_bytes=field_info.get("value_to_bytes"),
                        )
                fields.append(field)

        def to_values(self, data: bytes) -> Dict[str, Union[str, int]]:
                """Convert data to dict of values using the ByteField
                fields defined in the codec"""
                res = {}
                for field in self.fields:
                        res[field.name] = field.to_value(data)

                return res

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

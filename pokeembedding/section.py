from typing import Type, List, Union, ClassVar, Optional, Dict, Any
import numpy as np

from pokeembedding.codec import Codec, Serializable


@dataclass
class Section:
    """
    Section is the data 4096 bytes of a section
    """

    content_data: bytes
    section_id: int
    _codec: ClassVar[Codec]

class SectionCodec(Codec):
        pass


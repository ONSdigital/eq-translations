from dataclasses import dataclass
from typing import Union, Optional


@dataclass
class TranslatableItem:
    """A translatable item within the schema

        pointer (str): JSON pointer for this item within the schema
        value (str or tuple): The resolved value of the pointer. This is a Tuple for plural forms, and a String for all other elements
        context (str): The context to use when translating the item
    """

    pointer: str
    description: str
    value: Union[str, dict]
    context: Optional[str] = None
    additional_context: str = None

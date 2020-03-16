from dataclasses import dataclass
from typing import Union, Optional


@dataclass
class TranslatableItem:
    """A translatable item within the schema

        pointer (str): The string syntax for identifying this item within the JavaScript Object Notation (JSON) document
        value (str or tuple): The resolved value of the pointer. This is a Tuple for plural forms, and a String for all other elements
        context (str): The context to use when translating the item
    """

    pointer: str
    value: Union[str, dict]
    context: Optional[str] = None

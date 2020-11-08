from neomodel import (
    StructuredNode,
    StringProperty
)


class Faculty(StructuredNode):
    name = StringProperty(unique_index=True, required=True, max_length=50)

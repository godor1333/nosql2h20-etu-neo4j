from neomodel import (
    StructuredNode,
    StringProperty
)


class Degree(StructuredNode):
    content = StringProperty(unique_index=True, max_length=50)

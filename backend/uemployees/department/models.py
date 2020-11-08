from neomodel import (
    StructuredNode,
    StringProperty
)


class Department(StructuredNode):
    name = StringProperty(unique_index=True, max_length=50)

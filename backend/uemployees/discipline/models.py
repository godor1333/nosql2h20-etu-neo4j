from neomodel import (
    StructuredNode,
    StringProperty
)


class Discipline(StructuredNode):
    name = StringProperty(unique_index=True, max_length=50)

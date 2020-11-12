from neomodel import (
    StructuredNode,
    StringProperty
)


class Discipline(StructuredNode):
    name = StringProperty(required=True, max_length=50)

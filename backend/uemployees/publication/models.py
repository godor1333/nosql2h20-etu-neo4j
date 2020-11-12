from neomodel import (
    StructuredNode,
    StringProperty
)


class Publication(StructuredNode):
    content = StringProperty(required=True, max_length=500)

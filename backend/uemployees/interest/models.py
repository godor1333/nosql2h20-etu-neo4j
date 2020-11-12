from neomodel import (
    StructuredNode,
    StringProperty
)


class Interest(StructuredNode):
    content = StringProperty(required=True, max_length=500)

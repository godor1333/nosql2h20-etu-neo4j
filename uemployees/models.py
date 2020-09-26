from neomodel import (
    StructuredNode,
    IntegerProperty
)


class Group(StructuredNode):
    number = IntegerProperty(unique_index=True, required=True)
    num_of_students = IntegerProperty(index=True, default=0)

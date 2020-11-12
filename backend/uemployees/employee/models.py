from neomodel import (
    StructuredNode,
    StringProperty,
    EmailProperty,
)


class Employee(StructuredNode):
    name = StringProperty(unique_index=True, max_length=50)
    photo_url = StringProperty(max_length=50)
    email = EmailProperty(unique_index=True, max_length=30)
    education = StringProperty(required=True, max_length=50)

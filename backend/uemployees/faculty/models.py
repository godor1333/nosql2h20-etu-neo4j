from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipTo
)


class Faculty(StructuredNode):
    name = StringProperty(unique_index=True, max_length=50)
    faculties = RelationshipTo(
        'uemployees.department.models.Department',
        'DEPARTMENT_OF_FACULTY',
        cardinality=One
    )

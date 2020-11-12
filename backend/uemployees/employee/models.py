from neomodel import (
    StructuredNode,
    StringProperty,
    IntegerProperty,
    EmailProperty,
    StructuredRel,
    RelationshipTo
)


class TeachDiscipline(StructuredRel):
    group = IntegerProperty(required=True)
    time = StringProperty(required=True, max_length=20)
    auditorium = StringProperty(required=True, max_length=6)


class Employee(StructuredNode):
    name = StringProperty(unique_index=True, max_length=50)
    photo_url = StringProperty(max_length=50)
    email = EmailProperty(unique_index=True)
    education = StringProperty(required=True, max_length=50)
    disciplines = RelationshipTo(
        'uemployees.discipline.models.Discipline',
        'TEACH_A_DISCIPLINE',
        model=TeachDiscipline
    )
    degrees = RelationshipTo(
        'uemployees.degree.models.Degree',
        'EMPLOYEE_HAS_DEGREE'
    )
    interests = RelationshipTo(
        'uemployees.interest.models.Interest',
        'EMPLOYEE_HAS_APOI'
    )
    publications = RelationshipTo(
        'uemployees.publication.models.Publication',
        'EMPLOYEE_HAS_PUBLICATION'
    )

from neomodel import (
    StructuredNode,
    StringProperty,
    IntegerProperty,
    EmailProperty,
    StructuredRel,
    RelationshipTo,
    RelationshipFrom
)

from uemployees.department.models import WorkAtDepartment


class TeachDiscipline(StructuredRel):
    group = IntegerProperty(required=True)
    time = StringProperty(required=True, max_length=50)
    auditorium = StringProperty(required=True, max_length=6)


class Employee(StructuredNode):
    name = StringProperty(unique_index=True, max_length=50)
    photo_url = StringProperty(max_length=200)
    email = EmailProperty()
    education = StringProperty(max_length=50)
    department = RelationshipFrom(
        'uemployees.department.models.Department',
        'WORK_AT_DEPARTMENT',
        model=WorkAtDepartment
    )
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

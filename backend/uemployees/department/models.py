from neomodel import (
    StructuredNode,
    StringProperty,
    StructuredRel,
    RelationshipTo
)


class WorkAtDepartment(StructuredRel):
    job_title = StringProperty(required=True, max_length=30)


class Department(StructuredNode):
    name = StringProperty(unique_index=True, max_length=200)
    employees = RelationshipTo(
        'uemployees.employee.models.Employee',
        'WORK_AT_DEPARTMENT',
        model=WorkAtDepartment
    )

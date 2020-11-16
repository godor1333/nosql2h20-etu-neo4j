from flask_restful import Resource
from flask import request
from neomodel import db

from uemployees.department.models import Department


def getLessons(emp_id, dis_id):
    lessons = [
        lesson[0].items()
        for lesson in db.cypher_query(
            f'MATCH (e:Employee)'
            f'-[r:TEACH_A_DISCIPLINE]->(d:Discipline) '
            f'WHERE id(e)={emp_id} AND id(d)={dis_id} '
            f'RETURN r;'
        )[0]
    ]

    return [{
        k: v for k, v in lesson
    } for lesson in lessons]


def getUniqueDisciplines(desciplines):
    unique_disciplines = []
    for discipline in desciplines:
        if discipline not in unique_disciplines:
            unique_disciplines.append(discipline)
    return unique_disciplines


class EmployeeView(Resource):
    def get(self):
        response = []

        args = request.args
        department_id = args.get('department_id')

        try:
            department = Department(id=int(department_id))
            department.refresh()
        except Exception:
            return '', 400

        employees = department.employees.all()

        disciplines = []
        for employee in employees:
            response.append({
                **employee.__properties__,
                'job_title': department.employees.relationship(employee).job_title,
                'disciplines': [
                    {
                        'discipline': discipline.__properties__,
                        'lessons': getLessons(employee.id, discipline.id)
                    } for discipline in getUniqueDisciplines(employee.disciplines.all())
                ],
                'degrees': [
                    degree.__properties__ for degree in employee.degrees.all()
                ],
                'interests': [
                    interest.__properties__ for interest in employee.interests.all()
                ],
                'publications': [
                    publication.__properties__ for publication in employee.publications.all()
                ],
            })

        return response

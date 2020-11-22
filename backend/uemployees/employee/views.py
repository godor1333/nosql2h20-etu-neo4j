from flask_restful import Resource
from flask import request
from neomodel import db

from uemployees.department.models import Department
from uemployees.employee.models import Employee
from uemployees.discipline.models import Discipline


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


def getDiscipline(discipline_id):
    discipline_node = db.cypher_query(
            f'MATCH (e:Discipline) '
            f'WHERE id(e)={discipline_id} '
            f'RETURN e;'
        )[0][0][0]

    discipline = {
        k: v for k, v in discipline_node.items()
    }

    discipline['id'] = discipline_node.id
    return discipline


class EmployeeListView(Resource):
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

    def post(self):
        response = []

        name = request.form.get('name')
        email = request.form.get('email')
        education = request.form.get('education')
        job_title = request.form.get('job_title')
        disciplines = request.form.get('disciplines')
        degrees = request.form.get('degrees')
        interests = request.form.get('interests')
        publications = request.form.get('publications')

        employee = Employee(
            name=name,
            email=email,
            education=education,
            job_title=job_title,
        )
        employee.save()

        for discipline in disciplines:
            

        return response


class EmployeeView(Resource):
    def get(self, employee_id):
        try:
            employee = Employee(id=int(employee_id))
            employee.refresh()
        except Exception:
            return '', 400

        args = request.args
        department_id = args.get('department_id', default=employee.department.all()[0].id)

        try:
            department = list(filter(lambda d: d.id == int(department_id), employee.department.all()))[0]
        except Exception:
            return '', 400

        response = {
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
        }

        return response


class EmployeeScheduleView(Resource):
    def get(self, employee_id):

        args = request.args
        discipline_id = args.get('discipline_id')

        try:
            employee = Employee(id=int(employee_id))
            employee.refresh()
        except Exception:
            return '', 400

        try:
            discipline = getDiscipline(discipline_id)
        except Exception:
            return '', 400

        response = {
            'discipline': discipline,
            'lessons': getLessons(employee.id, discipline['id'])
        }

        return response

from flask_restful import Resource
from flask import request
from neomodel import db

from uemployees.faculty.models import Faculty
from uemployees.department.models import Department
from uemployees.degree.models import Degree

from uemployees.employee.views import (
    getUniqueDisciplines,
    getLessons
)


class SearchQueryView(Resource):
    def get(self):
        response = []

        args = request.args
        department_id = args.get('department_id')
        query = args.get("query")

        try:
            department = Department(id=int(department_id))
            department.refresh()
        except Exception:
            return '', 400

        filtered_employees = list(filter(lambda e: e.name.lower().find(query.lower()) != -1, department.employees.all()))

        for employee in filtered_employees:
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

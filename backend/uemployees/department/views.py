from flask_restful import (
    Resource
)

from uemployees.faculty.models import Faculty


class DepartmentView(Resource):
    def get(self):
        response = []

        for faculty in Faculty.nodes.all():
            response.append({
                **faculty.__properties__,
                'departments': [
                    department.__properties__ for department in faculty.departments.all()
                ]
            })

        return response

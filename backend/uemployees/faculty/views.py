from flask_restful import (
    Resource,
    reqparse
)
from neomodel.exception import UniqueProperty

from uemployees.faculty.models import Faculty
from uemployees.faculty.parser import faculty_args


class FacultyView(Resource):
    def get(self):
        return [group.__properties__ for group in Faculty.nodes.all()]

    def post(self):
        new_faculty = {
            'name': faculty_args['name'],
        }

        try:
            faculty = Faculty(**new_faculty).save()
        except UniqueProperty as e:
            return {
                "error": str(e)
            }, 400

        return faculty.__properties__, 201

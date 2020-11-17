from flask_restful import Resource

from uemployees.faculty.models import Faculty


class FacultyView(Resource):
    def get(self):
        return [faculty.__properties__ for faculty in Faculty.nodes.all()]

    # def post(self):
    #     faculty_args = get_faculty_parser()
    #
    #     new_faculty = {
    #         'name': faculty_args['name'],
    #     }
    #
    #     try:
    #         faculty = Faculty(**new_faculty).save()
    #     except UniqueProperty as e:
    #         return {
    #             "error": str(e)
    #         }, 400
    #
    #     return faculty.__properties__, 201

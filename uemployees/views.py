from flask_restful import (
    Resource,
    reqparse
)
from neomodel.exception import UniqueProperty

from uemployees.models import Group


class GroupView(Resource):
    def get(self):
        return [group.__properties__ for group in Group.nodes.all()]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'number',
            type=int,
            required=True,
            help='Number of the group is required and must be int'
        )
        parser.add_argument(
            'num_of_students',
            type=int,
            required=True,
            help='Number of students in the group is required and must be int'
        )
        args = parser.parse_args()
        print(args)
        new_group = {
            'number': args['number'],
            'num_of_students': args['num_of_students']
        }

        try:
            group = Group(**new_group).save()
        except UniqueProperty as e:
            return {
                "error": str(e)
            }, 400

        return group.__properties__, 201

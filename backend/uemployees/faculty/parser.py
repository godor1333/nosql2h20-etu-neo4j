from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument(
    'name',
    type=str,
    required=True,
    help='Faculty name must be set and the maximum length of the faculty name is 50 characters'
)

faculty_args = parser.parse_args()

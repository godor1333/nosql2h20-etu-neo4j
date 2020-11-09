from flask import Flask
from flask_restful import Api
from flask_cors import CORS, cross_origin

from uemployees.db import init_db
from uemployees.faculty.views import FacultyView
from uemployees.department.views import DepartmentView


init_db()

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['BUNDLE_ERRORS'] = True

api = Api(app)


api.add_resource(FacultyView, '/faculties/')
api.add_resource(DepartmentView, '/departments/')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

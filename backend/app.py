from flask import Flask
from flask_restful import Api
from flask_cors import CORS, cross_origin

from uemployees.db import init_db
from uemployees.faculty.views import FacultyView
from uemployees.department.views import DepartmentView
from uemployees.export.views import ExportView
from uemployees.employee.views import (
    EmployeeListView,
    EmployeeView,
    EmployeeScheduleView
)

init_db()

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['BUNDLE_ERRORS'] = True

api = Api(app)


api.add_resource(FacultyView, '/faculties/')
api.add_resource(DepartmentView, '/departments/')
api.add_resource(ExportView, '/export_document/')
api.add_resource(EmployeeScheduleView, '/employees/<employee_id>/schedule/')
api.add_resource(EmployeeView, '/employees/<employee_id>')
api.add_resource(EmployeeListView, '/employees/')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

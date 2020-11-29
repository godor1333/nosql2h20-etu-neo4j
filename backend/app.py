import threading
import time

from flask import Flask
from flask_restful import Api
from flask_cors import CORS, cross_origin

from uemployees.db import (
    init_db,
    load_db_data
)
from uemployees.faculty.views import FacultyView
from uemployees.department.views import DepartmentView
from uemployees.import_export.views import (
    ExportView,
    ImportView,
    GetCSVView
)
from uemployees.employee.views import (
    EmployeeListView,
    EmployeeView,
    EmployeeScheduleView,
    JobTitleList,
    DisciplineList,
    DegreeList,
    EmployeeFilterView
)
from uemployees.search.views import (
    SearchView,
    ParamsSearchView
)
from uemployees.statistic.views import (
    StatisticView,
    ParamsStatisticView
)
from uemployees.search_in_department.views import SearchQueryView

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['BUNDLE_ERRORS'] = True

api = Api(app)

# waiting db initialization
time.sleep(40)

init_db()
threading.Timer(3, load_db_data, args=['etu-neo4j.xlsx']).start()

api.add_resource(FacultyView, '/faculties/')
api.add_resource(DepartmentView, '/departments/')
api.add_resource(ExportView, '/export_document/')
api.add_resource(ImportView, '/import_document/')
api.add_resource(EmployeeFilterView, '/employees/filter')
api.add_resource(EmployeeScheduleView, '/employees/<employee_id>/schedule/')
api.add_resource(EmployeeView, '/employees/<employee_id>/')
api.add_resource(EmployeeListView, '/employees/')
api.add_resource(JobTitleList, '/job_titles/')
api.add_resource(DisciplineList, '/disciplines/')
api.add_resource(DegreeList, '/degrees/')

api.add_resource(ParamsSearchView, '/searchparams/')
api.add_resource(SearchView, '/search/')

api.add_resource(SearchQueryView, '/searchquery/')

# For internal usage
api.add_resource(GetCSVView, '/import/<file_name>')


api.add_resource(ParamsStatisticView, '/statisticparams/')
api.add_resource(StatisticView, '/statistic/')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

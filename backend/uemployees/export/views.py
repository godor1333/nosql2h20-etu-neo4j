import os

from flask_restful import Resource
from flask import send_file
from openpyxl import Workbook


def createFacultySheet(wb):
    faculty = wb.create_sheet('faculty')
    faculty['A1'] = 'id'
    faculty['B1'] = 'name'


def createDepartmentSheet(wb):
    department = wb.create_sheet('department')
    department['A1'] = 'id'
    department['B1'] = 'name'
    department['C1'] = "id_faculty"


def createEmployeeSheet(wb):
    department = wb.create_sheet('employee')
    department['A1'] = 'id'
    department['B1'] = 'name'
    department['C1'] = 'photo_url'
    department['D1'] = 'email'
    department['E1'] = 'education'


def createEmployeeDepartmentSheet(wb):
    department = wb.create_sheet('employee_department')
    department['A1'] = 'id_department'
    department['B1'] = 'id_employee'
    department['C1'] = 'job_title'


def createPublicationSheet(wb):
    department = wb.create_sheet('publication')
    department['A1'] = 'id'
    department['B1'] = 'content'
    department['C1'] = 'id_employee'


def createDegreeSheet(wb):
    department = wb.create_sheet('degree')
    department['A1'] = 'id'
    department['B1'] = 'content'


def createEmployeeDegreeSheet(wb):
    department = wb.create_sheet('employee_degree')
    department['A1'] = 'id_employee'
    department['B1'] = 'id_degree'


def createDisciplineSheet(wb):
    department = wb.create_sheet('discipline')
    department['A1'] = 'id'
    department['B1'] = 'name'


def createEmployeeDisciplineSheet(wb):
    department = wb.create_sheet('employee_discipline')
    department['A1'] = 'id_employee'
    department['B1'] = 'id_discipline'
    department['C1'] = 'group'
    department['D1'] = 'time'
    department['E1'] = 'auditorium'


def createExportFile(file_name):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(THIS_FOLDER, file_name)

    wb = Workbook()

    createFacultySheet(wb)
    createDepartmentSheet(wb)
    createEmployeeSheet(wb)
    createEmployeeDepartmentSheet(wb)
    createPublicationSheet(wb)
    createDegreeSheet(wb)
    createEmployeeDegreeSheet(wb)
    createDisciplineSheet(wb)
    createEmployeeDisciplineSheet(wb)

    wb.save(file_path)

    return file_path


class ExportView(Resource):
    def get(self):
        file_name = 'document_export.xlsx'
        file_path = createExportFile(file_name)

        response = send_file(
            file_path,
            as_attachment=True,
            attachment_filename=file_name,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            cache_timeout=0
        )

        response.headers["Content-Length"] = os.path.getsize(file_path)
        response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name)
        response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        return response

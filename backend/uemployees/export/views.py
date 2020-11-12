import os

from flask_restful import (Resource)
from flask import (send_from_directory, send_file)
from openpyxl import Workbook


class ExportView(Resource):
    def get(self):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        my_file = os.path.join(THIS_FOLDER, 'test.xlsx')

        wb = Workbook()
        faculty = wb.create_sheet("faculty")
        faculty['A1'] = "id"
        faculty['B1'] = "name"

        wb.save(my_file)

        response = send_file(
            my_file,
            as_attachment=True,
            attachment_filename="test.xlsx",
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        response.headers["Content-Length"] = os.path.getsize(my_file)
        response.headers["Content-Disposition"] = "attachment; filename=test.xlsx"
        response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        return response

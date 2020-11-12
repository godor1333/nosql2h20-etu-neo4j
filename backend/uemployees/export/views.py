import io

from flask_restful import (Resource)
from flask import (send_from_directory,send_file)
from openpyxl import Workbook


class ExportView(Resource):
    def get(self):

        return "Тут должне отправляться файл через один из методов send_from_directory, send_file"

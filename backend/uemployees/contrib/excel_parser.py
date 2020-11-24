import csv
import os
import errno

import xlrd


def csvFromExcelParser(excel_file):
    wb = xlrd.open_workbook(os.path.abspath(excel_file))
    sheets = ['faculty', 'department', 'employee',
              'employee_department', 'publication', 'degree',
              'employee_degree', 'discipline', 'employee_discipline']

    if not os.path.exists(os.path.dirname('tmp/filename')):
        try:
            os.makedirs(os.path.dirname('tmp/filename'))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    for sheet in sheets:
        sh = wb.sheet_by_name(sheet)
        csv_file = open(os.path.abspath(f'tmp/{sheet}.csv'), 'w')
        wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

        for rownum in range(sh.nrows):
            wr.writerow(sh.row_values(rownum))

        csv_file.close()

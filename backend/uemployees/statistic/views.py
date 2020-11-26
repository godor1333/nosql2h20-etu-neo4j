from itertools import groupby
from operator import itemgetter

from flask_restful import Resource
from flask import request
from neomodel import db

from uemployees.faculty.models import Faculty
from uemployees.department.models import Department

JOB_PARAM = 1
DEGREE_PARAM = 2


class StatisticView(Resource):
    def get(self):
        args = request.args
        faculty_id = args.get("faculty_id", default=None)
        department_id = args.get("department_id", default=None)
        param_id = int(args.get("param_id"))

        faculty_where = ""
        if faculty_id is not None:
            faculty_where = f" WHERE id(f)={faculty_id}"

        department_where = ""
        if department_id is not None:
            department_where = f" WHERE id(d)={department_id}"

        answer = db.cypher_query(
            f"MATCH (f:Faculty)-[:DEPARTMENT_OF_FACULTY]->(d:Department){faculty_where} "
            f"MATCH (d)-[w:WORK_AT_DEPARTMENT]->(e:Employee){department_where} "
            f"MATCH (e)-[:EMPLOYEE_HAS_DEGREE]->(deg:Degree) "
            f"RETURN f,d,w,e,deg"
        )[0]

        employees = []

        for block in answer:
            nodes = [{k: v for k, v in node.items()} for node in block]

            employees.append({
                "id": nodes[3]["id"],
                "name": nodes[3]["name"],
                "faculty": nodes[0]["name"],
                "department": nodes[1]["name"],
                "job": nodes[2]["job_title"],
                "degree": nodes[4]["content"]
            })

        key = ""
        if param_id == JOB_PARAM:
            key = "job"
        elif param_id == DEGREE_PARAM:
            key = "degree"
        else:
            return {
                "error": "param_id doesn't exist"
            }, 400

        groups = {}

        for e in employees:
            if e[key] not in groups:
                groups[e[key]] = []
            groups[e[key]].append(e["id"])

        if param_id == DEGREE_PARAM:
            for k in groups:
                groups[k] = set(groups[k])

        return [{"x": k, "y": len(groups[k])} for k in groups]


class ParamsStatisticView(Resource):
    def get(self):
        return {
            "faculties": [{"id": faculty.id, "name": faculty.name} for faculty in Faculty.nodes.all()],
            "departments": [{"id": department.id, "name": department.name} for department in Department.nodes.all()],
            "params": [
                {
                    "id": JOB_PARAM,
                    "name": "Должность"
                },
                {
                    "id": DEGREE_PARAM,
                    "name": "Ученная степень"
                }
            ]
        }

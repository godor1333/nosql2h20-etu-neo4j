from flask_restful import Resource
from flask import request
from neomodel import db

from uemployees.faculty.models import Faculty
from uemployees.department.models import Department
from uemployees.degree.models import Degree


def getJobs():
    w = [job[0].items() for job in db.cypher_query("MATCH (d)-[w:WORK_AT_DEPARTMENT]->(e) RETURN w")[0]]
    jobs = set([{k: v for k, v in job}["job_title"] for job in w])
    return list(jobs)


class SearchView(Resource):
    def get(self):
        args = request.args
        faculty_id = args.get("faculty_id", default=None)
        department_id = args.get("department_id", default=None)
        job_title = args.get("job_title", default=None)
        degree_id = args.get("degree_id", default=None)

        faculty_where = ""
        if faculty_id is not None:
            faculty_where = f" WHERE id(f)={faculty_id}"

        department_where = ""
        if department_id is not None and job_title is not None:
            department_where = f" WHERE id(d)={department_id} AND w.job_title='{job_title}'"
        elif department_id is not None and job_title is None:
            department_where = f" WHERE id(d)={department_id}"
        elif department_id is None and job_title is not None:
            department_where = f" WHERE w.job_title='{job_title}'"

        degree_where = ""
        if degree_id is not None:
            degree_where = f" WHERE id(deg)={degree_id}"

        answer = db.cypher_query(
            f"MATCH (f:Faculty)-[:DEPARTMENT_OF_FACULTY]->(d:Department){faculty_where} "
            f"MATCH (d)-[w:WORK_AT_DEPARTMENT]->(e:Employee){department_where} "
            f"MATCH (e)-[:EMPLOYEE_HAS_DEGREE]->(deg:Degree){degree_where} "
            f"RETURN f,d,w,e,deg"
        )[0]

        employees = []

        for block in answer:
            nodes = [{k: v for k, v in node.items()} for node in block]

            employees.append({
                "name": nodes[3]["name"],
                "faculty": nodes[0]["name"],
                "department": nodes[1]["name"],
                "job": nodes[2]["job_title"],
                "degree": nodes[4]["content"]
            })

        return employees


class ParamsSearchView(Resource):
    def get(self):
        return {
            "faculties": [{"id": faculty.id, "name": faculty.name} for faculty in Faculty.nodes.all()],
            "departments": [{"id": department.id, "name": department.name} for department in Department.nodes.all()],
            "jobs": getJobs(),
            "degrees": [{"id": degree.id, "content": degree.content} for degree in Degree.nodes.all()]
        }

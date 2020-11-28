from flask_restful import Resource
from flask import request, redirect
from neomodel import db

from uemployees.department.models import Department
from uemployees.employee.models import Employee
from uemployees.discipline.models import Discipline
from uemployees.degree.models import Degree
from uemployees.interest.models import Interest
from uemployees.publication.models import Publication


def getLessons(emp_id, dis_id):
    lessons = [
        lesson[0].items()
        for lesson in db.cypher_query(
            f'MATCH (e:Employee)'
            f'-[r:TEACH_A_DISCIPLINE]->(d:Discipline) '
            f'WHERE id(e)={emp_id} AND id(d)={dis_id} '
            f'RETURN r;'
        )[0]
    ]

    return [{
        k: v for k, v in lesson
    } for lesson in lessons]


def getUniqueDisciplines(desciplines):
    unique_disciplines = []
    for discipline in desciplines:
        if discipline not in unique_disciplines:
            unique_disciplines.append(discipline)
    return unique_disciplines


def getDiscipline(discipline_id):
    discipline_node = db.cypher_query(
        f'MATCH (e:Discipline) '
        f'WHERE id(e)={discipline_id} '
        f'RETURN e;'
    )[0][0][0]

    discipline = {
        k: v for k, v in discipline_node.items()
    }

    discipline['id'] = discipline_node.id
    return discipline


class JobTitleList(Resource):
    def get(self):
        rels = [
            rel[0]
            for rel in db.cypher_query(
                f'MATCH ()'
                f'-[r:WORK_AT_DEPARTMENT]->() '
                f'RETURN DISTINCT r.job_title;'
            )[0]
        ]

        result = []

        for rel in rels:
            result.append({
                "job_title": rel
            })

        return result


class DegreeList(Resource):
    def get(self):
        rels = [
            rel[0]
            for rel in db.cypher_query(
                f'MATCH ()'
                f'-[r:EMPLOYEE_HAS_DEGREE]->(d:Degree) '
                f'RETURN DISTINCT d.content;'
            )[0]
        ]

        result = []

        for rel in rels:
            result.append({
                "degree": rel
            })

        return result


class DisciplineList(Resource):
    def get(self):
        rels = [
            rel[0]
            for rel in db.cypher_query(
                f'MATCH ()'
                f'-[r:TEACH_A_DISCIPLINE]->(d:Discipline) '
                f'RETURN DISTINCT d.name;'
            )[0]
        ]

        result = []

        for rel in rels:
            result.append({
                "discipline": rel
            })

        return result


class EmployeeFilterView(Resource):
    def get(self):
        response = []

        args = request.args
        department_id = args.get('department_id')
        job_title = args.get('job_title')
        degree = args.get('degree')
        discipline = args.get('discipline')
        email = args.get('email')
        education = args.get('education')
        interest = args.get('interest')
        publication = args.get('publication')

        try:
            department = Department(id=int(department_id))
            department.refresh()
        except Exception:
            return '', 400

        employees = department.employees.all()

        for employee in employees:
            if job_title and department.employees.relationship(employee).job_title != job_title or \
                    degree and degree in [degree.__properties__.content for degree in employee.degrees.all()] or \
                    discipline and discipline in [discipline.__properties__.name for discipline in getUniqueDisciplines(employee.disciplines.all())] or \
                    email and email != employee.email or \
                    education and education != employee.education or \
                    interest and interest in [interest.__properties__.content for interest in employee.interests.all()] or \
                    publication and publication in [publication.__properties__.content for publication in employee.publications.all()]:
                continue
            else:
                response.append({
                    **employee.__properties__,
                    'job_title': department.employees.relationship(employee).job_title,
                    'disciplines': [
                        {
                            'discipline': discipline.__properties__,
                            'lessons': getLessons(employee.id, discipline.id)
                        } for discipline in getUniqueDisciplines(employee.disciplines.all())
                    ],
                    'degrees': [
                        degree.__properties__ for degree in employee.degrees.all()
                    ],
                    'interests': [
                        interest.__properties__ for interest in employee.interests.all()
                    ],
                    'publications': [
                        publication.__properties__ for publication in employee.publications.all()
                    ],
                })

        return response


class EmployeeListView(Resource):
    def get(self):
        response = []

        args = request.args
        department_id = args.get('department_id')

        try:
            department = Department(id=int(department_id))
            department.refresh()
        except Exception:
            return '', 400

        employees = department.employees.all()

        for employee in employees:
            response.append({
                **employee.__properties__,
                'job_title': department.employees.relationship(employee).job_title,
                'disciplines': [
                    {
                        'discipline': discipline.__properties__,
                        'lessons': getLessons(employee.id, discipline.id)
                    } for discipline in getUniqueDisciplines(employee.disciplines.all())
                ],
                'degrees': [
                    degree.__properties__ for degree in employee.degrees.all()
                ],
                'interests': [
                    interest.__properties__ for interest in employee.interests.all()
                ],
                'publications': [
                    publication.__properties__ for publication in employee.publications.all()
                ],
            })

        return response

    def post(self):
        name = request.json.get('name')
        email = request.json.get('email') or ""
        education = request.json.get('education') or ""
        job_title = request.json.get('job_title') or ""
        disciplines = request.json.get('disciplines') or []
        degrees = request.json.get('degrees') or []
        interests = request.json.get('interests') or []
        publications = request.json.get('publications') or []
        department = request.json.get('department') or []

        db.begin()
        try:
            employee = Employee(
                name=name,
                email=email,
                education=education,
                job_title=job_title,
            )
            employee.save()

            department = Department.nodes.get_or_none(name=department)

            if not department:
                return {
                           "error": "Department doesn't exist"
                       }, 400

            department.employees.connect(employee, {
                'job_title': job_title
            })

            for d in disciplines:
                discipline = Discipline.nodes.get_or_none(name=d['discipline']['name'])
                if not discipline:
                    discipline = Discipline(name=d['discipline']['name']).save()
                for lesson in d['lessons']:
                    employee.disciplines.connect(discipline, {
                        **lesson
                    })

            for d in degrees:
                degree = Degree.nodes.get_or_none(content=d['content'])
                if not degree:
                    degree = Degree(content=d['content']).save()
                employee.degrees.connect(degree)

            for i in interests:
                interest = Interest.nodes.get_or_none(content=i['content'])
                if not interest:
                    interest = Interest(content=i['content']).save()
                employee.interests.connect(interest)

            for p in publications:
                publication = Publication.nodes.get_or_none(content=p['content'])
                if not publication:
                    publication = Publication(content=p['content']).save()
                employee.publications.connect(publication)
            db.commit()
        except Exception as e:
            db.rollback()
            return {
                       "error": str(e)
                   }, 400

        response = {
            **employee.__properties__,
            'job_title': department.employees.relationship(employee).job_title,
            'disciplines': [
                {
                    'discipline': discipline.__properties__,
                    'lessons': getLessons(employee.id, discipline.id)
                } for discipline in getUniqueDisciplines(employee.disciplines.all())
            ],
            'degrees': [
                degree.__properties__ for degree in employee.degrees.all()
            ],
            'interests': [
                interest.__properties__ for interest in employee.interests.all()
            ],
            'publications': [
                publication.__properties__ for publication in employee.publications.all()
            ],
        }

        return response


class EmployeeView(Resource):
    def get(self, employee_id):
        try:
            employee = Employee(id=int(employee_id))
            employee.refresh()
        except Exception:
            return '', 400

        args = request.args
        department_id = args.get('department_id', default=employee.department.all()[0].id)

        try:
            department = list(filter(lambda d: d.id == int(department_id), employee.department.all()))[0]
        except Exception:
            return '', 400

        response = {
            **employee.__properties__,
            'job_title': department.employees.relationship(employee).job_title,
            'disciplines': [
                {
                    'discipline': discipline.__properties__,
                    'lessons': getLessons(employee.id, discipline.id)
                } for discipline in getUniqueDisciplines(employee.disciplines.all())
            ],
            'degrees': [
                degree.__properties__ for degree in employee.degrees.all()
            ],
            'interests': [
                interest.__properties__ for interest in employee.interests.all()
            ],
            'publications': [
                publication.__properties__ for publication in employee.publications.all()
            ],
        }

        return response

    def put(self, employee_id):
        name = request.json.get('name')
        email = request.json.get('email')
        education = request.json.get('education')
        job_title = request.json.get('job_title')
        disciplines = request.json.get('disciplines')
        degrees = request.json.get('degrees')
        interests = request.json.get('interests')
        publications = request.json.get('publications')

        try:
            employee = Employee(id=int(employee_id))
            employee.refresh()
        except Exception:
            return {
                       "error": "Employee not found"
                   }, 400

        employee.name = name or employee.name
        employee.email = email or employee.email
        employee.education = education or employee.education
        employee.save()

        department = employee.department.all()[0]

        rel_employee = employee.department.relationship(department)
        rel_employee.job_title = job_title or rel_employee.job_title
        rel_employee.save()

        if disciplines:
            db.cypher_query(f"MATCH (e:Employee)-[rel]-(d:Discipline) WHERE id(e)={employee.id} DELETE rel;")
            for d in disciplines:
                discipline = Discipline.nodes.get_or_none(name=d['discipline']['name'])
                if not discipline:
                    discipline = Discipline(name=d['discipline']['name']).save()
                for lesson in d['lessons']:
                    employee.disciplines.connect(discipline, {
                        **lesson
                    })

        if degrees:
            db.cypher_query(f"MATCH (e:Employee)-[rel]-(d:Degree) WHERE id(e)={employee.id} DELETE rel;")
            for d in degrees:
                degree = Degree.nodes.get_or_none(content=d['content'])
                if not degree:
                    degree = Degree(content=d['content']).save()
                employee.degrees.connect(degree)

        if interests:
            db.cypher_query(f"MATCH (e:Employee)-[rel]-(i:Interest) WHERE id(e)={employee.id} DELETE rel;")
            for i in interests:
                interest = Interest.nodes.get_or_none(content=i['content'])
                if not interest:
                    interest = Interest(content=i['content']).save()
                employee.interests.connect(interest)

        if publications:
            db.cypher_query(f"MATCH (e:Employee)-[rel]-(p:Publication) WHERE id(e)={employee.id} DELETE rel;")
            for p in publications:
                publication = Publication.nodes.get_or_none(content=p['content'])
                if not publication:
                    publication = Publication(content=p['content']).save()
                employee.publications.connect(publication)

        response = {
            **employee.__properties__,
            'job_title': department.employees.relationship(employee).job_title,
            'disciplines': [
                {
                    'discipline': discipline.__properties__,
                    'lessons': getLessons(employee.id, discipline.id)
                } for discipline in getUniqueDisciplines(employee.disciplines.all())
            ],
            'degrees': [
                degree.__properties__ for degree in employee.degrees.all()
            ],
            'interests': [
                interest.__properties__ for interest in employee.interests.all()
            ],
            'publications': [
                publication.__properties__ for publication in employee.publications.all()
            ],
        }

        return response

class EmployeeScheduleView(Resource):
    def get(self, employee_id):

        args = request.args
        discipline_id = args.get('discipline_id')

        try:
            employee = Employee(id=int(employee_id))
            employee.refresh()
        except Exception:
            return '', 400

        try:
            discipline = getDiscipline(discipline_id)
        except Exception:
            return '', 400

        response = {
            'discipline': discipline,
            'lessons': getLessons(employee.id, discipline['id'])
        }

        return response

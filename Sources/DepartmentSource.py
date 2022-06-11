import csv

from Models import Department as D
from Sources import DisciplineSource as DS


class DepartmentSource:

    source = []

    def __init__(self):
        self.load_data()

    def add_source(self, department):
        self.source.append(department)

    def check_source(self, id, name, departments):
        result = (id in departments) and (name.find('Резерв') == -1)

        return result

    def load_data(self):
        departments = [d.department for d in DS.DisciplineSource.source]

        with open('SourceFiles/department.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')

            for row in reader:
                if (row[0] not in ['', 'id']) and (row[2] != '') and (row[4] == 'кафедра'):

                    d_id = row[0][1:]
                    d_name = row[2]

                    if self.check_source(d_id, d_name, departments):
                        department = D.Department(d_id, d_name)
                        self.add_source(department)

    def get_department(id):
        result = [d for d in DepartmentSource.source if d.id == id][0].name

        return result

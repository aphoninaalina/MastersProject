import csv

from Models import Auditorium as A
from Sources import CampusSource as CS, DepartmentSource as DeS


class AuditoriumSource:

    source = []

    def __init__(self):
        self.load_data()

    def add_source(self, auditorium):
        self.source.append(auditorium)

    def get_department(self, name):
        result = name.replace('кафедра ', '')
        result = name.replace('"', '')

        return result

    def check_source(self, department, departments):
        result = department in departments

        return result

    def define_department(self, name):
        result = [d.id for d in DeS.DepartmentSource.source if name == d.name][0]

        return result

    def define_campus(self, building):
        result = [c.name for c in CS.CampusSource.source if building in c.buildings][0]

        return result

    def load_data(self):
        departments = [d.name for d in DeS.DepartmentSource.source]

        with open('SourceFiles/auditorium.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')

            for row in reader:
                if (row[0] != '') and (row[1] != '') and (row[2] != '') and \
                   (row[6] not in ['', 'Закрепление (кафедра/подразделение)']) and \
                   (row[8] != '') and (row[9] == '(+)') and (row[10] != ''):

                    a_number = row[0]
                    a_type = row[8]
                    a_floor = row[2]
                    a_building = row[1]

                    department = self.get_department(row[6])

                    if self.check_source(department, departments):
                        a_department = self.define_department(department)
                    else:
                        a_department = 'Extra'

                    a_campus = self.define_campus(a_building)

                    auditorium = A.Auditorium(a_number, a_type, a_floor, a_building, a_campus, a_department)

                    self.add_source(auditorium)

    def refactor_sources(di_source, de_source):
        d_departments = set([d.department for d in di_source])
        a_departments = set([a.department for a in AuditoriumSource.source])

        common = [d for d in d_departments if d in a_departments]

        di_source[:] = [d for d in di_source if d.department in common]
        de_source[:] = [d for d in de_source if d.id in common]

    def get_auditoriums(department):
        result = [a for a in AuditoriumSource.source if a.department == department]

        return result

    def get_extras():
        result = [a for a in AuditoriumSource.source if a.department == 'Extra']

        return result

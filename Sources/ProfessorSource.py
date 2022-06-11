import csv

from Models import Professor as P
from Sources import DisciplineSource as DS


class ProfessorSource:

    source = []

    def __init__(self):
        self.load_data()
        self.source[:] = set(self.source)

    def add_source(self, professor):
        self.source.append(professor)

    def load_data(self):
        with open('SourceFiles/timetable.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')

            for row in reader:
                if (row[7] not in ['', 'Name']) and (row[13] not in ['', '0']):

                    p_id = f'p_{row[13]}'
                    p_name = row[7]

                    professor = P.Professor(p_id, p_name)
                    self.add_source(professor)

    def refactor_source():
        professors = set([d.professor for d in DS.DisciplineSource.source])

        ProfessorSource.source[:] = [p for p in ProfessorSource.source if p.id in professors]

    def get_professor(id):
        result = [p for p in ProfessorSource.source if p.id == id][0]

        return result

    def get_id(name):
        result = [p.id for p in ProfessorSource.source if p.name == name][0]

        return result

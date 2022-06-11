import csv

from Models import Discipline as D


class DisciplineSource:

    source = []

    def __init__(self):
        self.load_data()
        self.source[:] = set(self.source)

    def add_source(self, discipline):
        self.source.append(discipline)

    def load_data(self):
        with open('SourceFiles/timetable.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            i = 0
            for row in reader:
                if (row[0] not in ['', 'Group']) and (row[9] != '') and (row[10] != '') and \
                   (row[10] in ['л.', 'пр.', 'лаб.']) and (row[12] not in ['', '0']) and (row[13] not in ['',  '0']):

                    d_name = row[9]
                    d_type = row[10]
                    d_group = row[0].replace(' ', '')
                    d_professor = f'p_{row[13]}'
                    d_department = row[12]

                    discipline = D.Discipline(d_name, d_type, d_group, d_professor, d_department)

                    self.add_source(discipline)

    def update_lecture(discipline, index):
        if len(DisciplineSource.source) != 0:
            indexes = [i for i,v in enumerate(DisciplineSource.source) if v.equal_lecture(discipline)]

            if len(indexes) > 2:
                indexes = indexes[:2]

            if len(indexes) != 0:
                for index_ in indexes:
                    DisciplineSource.source[index].group += f' {DisciplineSource.source[index_].group}'

                indexes.sort(reverse=True)

                for index_ in indexes:
                    del(DisciplineSource.source[index_])

    def update_lab_practice(discipline, index):
        if len(DisciplineSource.source) != 0:
            indexes = [i for i,v in enumerate(DisciplineSource.source) if v.equal_lab_practice(discipline)]

            if len(indexes) != 0:
                for index_ in indexes:
                    DisciplineSource.source[index].professor += f' {DisciplineSource.source[index_].professor}'

                indexes.sort(reverse=True)

                for index_ in indexes:
                    del(DisciplineSource.source[index_])

                DisciplineSource.source.append(discipline)

    def refactor_source():
        for index,discipline in enumerate(DisciplineSource.source):
            if discipline.type == 'л.':
                DisciplineSource.update_lecture(discipline, index)
            else:
                DisciplineSource.update_lab_practice(discipline, index)

    def get_disciplines(department):
        result = [d for d in DisciplineSource.source if d.department == department]

        return result

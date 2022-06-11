import csv

from Models import Group as G
from Sources import DisciplineSource as DS


class GroupSource:

    source = []

    def __init__(self):
        self.load_data()

    def add_source(self, group):
        self.source.append(group)

    def check_source(self, name, groups):
        result = name in groups

        return result

    def load_data(self):

        groups = set([d.group for d in DS.DisciplineSource.source])

        with open('SourceFiles/calendar.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')

            for row in reader:
                if (row[0] not in ['', 'Уровень']) and (row[1] != '') and (row[3] != ''):

                    g_level = row[0]
                    g_year = row[1]

                    groups_ = row[3].split(', ')

                    for group_ in groups_:
                        g_name = group_

                        if self.check_source(g_name, groups):
                            group = G.Group(g_name, g_level, g_year)
                            self.add_source(group)

    def refactor_source():
        groups = set([d.group for d in DS.DisciplineSource.source])

        GroupSource.source[:] = [g for g in GroupSource.source if g.name in groups]

    def refactor_sources(di_source):
        d_groups = set([d.group for d in di_source])
        g_groups = [g.name for g in GroupSource.source]

        common = [g for g in g_groups if g in d_groups]

        di_source[:] = [d for d in di_source if d.group in common]

    def get_group(id):
        result = [g for g in GroupSource.source if g.name == id][0]

        return result

import csv
from datetime import *

from Models import Discipline as D, TimetableCell as TC
from Sources import ProfessorSource as PS


class TimetableSource:

    source = []

    def add_source(timetable_cell):
        TimetableSource.source.append(timetable_cell)

    def write_to_csv():
        with open(f'Timetables/timetable_{str(datetime.now().strftime("%Y%m%d%H%M%S"))}.csv', 'w', newline='') as csvfile:
            write = csv.writer(csvfile, delimiter=';')

            write.writerow(['Group(s)', 'Day', 'Lesson', 'Auditorium(s)', 'Week', 'Professor(s)', 'Department', 'Subject', 'Type', 'ID(s)'])
            for cell in TimetableSource.source:
                group = cell.discipline.group
                day = (cell.day % 6) + 1
                lesson = cell.time + 1
                auditorium = cell.auditorium
                week = 1 if cell.day < 6 else 2
                professor = '/'.join([PS.ProfessorSource.get_professor(p).name for p in cell.discipline.professor.split(' ')])
                department = cell.discipline.department
                subject = cell.discipline.name
                type = cell.discipline.type
                ids = '/'.join([p.replace('p_', '') for p in cell.discipline.professor.split(' ')])

                write.writerow([group, day, lesson, auditorium, week, professor, department, subject, type, ids])

    def load_source(file):
        TimetableSource.source[:] = []

        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')

            for row in reader:
                if (row[0] != 'Group(s)'):

                    discipline = row[7]
                    type = row[8]
                    group = row[0]
                    #professor = ' '.join([f'p_{p}' for p in row[9].split(' ')])
                    professor = ' '.join([f'p_{p}' for p in row[9].split('/')])
                    department = row[6]

                    discipline_ = D.Discipline(discipline, type, group, professor, department)

                    auditorium = ' '.join([a for a in row[3].split('/')])
                    day = str((int(row[4]) - 1) * 6 + int(row[1]) - 1)
                    time = str(int(row[2]) - 1)

                    cell = TC.TimetableCell(discipline_, auditorium, day, time)
                    TimetableSource.add_source(cell)

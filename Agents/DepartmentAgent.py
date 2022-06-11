from functools import reduce

import numpy
import operator
import random
import jellyfish

from mesa import Agent

from Models import TimetableCell as TC

from Sources import AuditoriumSource as AS, ClassTypeSource as CTS,\
                    DisciplineSource as DiS, TimetableSource as TS


class DepartmentAgent(Agent):

    days = 12
    times = 7

    def __init__(self, id, model):
        super().__init__(id, model)

        self.id = id

        self.disciplines = DiS.DisciplineSource.get_disciplines(id).copy()

        self.auditoriums = AS.AuditoriumSource.get_auditoriums(id)

        self.define_estimates()
        self.define_campuses_information()

        self.fine = round(1 / len(self.disciplines), 2)

    def define_estimates(self):
        self.estimates = [[1.0 for j in range(self.times)] for i in range(self.days)]

    def define_campuses_information(self):
        campuses = [a.campus for a in self.auditoriums]
        campuses[:] = set(campuses)

        if len(campuses) > 1:
            max_count = 0
            for campus in campuses:
                count = len([a for a in self.auditoriums if a.campus == campus])
                if count > max_count:
                    max_count = count
                    self.main_campus = campus
        else:
            self.main_campus = campuses[0]

        self.campuses = campuses

    def get_estimates(self, discipline):
        result = [[0.0 for j in range(self.times)] for i in range(self.days)]

        estimates_source = []
        estimates_source += discipline.group.split(' ')
        estimates_source += discipline.professor.split(' ')

        estimates_source = [self.model.get_agent(s) for s in estimates_source]

        for day in range(self.days):
            for time in range(self.times):
                estimates = [s.estimates[day][time] for s in estimates_source]
                min_estimate = min(estimates)

                if min_estimate >= 0:
                    result[day][time] = reduce(operator.mul, [e for e in estimates if e > 0], 1) * self.estimates[day][time]
                else:
                    result[day][time] = min_estimate

        return result

    def refactor_estimates(self, discipline, day, time, auditoriums):
        groups = discipline.group.split(' ')
        for group_ in groups:
            group = self.model.get_agent(group_)

            group.refactor_estimates(day, time)

        professors = discipline.professor.split(' ')
        for professor_ in professors:
            professor = self.model.get_agent(professor_)

            professor.refactor_estimates(day, time)

        for auditorium_ in auditoriums:
            auditorium = self.model.get_agent(auditorium_.number)

            auditorium.refactor_estimates(day, time)

    def check_loaded(self, group, best):
        loaded = []
        loaded_once = []

        groups = group.split(' ')
        for group_ in groups:
            group = self.model.get_agent(group_)

            load = group.get_loaded()
            if len(load) != 0:
                loaded += load[0]
                loaded_once += load[1]

        if len(loaded_once) != 0:
            loaded_ = loaded_once
        else:
            loaded_ = loaded

        if len(loaded_) != 0:
            loaded_[:] = set(loaded_)

            result = [b for b in best if b[0] in loaded_]

            if len(result) != 0:
                best = result

        return best

    def get_members_campuses(self, members):
        result = []

        members = members.split(' ')
        for member_ in members:
            member = self.model.get_agent(member_)
            result.append(member.campuses)

        return result

    def get_members_auditoriums(self, members):
        result = []

        members = members.split(' ')
        for member_ in members:
            member = self.model.get_agent(member_)
            result.append(member.auditoriums)

        return result

    def define_auditoriums(self, discipline, day, time):
        result = []

        group_campuse = [c for c in [c[day] for c in self.get_members_campuses(discipline.group)] if c != '']
        group_campuse[:] = set(group_campuse)
        professor_campuse = [c for c in [c[day] for c in self.get_members_campuses(discipline.professor)] if c != '']
        professor_campuse[:] = set(professor_campuse)

        campus = group_campuse
        if len(campus) == 0:
            campus = professor_campuse
            if len(campus) == 0:
                campus = [self.main_campus]
        campus = campus[0]

        self_auditoriums = [a for a in self.auditoriums if a.campus == campus
                                    and a.type in CTS.ClassTypeSource.get_types(discipline.type)
                                    and self.model.get_agent(a.number).get_estimate(day, time) != -1]

        extra_auditoriums = [a for a in self.model.extra_auditoriums if a.campus == campus
                                     and a.type in CTS.ClassTypeSource.get_types(discipline.type)
                                     and self.model.get_agent(a.number).get_estimate(day, time) != -1]

        needed_count = len(discipline.professor.split(' '))
        auditoriums = self_auditoriums + extra_auditoriums

        if len(auditoriums) < needed_count:
            auditoriums += [a for a in AS.AuditoriumSource.source
                                    if a not in self.auditoriums + self.model.extra_auditoriums
                                    and a.campus == campus and a.type in CTS.ClassTypeSource.get_types(discipline.type)
                                    and self.model.get_agent(a.number).get_estimate(day, time) != -1]

        group_auditoriums = [c for c in [c[day] for c in self.get_members_auditoriums(discipline.group)] if c != '']
        group_auditoriums[:] = set(group_auditoriums)
        professor_auditoriums = [c for c in [c[day] for c in self.get_members_auditoriums(discipline.professor)] if c != '']
        professor_auditoriums[:] = set(professor_auditoriums)

        auditoriums_for_check = group_auditoriums
        if len(auditoriums_for_check) == 0:
            auditoriums_for_check = professor_auditoriums
            if len(auditoriums_for_check) == 0:
                auditoriums_for_check = [a.number for a in self_auditoriums]
                if len(auditoriums_for_check) == 0:
                    auditoriums_for_check = [a.number for a in extra_auditoriums]
                    if len(auditoriums_for_check) == 0:
                        auditoriums_for_check = [a.number for a in auditoriums]

        for_check = random.choice(auditoriums_for_check)
        auditoriums.sort(key=lambda a: jellyfish.damerau_levenshtein_distance(a.number, for_check))

        for i in range(needed_count):
            result.append(auditoriums.pop(0))

        return result

    def check_campuses(self, group, professor, estimates):
        campuses = []

        campuses += self.get_members_campuses(group)
        campuses += self.get_members_campuses(professor)

        for i in range(self.days):
            today_campuses = [c[i] for c in campuses if c[i] != '']
            if len(today_campuses) != 0:
                today_campuses[:] = set(today_campuses)
                if len(today_campuses) > 1:
                    estimates[i] = [-1 for j in range(self.times)]

        return estimates

    def step(self):
        discipline = self.disciplines[0]

        estimates = self.get_estimates(discipline)
        checked_estimates = self.check_campuses(discipline.group, discipline.professor, estimates)

        best = numpy.max(checked_estimates)

        best_list = numpy.asarray(numpy.where(checked_estimates == best)).T.tolist()
        best_list = self.check_loaded(discipline.group, best_list)

        day,time = random.choice(best_list)

        auditoriums = self.define_auditoriums(discipline, day, time)
        auditoriums_ = ' '.join([a.number for a in auditoriums])

        current_timetable_cell = TC.TimetableCell(discipline, auditoriums_, day, time)
        TS.TimetableSource.add_source(current_timetable_cell)

        self.estimates[day][time] -= self.fine
        self.refactor_estimates(discipline, day, time, auditoriums)

        members = f'{discipline.group} {discipline.professor}'.split(' ')
        for member_ in members:
            member = self.model.get_agent(member_)
            if member.campuses[day] == '':
                member.campuses[day] = auditoriums[0].campus
            if member.auditoriums[day] == '':
                member.auditoriums[day] = auditoriums[0].number

    def advance(self):
        del(self.disciplines[0])

        if len(self.disciplines) == 0:
            self.model.schedule.remove(self)

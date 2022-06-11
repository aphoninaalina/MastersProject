import numpy
from mesa import Agent

from Sources import GroupSource as GS, DisciplineSource as DS

class GroupAgent(Agent):

    days = 12
    times = 7

    def __init__(self, id, model):
        super().__init__(id, model)
        self.group = GS.GroupSource.get_group(id)

        self.define_middle_load()
        self.define_estimates()
        self.define_campuses()
        self.define_auditoriums()

    def define_middle_load(self):
        disciplines_count = len([d for d in DS.DisciplineSource.source if d.group.find(self.group.name) != -1])
        self.middle_load = round(disciplines_count / 12)

        if self.middle_load < 3:
            self.middle_load = 3

    def define_campuses(self):
        self.campuses = ['' for i in range(self.days)]

    def define_auditoriums(self):
        self.auditoriums = ['' for i in range(self.days)]

    def define_estimates(self):
        self.estimates = [[1.0 for j in range(self.times)] for i in range(self.days)]
        for i in range(self.days):
            self.inc_estimate(i, int(self.group.year) - 1)

    def refactor_estimates(self, day, time):
        self.reset_estimate(day, time)

        times_to_double = [time]

        load = len([e for e in self.estimates[day] if e == -1])
        if load >= self.middle_load:
            for time_ in range(self.times):
                if self.estimates[day][time_] != -1:
                    self.estimates[day][time_] = 0.0
        elif load > 1:
            used_estimate = numpy.min(self.estimates)

            if used_estimate == -1:
                times = numpy.asarray(numpy.where(self.estimates[day] == used_estimate)).T.tolist()
                times = [t for st in times for t in st]
                times.sort()

                between = [t for t in range(times[0], times[-1] + 1) if t not in times]
                if len(between) != 0:
                    for time_ in between:
                        self.double_estimate(day, time_)
                else:
                    times_to_double.append(min(times))
                    times_to_double.append(max(times))

        times_to_double[:] = set(times_to_double)

        for time_ in times_to_double:
            if time_ in range(self.times - 1):
                if self.estimates[day][time_ + 1] != -1:
                    self.double_estimate(day, time_ + 1)
            if time_ in range(1, self.times):
                if self.estimates[day][time_ - 1] != -1:
                    self.double_estimate(day, time_ - 1)

    def inc_estimate(self, day, time):
        self.estimates[day][time] += 1

    def double_estimate(self, day, time):
        self.estimates[day][time] *= 10

    def reset_estimate(self, day, time):
        self.estimates[day][time] = -1

    def get_loaded(self):
        result = []
        used_estimate = numpy.min(self.estimates)

        if used_estimate == -1:
            days = numpy.asarray(numpy.where(self.estimates == used_estimate)).T.tolist()
            if len(days) != 0:
                days = [d[0] for d in days]
                days_best = [d for d in days if len([e for e in self.estimates[d] if e == -1]) == 1]
                result = days, days_best

        return result
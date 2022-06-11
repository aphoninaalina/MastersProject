from mesa import Agent

class ProfessorAgent(Agent):

    days = 12
    times = 7

    def __init__(self, id, model):
        super().__init__(id, model)

        self.define_estimates()
        self.define_campuses()
        self.define_auditoriums()

    def define_estimates(self):
        self.estimates = [[1.0 for j in range(self.times)] for i in range(self.days)]

    def define_campuses(self):
        self.campuses = ['' for i in range(self.days)]

    def define_auditoriums(self):
        self.auditoriums = ['' for i in range(self.days)]

    def refactor_estimates(self, day, time):
        self.reset_estimate(day, time)

        load = len([e for e in self.estimates[day] if e == -1])
        if load >= 4:
            for time_ in range(self.times):
                if self.estimates[day][time_] != 0:
                    self.estimates[day][time_] = 0.0

        if time != 0:
            if self.estimates[day][time - 1] != -1:
                self.inc_estimate(day, time - 1)
        elif time != self.times - 1:
            if self.estimates[day][time + 1] != -1:
                self.inc_estimate(day, time + 1)

    def inc_estimate(self, day, time):
        self.estimates[day][time] += 1

    def reset_estimate(self, day, time):
        self.estimates[day][time] = -1

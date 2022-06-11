from mesa import Agent

class AuditoriumAgent(Agent):

    days = 12
    times = 7

    def __init__(self, id, model):
        super().__init__(id, model)

        self.define_estimates()

    def define_estimates(self):
        self.estimates = [[1.0 for j in range(self.times)] for i in range(self.days)]

    def refactor_estimates(self, day, time):
        self.reset_estimate(day, time)

    def reset_estimate(self, day, time):
        self.estimates[day][time] = -1

    def get_estimate(self, day, time):
        result = self.estimates[day][time]

        return result

from mesa import Model
from mesa.time import SimultaneousActivation

from Agents import AuditoriumAgent as AA,  DepartmentAgent as DA, \
                   GroupAgent as GA, ProfessorAgent as PA

from Sources import AuditoriumSource as AS, DepartmentSource as DS, GroupSource as GS, \
                    ProfessorSource as PS, TimetableSource as TS


class TimeTableModel(Model):

    def __init__(self):

        self.running = True
        self.schedule = SimultaneousActivation(self)

        self.extra_auditoriums = AS.AuditoriumSource.get_extras()

        for department in DS.DepartmentSource.source:
            agent = DA.DepartmentAgent(department.id, self)
            self.schedule.add(agent)
        for group in GS.GroupSource.source:
            agent = GA.GroupAgent(group.name, self)
            self.schedule.add(agent)
        for professor in PS.ProfessorSource.source:
            agent = PA.ProfessorAgent(professor.id, self)
            self.schedule.add(agent)
        for auditorium in AS.AuditoriumSource.source:
            agent = AA.AuditoriumAgent(auditorium.number, self)
            self.schedule.add(agent)

        self.departments = [d.id for d in DS.DepartmentSource.source]

    def step(self):
        self.schedule.step()

        ids = [a.unique_id for a in self.schedule.agents]
        working = [d for d in ids if d in self.departments]

        if len(working) == 0:
            self.running = False
            TS.TimetableSource.write_to_csv()

    def run_model(self):
        while self.running:
            self.step()

    def get_agent(self, id):
        result = [a for a in self.schedule.agents if a.unique_id == id][0]

        return result
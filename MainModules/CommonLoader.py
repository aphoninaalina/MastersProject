from Sources import AuditoriumSource as AS, CampusSource as CS, ClassTypeSource as CTS, DepartmentSource as DeS,\
                    DisciplineSource as DiS, GroupSource as GS, ProfessorSource as PS, TimetableSource as TS


class CommonLoader:

    def __init__(self):
        self.load_data()

    def load_data(self):
        DiS.DisciplineSource()
        PS.ProfessorSource()

        DeS.DepartmentSource()
        GS.GroupSource()

        CS.CampusSource()
        AS.AuditoriumSource()

        CTS.ClassTypeSource()
        TS.TimetableSource()
        
        self.refactor_sources()

    def refactor_sources(self):
        AS.AuditoriumSource.refactor_sources(DiS.DisciplineSource.source, DeS.DepartmentSource.source)
        GS.GroupSource.refactor_sources(DiS.DisciplineSource.source)

        GS.GroupSource.refactor_source()
        PS.ProfessorSource.refactor_source()
        DiS.DisciplineSource.refactor_source()

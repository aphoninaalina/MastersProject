class Discipline:

    def __init__(self, name, type, group, professor, department):
        self.name = name
        self.type = type
        self.group = group
        self.professor = professor
        self.department = department

    def __eq__(self, other):
        if not isinstance(other, Discipline):
            return NotImplemented

        return (self.name, self.type, self.group, self.professor, self.department) == \
               (other.name, other.type, other.group, other.professor, other.department)

    def __hash__(self):
        return hash((self.name, self.type, self.group, self.professor, self.department))

    def compare_groups(self, group_1, group_2):
        year_1 = group_1[:-1]
        year_2 = group_2[:-1]

        result = year_1 == year_2

        return result

    def equal_lecture(self, other):
        result = self.name == other.name and self.type == other.type and self.group != other.group and \
                 self.professor == other.professor and self.department == other.department and \
                 self.compare_groups(self.group, other.group)

        return result

    def equal_lab_practice(self, other):
        result = self.name == other.name and self.type == other.type and self.group == other.group and \
                 self.department == other.department and self.professor != other.professor

        return result

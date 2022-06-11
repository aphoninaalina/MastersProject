class Professor:

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, Professor):
            return NotImplemented

        return (self.id, self.name) == (other.id, other.name)

    def __hash__(self):
        return hash((self.id, self.name))

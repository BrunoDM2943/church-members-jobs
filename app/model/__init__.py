class Member:
    def __init__(self, id, birthDateShort, firstName, lastName):
        self.id = id
        self.birtDateShort = birthDateShort
        self.name = "{} {}".format(firstName, lastName)

    def __repr__(self):
        return "{} - {}".format(self.name, self.birtDateShort)

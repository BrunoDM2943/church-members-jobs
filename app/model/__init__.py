class Member:
    def __init__(self, _id, birth_date_short, first_name, last_name, marriage_date_short):
        self.id = _id
        self.birth_date_short = birth_date_short
        self.marriage_date_short = marriage_date_short
        self.name = "{} {}".format(first_name, last_name)

    def __repr__(self):
        return "{} - {}".format(self.name, self.birth_date_short)

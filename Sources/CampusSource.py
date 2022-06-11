from Models import Campus as C


class CampusSource:

    source = []

    def __init__(self):
        self.load_data()

    def load_data(self):
        self.source += [C.Campus('Главный кампус', ['1', '2', '3', '4', '5', '6', '7', '8', '9']),
                        C.Campus('Кампус на Социалистической', ['21', '22', '23', '24', '25', '26']),
                        C.Campus('Страна Советов', ['10']),
                        C.Campus('Шаповалова', ['11'])]

from Models import ClassType as CT


class ClassTypeSource:

    source = []

    def __init__(self):
        self.load_data()

    def load_data(self):
        self.source += [CT.ClassType('л.', ['Аудитория', 'Групповая', 'Класс', 'Компьютерный класс', 'Поточная',
                                            'Учебная аудитория',

                                            'Лекционная аудитория']),

                        CT.ClassType('пр.', ['Аудитория', 'Групповая', 'Класс', 'Компьютерный класс', 'Поточная',
                                             'Учебная аудитория',

                                             'Лаборатория', 'Лаборатория изучения электрических цепей и электроники',
                                             'Лаборатория модульной сборки электрических и электронных схем',
                                             'Лаборатория рисунка и живописи', 'Лаборатория УПП, ОМД',
                                             'Лаборатория художественной обработки материалов',
                                             'Лаборатория ювелирного мастерства',

                                             'Мастерская для рисования', 'Мастерская лепки',

                                             'Учебная лаборатория', 'Учебная лаборатория с кладовой']),

                        CT.ClassType('лаб.', ['Аудитория', 'Групповая', 'Класс', 'Компьютерный класс', 'Поточная',
                                              'Учебная аудитория',

                                              'Лаборатория', 'Лаборатория изучения электрических цепей и электроники',
                                              'Лаборатория модульной сборки электрических и электронных схем',
                                              'Лаборатория рисунка и живописи', 'Лаборатория УПП, ОМД',
                                              'Лаборатория художественной обработки материалов',
                                              'Лаборатория ювелирного мастерства',

                                              'Мастерская для рисования', 'Мастерская лепки',

                                              'Учебная лаборатория', 'Учебная лаборатория с кладовой'])]

    def get_types(name):
        result = [c for c in ClassTypeSource.source if c.name == name][0].types

        return result

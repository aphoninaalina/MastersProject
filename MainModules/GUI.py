import glob
import os

from os import listdir
from os.path import isfile, join

from tkinter import *
from tkinter import filedialog, ttk

from Sources import GroupSource as GS, ProfessorSource as PS, TimetableSource as TS
from MainModules import AgencyModule as AM, CommonLoader as CL


class GUI:
    class TimetableWindow():

        days_ = {0: 'Понедельник', 1: 'Вторник', 2: 'Среда', 3: 'Четверг', 4: 'Пятница', 5: 'Суббота',
                6: 'Понедельник', 7: 'Вторник', 8: 'Среда', 9: 'Четверг', 10: 'Пятница', 11: 'Суббота'}
        times_ = {0: ('8:30', '10:05'), 1: ('10:15', '11:50'), 2: ('12:00', '13:35'), 3: ('14:15', '15:50'),
                 4: ('16:00', '17:35'), 5: ('17:45', '19:20'), 6: ('19:30', '21:05')}

        days = 12
        times = 7

        def __init__(self, member, member_type):
            self.window = Tk()
            self.window.title('')

            self.add_scrollbar()

            self.member = member
            self.member_type = member_type

            self.timetable = self.load_timetable()

            self.show_timetable()
            self.window.mainloop()

        def add_scrollbar(self):
            self.frame = Frame(self.window)
            self.frame.pack(fill=BOTH, expand=1)

            self.canvas = Canvas(self.frame)
            self.canvas.pack(side=LEFT, fill=BOTH, expand=1)

            self.scrollbar = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.canvas.yview)
            self.scrollbar.pack(side=RIGHT, fill=Y)

            self.canvas.configure(yscrollcommand=self.scrollbar.set)
            self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

            self.frame_ = Frame(self.canvas)

            self.canvas.create_window((0, 0), window=self.frame_, anchor='nw')

        def load_timetable(self):
            match self.member_type:
                case 'group':
                    result = [t for t in TS.TimetableSource.source if self.member in t.discipline.group.split(' ')]
                case 'professor':
                    result = [t for t in TS.TimetableSource.source if self.member in t.discipline.professor.split(' ')]
                case 'auditorium':
                    result = [t for t in TS.TimetableSource.source if self.member in t.auditorium.split(' ')]

            result.sort(key=lambda t: int(t.time))
            result.sort(key=lambda t: int(t.day))

            return result

        def show_timetable(self):
            row = 0

            current_day = -1
            current_week = ''
            for cell in self.timetable:
                week = 'Нижняя неделя' if int(cell.day) < 6 else 'Верхняя неделя'
                if week != current_week:
                    self.week_label = Label(self.frame_, text=week).grid(row=0 + row, column=0, columnspan=10)
                    row += 1
                    current_week = week
                if int(cell.day) != current_day:
                    self.day_label = Label(self.frame_, text=self.days_[int(cell.day)]).grid(row=0 + row, column=0, columnspan=10)
                    current_day = int(cell.day)

                professors = ' '.join([PS.ProfessorSource.get_professor(p).name for p in cell.discipline.professor.split(' ')])
                times = self.times_[int(cell.time)]

                start = times[0]
                stop = times[1]

                self.start_label = Label(self.frame_, text=start).grid(row=1 + row, column=0, rowspan=2, sticky=S)
                self.stop_label = Label(self.frame_, text=stop).grid(row=3 + row, column=0, rowspan=2, sticky=N)

                self.discipline_label = Label(self.frame_, text=f'{cell.discipline.type} {cell.discipline.name}').grid(row=1 + row, column=1, columnspan=9, sticky=W)
                self.group_label = Label(self.frame_, text=cell.discipline.group).grid(row=2 + row, column=1, columnspan=9, sticky=W)
                self.professor_label = Label(self.frame_, text=professors).grid(row=3 + row, column=1, columnspan=9, sticky=W)
                self.auditorium_label = Label(self.frame_, text=cell.auditorium).grid(row=4 + row, column=1, columnspan=9, sticky=W)

                row += 5

    def __init__(self):
        CL.CommonLoader()

        self.define_timetable()

        self.window = Tk()
        self.window.title('')

        self.auditoriums = []
        for cell in TS.TimetableSource.source:
            self.auditoriums += cell.auditorium.split(' ')

        self.auditoriums[:] = set(self.auditoriums)
        self.groups = [g.name for g in GS.GroupSource.source]
        self.professors = [p.name for p in PS.ProfessorSource.source]

        self.source = self.groups
        self.type = 'group'

        self.new_button = Button(self.window, text='Создать новое расписание', command=lambda: self.create_new_timetable()).grid(row=0, column=0, columnspan=3, sticky=N+S+W+E)
        self.load_button = Button(self.window, text='Загрузить расписание', command=lambda: self.load_timetable()).grid(row=1, column=0, columnspan=3, sticky=N+S+W+E)

        self.group_button = Button(self.window, text='По группам', command=lambda: self.change_source(self.groups, 'group')).grid(row=2, column=0)
        self.professor_button = Button(self.window, text='По преподавателям', command=lambda: self.change_source(self.professors, 'professor')).grid(row=2, column=1)
        self.auditorium_button = Button(self.window, text='По аудиториям', command=lambda: self.change_source(self.auditoriums, 'auditorium')).grid(row=2, column=2)

        self.config_searcher()

        self.window.mainloop()

    def change_source(self, source, type):
        if self.source != source:
            self.source = source
            self.type = type

            self.searcher.delete(0, 'end')
            self.update_source(self.source)

    def config_searcher(self):
        self.searcher = Entry(self.window)
        self.searcher.grid(row=3, column=0, columnspan=3, sticky=N+S+W+E)
        self.searcher.bind('<KeyRelease>', self.scan_key)

        self.listbox = Listbox(self.window)
        self.listbox.grid(row=4, column=0, columnspan=3, sticky=N+S+W+E)
        self.listbox.bind('<<ListboxSelect>>', self.select_member)
        self.update_source(self.source)

    def select_member(self, event):
        widget = event.widget
        index = int(widget.curselection()[0])
        value = widget.get(index)

        if self.type == 'professor':
            value = PS.ProfessorSource.get_id(value)

        self.TimetableWindow(value, self.type)

    def scan_key(self, event):
        value = event.widget.get()
        if value == '':
            source = self.source
        else:
            source = []
            for value_ in self.source:
                if value.lower() in value_.lower():
                    source.append(value_)
        self.update_source(source)

    def update_source(self, source):
        self.listbox.delete(0, 'end')
        for value in source:
            self.listbox.insert('end', value)

    def create_new_timetable(self):
        TS.TimetableSource.source[:] = []
        model = AM.TimeTableModel()
        model.run_model()

    def load_timetable(self):
        file = filedialog.askopenfilename(title='Open a timetable', initialdir='Timetables/')
        TS.TimetableSource.load_source(file)

    def define_timetable(self):
        path = 'Timetables/'
        files = [f for f in listdir(path) if isfile(join(path, f))]

        if len(files) != 0:
            file = max(glob.glob(f'{path}*'), key=os.path.getctime).replace(f'{path[:-1]}\\', '')
            TS.TimetableSource.load_source(path + file)
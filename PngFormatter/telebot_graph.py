import matplotlib.pyplot as plt
from enum import Enum

class FinalsType(Enum):
    EXAM = 0
    CREDIT = 1
    PROJECT = 2

    @staticmethod
    def to_string(ftype):
        match ftype:
            case FinalsType.EXAM:
                return "exam"
            case FinalsType.CREDIT:
                return "credit"
            case FinalsType.PROJECT:
                return "project"

class Discipline:
    def __init__(self, name, grades_wl, sgrade, ftype: FinalsType = FinalsType.EXAM, exgrade=0):
        self.name=name
        self.grades_week_list=grades_wl
        self.sum_grade=sgrade
        self.exam_grade=exgrade
        self.finals = ftype

    def change_week_grades(self, new_grades):
        self.grades_week_list = new_grades

    def make_pie_chart(self):
        plt.figure(num=1, figsize=(6, 6))

        size=[self.sum_grade, 100-self.sum_grade-self.exam_grade, self.exam_grade]
        colors = ['#ff9999', '#66b3ff', '#99ff99']

        plt.pie(size, labels=["practice", "",  FinalsType.to_string(self.finals)], colors=colors,autopct='%1.1f',  startangle=90 )

        plt.text(0, -1.1, f'Total: {self.sum_grade+self.exam_grade} / 100', ha='center', va='center', fontsize=12, color='black',fontweight='bold')
        plt.title(self.name, fontsize=14)
        plt.axis('equal')# співвідношення сторін осей (1=рівне)

        plt.savefig(self.name+"_piechart.png")
        plt.show()


class DisciplinesList:
    def __init__(self, *disciplines):
        self.disciplines_list = list(disciplines)

    def add(self, discip):
        self.disciplines_list.append(discip)

    def remove(self, discip):
        self.disciplines_list.remove(discip)

    def make_week_graph(self):
        plt.close()
        plt.figure(figsize=(10, 6))

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        colormap = plt.get_cmap('viridis', len(self.disciplines_list))
        colours = [colormap(i) for i in range(len(self.disciplines_list))]

        for discip, c in zip(self.disciplines_list, colours):
            if len(discip.grades_week_list) != len(days):
                raise ValueError(f"{discip.name} should have {len(days)} grades for each day of the week.")
            plt.plot(days, discip.grades_week_list, color=c, label=discip.name)


        font1={'family':'serif','color':'darkred','size':15}
        font2={'family':'serif','color':'darkred','size':20}
        plt.title("Grades over the week", fontdict = font2)
        plt.ylabel("Grades", fontdict = font1)
        plt.xlabel("Days of the week", fontdict = font1)

        plt.legend()
        plt.ylim(0, 100)

        plt.savefig('output.png')
        plt.show()


d1=Discipline("Discrete mathematics", [2, 32, 53, 6, 7, 63, 3], 47, FinalsType.CREDIT, 30)
d2=Discipline("mathematical analysis", [4, 6, 42, 4, 4, 85, 9], 33 , FinalsType.EXAM, 26)
d3=Discipline("English", [46, 16,12, 14, 24,54, 29],30, FinalsType.CREDIT, 14)

DisList=DisciplinesList(d1, d2, d3)
DisList.make_week_graph()

d1.make_pie_chart()
d2.make_pie_chart()
d3.make_pie_chart()

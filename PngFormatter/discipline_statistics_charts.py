import matplotlib.pyplot as plt
import os
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

class ChartMaker:
    def __init__(self, output_directory="disciplines_graphs"):
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def make_pie_chart(self, discipline: Discipline):
        plt.close()
        plt.figure(num=1, figsize=(6, 6))

        size = [discipline.sum_grade, 100 - discipline.sum_grade - discipline.exam_grade, discipline.exam_grade]
        colors = ['#ff9999', '#66b3ff', '#99ff99']

        plt.pie(size, labels=["practice", "", FinalsType.to_string(discipline.finals)], colors=colors, autopct='%1.1f',
                startangle=90)

        plt.text(0, -1.1, f'Total: {discipline.sum_grade + discipline.exam_grade} / 100', ha='center', va='center', fontsize=12,
                 color='black', fontweight='bold')
        plt.title(discipline.name, fontsize=14)
        plt.axis('equal')  # співвідношення сторін осей (1=рівне)
        output_directory = "disciplines_graphs"
        plt.savefig(os.path.join(output_directory, discipline.name + "_piechart.png"))


    def make_week_graph(self, desciplinelist: list):
        plt.close()
        plt.figure(figsize=(10, 6))

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        colormap = plt.get_cmap('viridis', len(desciplinelist))
        colours = [colormap(i) for i in range(len(desciplinelist))]

        for discip, c in zip(desciplinelist, colours):
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
        output_directory="disciplines_graphs"
        plt.savefig(os.path.join(output_directory, 'weekly_discipline_overview.png'))


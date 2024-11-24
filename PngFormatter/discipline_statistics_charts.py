import matplotlib.pyplot as plt
import os
from enum import Enum
from datetime import datetime, timedelta


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
class Grade:
    def __init__(self, grade, time):
        self.grade=grade
        self.time_added=time

class Discipline:
    def __init__(self, name, grades_list, sumgrade, ftype: FinalsType = FinalsType.EXAM, exgrade=0):
        self.name=name
        self.grades_list=grades_list
        self.sum_grade=sumgrade
        self.exam_grade=exgrade
        self.finals = ftype

    def change_week_grades(self, new_grades):
        self.grades_list = new_grades

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

    def make_week_graph(self, discipline, start_date, end_date):
        plt.close()
        plt.figure(figsize=(10, 6))

        date_labels = [date.time_added for date in discipline.grades_list]
        grades_list = [date.grade for date in discipline.grades_list]

        if len(discipline.grades_list) > 0:
            plt.plot(date_labels, grades_list, color='blue', label=discipline.name)

        plt.title(f"Progress of {discipline.name} from {start_date.date()} to {end_date.date()}")
        plt.xlabel("Dates (with time)")
        plt.ylabel("Grades")
        plt.xticks(rotation=45)  # Поворот дат на осі X
        plt.legend()
        plt.tight_layout()

        output_directory = f"{self.output_directory}/grades_comparison_{discipline.name}_{start_date.date()}_to_{end_date.date()}.png"
        plt.savefig(output_directory)

        return output_directory

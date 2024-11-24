import matplotlib.pyplot as plt
import matplotlib
import os
from enum import Enum
from datetime import datetime, timedelta
matplotlib.use('agg')


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
    def __init__(self, discipline):
        self.discipline=discipline
        self.name=discipline["discipline"]
        self.practice_grades_list=discipline["points"]["practice"]
        self.lecture_grades_list=discipline["points"]["lecture"]
        self.sum_practice_grade=sum([grade["value"] for grade in self.practice_grades_list])
        self.sum_lecture_grade=sum([grade["value"] for grade in self.lecture_grades_list])
        self.finals = FinalsType.EXAM

    def change_week_grades(self, new_grades):
        self.grades_list = new_grades

class ChartMaker:
    def __init__(self, output_directory="disciplines_graphs"):
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def make_pie_chart(self, discipline: Discipline):
        plt.close()
        plt.figure(num=1, figsize=(6, 6))

        left = 100 - discipline.sum_practice_grade - discipline.sum_lecture_grade
        size = [discipline.sum_practice_grade, discipline.sum_lecture_grade, left]
        colors = ['#ff9999', '#99ff99', '#66b3ff']

        plt.pie(size, labels=["practice", FinalsType.to_string(discipline.finals), "left"], colors=colors, autopct='%1.1f',
                startangle=90)

        plt.text(0, -1.3, f'Total: {discipline.sum_lecture_grade + discipline.sum_practice_grade} / 100', ha='center', va='center', fontsize=12,
                 color='black', fontweight='bold')

        plt.title(discipline.name, fontsize=14, pad=20)
        plt.axis('equal')  # співвідношення сторін осей (1=рівне)
        output_directory = "disciplines_graphs"

        timestamp = datetime.now()

        plt.savefig(os.path.join(output_directory, f"{discipline.name}_{timestamp}_piechart.png"))

        return f"{output_directory}/{discipline.name}_{timestamp}_piechart.png"

    def make_n_days_chart(self, discipline: Discipline, start_date: datetime, end_date: datetime):
        plt.close()
        plt.figure(figsize=(10, 6))

        lecture_grades = [grade["value"] for grade in discipline.lecture_grades_list]
        practice_grades = [grade["value"] for grade in discipline.practice_grades_list]
        lecture_dates = [grade["time"] for grade in discipline.lecture_grades_list]
        practice_dates = [grade["time"] for grade in discipline.practice_grades_list]

        plt.plot(lecture_dates, lecture_grades, label="Lecture", color='red')
        plt.plot(practice_dates, practice_grades, label="Practice", color='blue')
        plt.plot(lecture_dates, lecture_grades, marker='o', color='red')
        plt.plot(practice_dates, practice_grades, marker='o', color='blue')

        plt.title(f"Progress of {discipline.name} from {start_date.date()} to {end_date.date()}")
        plt.xlabel("Dates (with time)")
        plt.ylabel("Grades")
        plt.xticks(rotation=45)  # Поворот дат на осі X
        plt.legend()
        plt.tight_layout()

        output_directory = f"{self.output_directory}/grades_comparison_{discipline.name}_{start_date.date()}_to_{end_date.date()}_{datetime.now()}.png"

        plt.savefig(output_directory)

        return output_directory

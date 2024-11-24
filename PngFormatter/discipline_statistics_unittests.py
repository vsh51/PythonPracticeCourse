import matplotlib
matplotlib.use('Agg')
import unittest
import matplotlib.pyplot as plt
from discipline_statistics_charts import Discipline, ChartMaker, FinalsType


class TestWeekGraph(unittest.TestCase):

    def test_discipline(self):
        d1 = Discipline("name", [1, 2, 3, 4, 5, 6, 7], 80, FinalsType.EXAM, 10)
        self.assertEqual(d1.name, "name")  # add assertion here
        self.assertEqual(d1.grades_list, [1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(d1.sum_grade, 80)
        self.assertEqual(d1.finals, FinalsType.EXAM)
        self.assertEqual(d1.exam_grade, 10)

        d1.change_week_grades([4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(d1.grades_list, [4, 5, 6, 7, 8, 9, 10])

    def test_make_week_graph(self):
        d1 = Discipline("name1", [1, 2, 3, 4, 5, 6, 7], 70, FinalsType.EXAM, 20)
        d2 = Discipline("name2", [5, 6, 7, 4, 5, 6, 7], 80, FinalsType.CREDIT, 10)
        d3 = Discipline("name3", [1, 9, 3, 4, 5, 6, 7], 85, FinalsType.PROJECT, 5)
        disciplines_list = [d1, d2, d3]

        chart_maker = ChartMaker()
        chart_maker.make_week_graph(disciplines_list)

        self.assertEqual(len(plt.get_fignums()), 1)

        axes = plt.gca()
        self.assertEqual(axes.get_title(), "Grades over the week")
        self.assertEqual(axes.get_ylabel(), "Grades")
        self.assertEqual(axes.get_xlabel(), "Days of the week")
        self.assertEqual(axes.get_ylim(), (0, 100))
        self.assertEqual(len(axes.get_lines()), 3)

    def test_make_week_graph_raises(self):
        d1 = Discipline("name1", [1, 2, 3, 4, 5, 6], 70, FinalsType.EXAM, 20)  # 6 days instead of 7
        d2 = Discipline("name2", [], 80, FinalsType.CREDIT, 10)  # empty grades list
        d3 = Discipline("name3", [1, 9, 3, 4, 5, 6, 7, 8, 9], 85, FinalsType.PROJECT, 5)  # 9 days instead of 7
        disciplines_list = [d1, d2, d3]

        chart_maker = ChartMaker()

        for discip in disciplines_list:
            with self.assertRaises(ValueError) as context:
                chart_maker.make_week_graph([discip])

            expected_message = f"{discip.name} should have 7 grades for each day of the week."
            self.assertEqual(str(context.exception), expected_message)

if __name__ == '__main__':
    unittest.main()

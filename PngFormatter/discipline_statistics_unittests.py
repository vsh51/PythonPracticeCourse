import matplotlib
matplotlib.use('Agg')
import unittest
import matplotlib.pyplot as plt
from discipline_statistics_charts import Discipline, DisciplinesList


class TestWeekGraph(unittest.TestCase):

    def test_discipline(self):
        d1=Discipline("name", [1, 2, 3])
        self.assertEqual(d1.name, "name")  # add assertion here
        self.assertEqual(d1.grades_list, [1, 2, 3])

        d1.change_grades([4, 5, 6])
        self.assertEqual(d1.grades_list, [4, 5, 6])

    def test_discipline_list_init(self):
        d1 = Discipline("name1", [1, 2, 3])
        d2 = Discipline("name2", [5, 6, 7])
        d3 = Discipline("name3", [1, 9, 3])
        dl=DisciplinesList(d1, d2, d3)

        self.assertEqual(len(dl.disciplines_list), 3)
        self.assertEqual(dl.disciplines_list[0].name, "name1")
        self.assertEqual(dl.disciplines_list[1].name, "name2")
        self.assertEqual(dl.disciplines_list[2].name, "name3")

        self.assertEqual(dl.disciplines_list[0].grades_list, [1, 2, 3])
        self.assertEqual(dl.disciplines_list[1].grades_list, [5, 6, 7])
        self.assertEqual(dl.disciplines_list[2].grades_list, [1, 9, 3])

    def test_discipline_list_add(self):
        d1 = Discipline("name1", [1, 2, 3])
        d2 = Discipline("name2", [5, 6, 7])
        dl = DisciplinesList(d1, d2)
        self.assertEqual(len(dl.disciplines_list), 2)

        d3 = Discipline("name3", [1, 9, 3])
        dl.add(d3)
        self.assertEqual(len(dl.disciplines_list), 3)

    def test_discipline_list_remove(self):
        d1 = Discipline("name1", [1, 2, 3])
        d2 = Discipline("name2", [5, 6, 7])
        d3 = Discipline("name3", [1, 9, 3])
        dl = DisciplinesList(d1, d2, d3)
        self.assertEqual(len(dl.disciplines_list), 3)

        self.assertEqual(dl.disciplines_list[0].name, "name1")
        self.assertEqual(dl.disciplines_list[1].name, "name2")
        self.assertEqual(dl.disciplines_list[2].name, "name3")

        dl.remove(d2)
        self.assertEqual(len(dl.disciplines_list), 2)

        self.assertEqual(dl.disciplines_list[0].name, "name1")
        self.assertEqual(dl.disciplines_list[1].name, "name3")

    def test_make_week_graph(self):
        d1 = Discipline("name1", [1, 2, 3, 4, 5, 6, 7])
        d2 = Discipline("name2", [5, 6, 7, 4, 5, 6, 7])
        d3 = Discipline("name3", [1, 9, 3, 4, 5, 6, 7])
        dl = DisciplinesList(d1, d2, d3)

        dl.make_week_graph()
        self.assertEqual(len(plt.get_fignums()), 1)

        axes = plt.gca()
        self.assertEqual(axes.get_title(), "Grades over the week")
        self.assertEqual(axes.get_ylabel(), "Grades")
        self.assertEqual(axes.get_xlabel(), "Days of the week")
        self.assertEqual(axes.get_ylim(), (0, 100))
        self.assertEqual(len(axes.get_lines()), 3)

    def test_make_week_graph_raises(self):
        d1 = Discipline("name1", [1, 2, 3])
        d2 = Discipline("name2", [])
        d3 = Discipline("name3", [1, 9, 3, 7, 3, 6, 2, 5, 7])
        dl = DisciplinesList(d1, d2, d3)

        for discip in [d1, d2, d3]:
            with self.assertRaises(ValueError) as context:
                dl = DisciplinesList(discip)
                dl.make_week_graph()

            expected_message = f"{discip.name} should have 7 grades for each day of the week."
            self.assertEqual(str(context.exception), expected_message)

if __name__ == '__main__':
    unittest.main()

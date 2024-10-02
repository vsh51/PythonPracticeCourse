import matplotlib.pyplot as plt

class Discipline:
    def __init__(self, name, gradesl):
        self.name=name
        self.grades_list=gradesl

    def change_grades(self, new_grades):
        self.grades_list = new_grades

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
            if len(discip.grades_list) != len(days):
                raise ValueError(f"{discip.name} should have {len(days)} grades for each day of the week.")
            plt.plot(days, discip.grades_list, color=c, label=discip.name)


        font1={'family':'serif','color':'darkred','size':15}
        font2={'family':'serif','color':'darkred','size':20}
        plt.title("Grades over the week", fontdict = font2)
        plt.ylabel("Grades", fontdict = font1)
        plt.xlabel("Days of the week", fontdict = font1)

        plt.legend()
        plt.ylim(0, 100)

        plt.savefig('output.png')
        plt.show()


if __name__=="__main__":
    d1=Discipline("Discrete mathematics", [2, 32, 53, 6, 7, 63, 3])
    d2=Discipline("mathematical analysis", [4, 6, 42, 4, 4, 85, 9] )
    d3=Discipline("English", [46, 16,12, 14, 24,54, 29])

    DisList=DisciplinesList(d1, d2, d3)
    DisList.make_week_graph()

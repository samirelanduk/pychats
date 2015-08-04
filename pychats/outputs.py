import matplotlib.pyplot as plt

class Chart:

    def show(self):
        fig = self._generate()
        fig.show()

    def save(self, path):
        fig = self._generate()
        fig.savefig(path)


class BarChart(Chart):

    def __init__(self, x_data, y_data, color="#0000FF", edgecolor="#000000", width=0.75, xlabel="X-axis", xticks=[], xticklabels=[], ylabel="Y-axis", title="A bar chart"):
        Chart.__init__(self)
        self.x_data = x_data
        self.y_data = y_data
        self.color = color
        self.edgecolor = edgecolor
        self.width = width
        self.xlabel = xlabel
        self.xticks = xticks
        self.xticklabels = xticklabels
        self.ylabel = ylabel
        self.title = title

    def _generate(self):
        fig, ax = plt.subplots()
        ax.bar(self.x_data, self.y_data, color=self.color, edgecolor=self.edgecolor, width=self.width)
        ax.set_xlabel(self.xlabel)
        ax.set_xticks(self.xticks)
        ax.set_xticklabels(self.xticklabels)
        ax.set_ylabel(self.ylabel)
        ax.set_title(self.title)
        ax.grid(b=True, which='major', color='k', linestyle='--')
        return fig


class LineChart(Chart):

    def __init__(self, x_data, y_data):
        pass

    def _generate(self):
        pass

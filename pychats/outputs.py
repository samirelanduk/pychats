import matplotlib.pyplot as plt
import os
import datetime
import collections
#This has some serious issues regarding code-reuse - there HAS to be a more elegant way, especially for the figure. It will do for now though

class Chart:
    """A generic chart object - requires a _generate method to actually produce a matplotlib chart"""

    def show(self):
        """Produce a matplotlib chart on screen"""
        fig = self._generate()
        fig.show()

    def save(self, path):
        """Save to file"""
        fig = self._generate()
        fig.savefig(path)

    def to_svg(self):
        """Return the xml of a svg chart"""
        #Need a better way to do this
        self.save("svg.svg")
        f = open("svg.svg", "r")
        svg = f.read()
        f.close()
        os.remove("svg.svg")
        return svg



class BarChart(Chart):
    """A bar chart"""

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
    """A line chart"""

    def __init__(self, x_data, y_data, color="#0000FF", linewidth=1, xlabel="X-axis", xticks=[], xticklabels=[], ylabel="Y-axis", title="A line chart"):
        Chart.__init__(self)
        self.x_data = x_data
        self.y_data = y_data
        self.color = color
        self.linewidth = linewidth
        self.xlabel = xlabel
        self.xticks = xticks
        self.xticklabels = xticklabels
        self.ylabel = ylabel
        self.title = title


    def _generate(self):
        fig, ax = plt.subplots()
        ax.plot(self.x_data, self.y_data, color=self.color, linewidth=self.linewidth)
        ax.set_xlabel(self.xlabel)
        ax.set_xticks(self.xticks)
        ax.set_xticklabels(self.xticklabels)
        ax.set_ylabel(self.ylabel)
        ax.set_title(self.title)
        ax.grid(b=True, which='major', color='k', linestyle='--')
        return fig


class MultiLineChart(Chart):
    """A chart with multiple line"""

    def __init__(self, line_charts, colors=None, labels=["No value"], linewidth=1, xlabel="X-axis", ylabel="Y-axis", title="A MultiLineChart"):
        #Determine x-axis range
        x_min = min([min(chart.x_data) for chart in line_charts])
        x_max = max([max(chart.x_data) for chart in line_charts])
        self.x_data = [x_min]
        while self.x_data[-1] != x_max:
            if isinstance(x_min, datetime.date) or isinstance(x_min, datetime.datetime):
                self.x_data.append(self.x_data[-1] + datetime.timedelta(days=1))
            else:
                self.x_data.append(self.x_data[-1] + 1)

        #Determine x-axis ticks (also determines xticklabels but not... very well)
        self.xticks = []
        self.xticklabels = []
        for chart in line_charts:
            self.xticks += chart.xticks
            self.xticklabels += chart.xticklabels
        self.xticks = list(set(self.xticks))
        self.xticklabels = sorted(list(set(self.xticklabels)))

        #Determine y-axis ranges
        self.y_datas = []
        for chart in line_charts:
            #Extend before range
            if isinstance(x_min, datetime.datetime) or isinstance(x_min, datetime.date):
                left_padding = [0] * (chart.x_data[0] - self.x_data[0]).days
                right_padding = [None] * (self.x_data[-1] - chart.x_data[-1]).days
            else:
                left_padding = [0] * (chart.x_data[0] - self.x_data[0])
                right_padding = [None] * (self.x_data[-1] - chart.x_data[-1])
            self.y_datas.append(left_padding + chart.y_data + right_padding)

        #Determine colors for each line
        if isinstance(colors, collections.Sequence):
            colors = colors[:]
            #Do the colors match the number of charts?
            if len(colors) == len(line_charts):
                pass
            elif len(colors) < len(line_charts):
                while len(colors) != len(line_charts):
                    colors.append(colors[-1])
            else:
                while len(colors) != len(line_charts):
                    colors = colors[:-1]
            self.colors = colors
        else:
            self.colors = None

        #Determine labels for each line
        labels = labels[:]
        if len(labels) == len(line_charts):
            pass
        elif len(labels) < len(line_charts):
            while len(labels) != len(line_charts):
                labels.append("No value")
        else:
            while len(labels) != len(line_charts):
                labels = labels[:-1]
        self.labels = labels

        #Other arguments
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.linewidth = linewidth
        self.title = title


    def _generate(self):
        fig, ax = plt.subplots()
        for line in self.y_datas:
            if self.colors == None:
                ax.plot(self.x_data, line, linewidth=self.linewidth, label=self.labels[self.y_datas.index(line)])
            else:
                ax.plot(self.x_data, line, color=self.colors[self.y_datas.index(line)], linewidth=self.linewidth, label=self.labels[self.y_datas.index(line)])
        ax.set_xlabel(self.xlabel)
        ax.set_xticks(self.xticks)
        ax.set_xticklabels(self.xticklabels)
        ax.set_ylabel(self.ylabel)
        ax.set_title(self.title)
        ax.grid(b=True, which='major', color='k', linestyle='--')
        ax.legend()
        return fig




class PieChart(Chart):
    """A pie chart"""

    def __init__(self, pie_data, pie_labels):
        Chart.__init__(self)
        self.pie_data = pie_data
        self.pie_labels = pie_labels

    def _generate(self):
        fig, ax = plt.subplots()
        ax.pie(self.pie_data, labels=self.pie_labels)
        ax.axis("equal")
        return fig


class Figure(Chart):
    """A figure with multiple charts"""

    def __init__(self, rows, columns, charts):
        Chart.__init__(self)
        self.rows = rows
        self.columns = columns
        self.charts = charts

    def _generate(self):
        fig = plt.figure()

        chart_no = 1
        for chart in self.charts:
            plt.subplot(self.rows, self.columns, chart_no)
            if isinstance(chart, BarChart):
                plt.bar(chart.x_data, chart.y_data, color=chart.color, edgecolor=chart.edgecolor, width=chart.width)
            elif isinstance(chart, LineChart):
                plt.plot(chart.x_data, chart.y_data, color=chart.color, linewidth=chart.linewidth)
            elif isinstance(chart, PieChart):
                plt.pie(chart.pie_data, labels=chart.pie_labels)
                plt.axis("equal")
            if isinstance(chart, BarChart) or isinstance(chart, LineChart):
                plt.xlabel(chart.xlabel)
                plt.xticks(chart.xticks, chart.xticklabels)
                plt.ylabel(chart.ylabel)
                plt.title(chart.title)
                plt.grid(b=True, which='major', color='k', linestyle='--')
            chart_no += 1
        return fig

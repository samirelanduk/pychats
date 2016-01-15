import sys
sys.path.append("/Users/sam/Dropbox/PROJECTS/quickplots")
sys.path.append("/home/sam/Dropbox/PROJECTS/quickplots")
import quickplots
import datetime

class ChartGeneratingContact:

    def __getattr__(self, attribute):

        if attribute == "days":
            self.days = [min([m.datetime for m in self.messages]).date()]
            while self.days[-1] < self.log.end_date.date():
                self.days.append(self.days[-1] + datetime.timedelta(days=1))
            return self.days

        elif attribute == "_day_ticks":
            if self.days[-1] - self.days[0] > datetime.timedelta(days=365):
                self._day_ticks = [d for d in self.days if d.month == 1 and d.day == 1]
            else:
                self._day_ticks = [d for d in self.days if d.day == 1]
            return self._day_ticks

        elif attribute == "_day_tick_labels":
            self._day_tick_labels = [
             datetime.datetime.strftime(d, "01/%m/%y") for d in self._day_ticks]
            return self._day_tick_labels

        elif attribute == "days_chart":
            series = [(d, sum([m.score for m in self.messages if m.datetime.date() == d]))
             for d in self.days]
            self.days_chart = quickplots.BarChart(
             series,
             series_name=self.name,
             title=self.name + " (characters per day)",
             x_ticks=self._day_ticks,
             x_tick_labels=self._day_tick_labels,
             x_label="Date",
             y_label="Characters",
             edge_width=0,
             color=quickplots.COLORS[0]
            )
            return self.days_chart

        elif attribute == "days_average":
            chart = self.days_chart.generate_moving_average(n=30, use_start=True)
            chart.series = [(chart.series[0][0].dt - datetime.timedelta(days=1), 0)] + chart.series
            chart.color = quickplots.COLORS[0]
            chart.x_ticks = list(zip(self._day_ticks, self._day_tick_labels))
            chart.title = "Moving average"
            self.days_average = chart
            return self.days_average

        elif attribute == "months":
            self.months = [get_month(min([m.datetime for m in self.messages]).date())]
            while self.months[-1] < get_month(self.log.end_date.date()):
                self.months.append(increment_month(self.months[-1]))
            return self.months

        elif attribute == "_month_tick_labels":
            self._month_tick_labels = [
             datetime.datetime.strftime(m, "%b ''%y") for m in self._day_ticks]
            return self._month_tick_labels

        elif attribute == "months_chart":
            series = [(d, sum([m.score for m in self.messages
             if get_month(m.datetime.date()) == get_month(d)]))
              for d in self.months]
            self.months_chart = quickplots.BarChart(
             series,
             series_name=self.name,
             title=self.name + " (characters per month)",
             x_ticks=self._day_ticks,
             x_tick_labels=self._month_tick_labels,
             x_label="Date",
             y_label="Characters",
             bar_width=2628333,
             color=quickplots.COLORS[0]
            )
            return self.months_chart

        elif attribute == "months_average":
            chart = self.months_chart.generate_moving_average(n=3, use_start=True)
            chart.series = [(chart.series[0][0].dt - datetime.timedelta(days=1), 0)] + chart.series
            chart.color = quickplots.COLORS[0]
            chart.x_ticks = list(zip(self._day_ticks, self._month_tick_labels))
            chart.title = "Moving average"
            self.months_average = chart
            return self.months_average
        else:
            raise AttributeError("No attribute %s" % attribute)



class ChartGeneratingLog:

    def get_multi_chart(self, *contacts):

        charts = [c.days_average for c in contacts]
        x_ticks = []
        for index, chart in enumerate(charts):
            try:
                chart.color = quickplots.COLORS[index]
            except IndexError:
                chart.color = quickplots.generate_random_color()
            x_ticks += chart.x_ticks

        return quickplots.MultiSeriesAxisChart(charts,
         x_ticks=list(set([(t.value.value, t.label) for t in x_ticks])),
         legend=True)



def get_month(dt):
    return datetime.datetime(dt.year, dt.month, 1).date()


def increment_month(dt):
    year = dt.year + 1 if dt.month == 12 else dt.year
    month = 1 if dt.month == 12 else dt.month + 1
    day = dt.day
    return datetime.date(year, month, day)

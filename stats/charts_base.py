import pygal
from stats.names import CLANS, COLORS
from datetime import datetime, timedelta
from pygal.style import LightSolarizedStyle


class L5RStyle(LightSolarizedStyle):
    
    colors = [COLORS[index] for index in range(7)] + ['rgb(0, 0, 0)']


class BaseBar(object):
    """
    Represents the average winrates.
    :param days: number of days the average is made out of
    """
    def __init__(self, days):
        self.chart = pygal.HorizontalBar(show_legend=False, height=350, style=L5RStyle)
        self.days = days

    def get_data(self):
        """Abstract"""
        raise Exception("Not implemented")

    def generate(self):
        # Get chart data
        chart_data = self.get_data()

        # Add data to chart
        for index, v in enumerate(chart_data):
            self.chart.add(CLANS[index], v)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)


class BasePie(object):
    """
    Represents the average winrates.
    :param days: number of days the average is made out of
    """
    def __init__(self, days):
        self.chart = pygal.Pie(show_legend=False, height=521, style=L5RStyle)
        self.days = days

    def get_data(self):
        """Abstract"""
        raise Exception("Not implemented")

    def generate(self):
        # Get chart data
        chart_data = self.get_data()

        # Add data to chart
        for index, v in enumerate(chart_data):
            self.chart.add(CLANS[index], v)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)


class BaseDot(object):
    """
    Represents the average winrates.
    :param days: number of days the average is made out of
    """
    def __init__(self, days):
        self.chart = pygal.Dot(height=350, style=L5RStyle)
        self.days = days

    def get_data(self):
        """Abstract"""
        raise Exception("Not implemented")

    def generate(self):
        # Get chart data
        chart_data = self.get_data()
        self.chart.x_labels = ["vs " + CLANS[index] for index in range(7)]

        # Add data to chart
        for index, v in enumerate(chart_data):
            self.chart.add(CLANS[index], v)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)


class BaseTime(object):
    """
    Represents the average winrates during time.
    :param interval: days to average on
    :param interval_nb: number of intervals
    """
    def __init__(self, interval, interval_nb=10):
        self.interval = interval
        self.interval_nb = interval_nb

    def get_data(self):
        """Abstract"""
        raise Exception("Not implemented")

    def generate(self):
        chart_data = self.get_data()
        day_list = [datetime.now() - timedelta(days=self.interval * t) for t in range(self.interval_nb)][::-1]
        labels = [str(day.month) + "/" + str(day.day) for day in day_list]
        chart = pygal.Line(style=L5RStyle, height=350)
        chart.x_labels = labels
        for index, serie in enumerate(chart_data):
            chart.add(CLANS[index], serie[::-1])
        return chart.render(is_unicode=True)


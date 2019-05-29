import pygal
from stats.names import CLANS, COLORS, STRONGHOLDS, STRONGHOLDS_OWNERS, REV_CLANS
from datetime import datetime, timedelta
from pygal.style import LightSolarizedStyle
from copy import deepcopy


class L5RStyle(LightSolarizedStyle):
    
    colors = [COLORS[index] for index in range(7)] + ['rgb(0, 0, 0)']


class BaseBar(object):
    """
    Represents the average winrates.
    :param days: number of days the average is made out of
    """
    def __init__(self, manager, **kwargs):
        self.params = kwargs
        if self.params.get('horizontal', False) == True:
            self.chart = pygal.HorizontalBar(show_legend=False, height=350, style=L5RStyle)
        else:
            self.chart = pygal.Bar(height=350, style=L5RStyle)
        self.manager = manager

    def get_data(self):
        """Abstract"""
        raise Exception("Not implemented")

    def generate(self):
        # Get chart data
        chart_data = self.get_data(top=self.params.get('top'), filt3r=self.params.get('filt3r'))

        # Add data to chart
        for index, v in enumerate(chart_data):
            self.chart.add(CLANS[index], v)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)

    def generate_clan(self, clan):
        # Get chart data
        chart_data = self.get_data(clan, top=self.params.get('top'), filt3r=self.params.get('filt3r'))

        # Add data to chart
        for index, v in enumerate(chart_data):
            self.chart.add(CLANS[index], v)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)

    def generate_stronghold(self, clan):
        chart_data = self.get_data(clan)
        self.chart.config.style.colors = [COLORS[REV_CLANS[clan]]] * 8
        
        starting_index = STRONGHOLDS_OWNERS.index(clan)
        for index, v in enumerate(chart_data):
            self.chart.add(STRONGHOLDS[starting_index + index], v)

        # Return the rendered SVG
        rendered = self.chart.render(is_unicode=True)
        self.chart.config.style.colors = [COLORS[index] for index in range(7)] + ['rgb(0, 0, 0)']
        return rendered

class BasePie(object):
    """
    Represents the average winrates.
    :param days: number of days the average is made out of
    """
    def __init__(self, manager):
        self.chart = pygal.Pie(show_legend=False, height=521, style=L5RStyle)
        self.manager = manager

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

    def generate_stronghold(self, clan):
        chart_data = self.get_data(clan)
        self.chart.config.style.colors = [COLORS[REV_CLANS[clan]]] * 8
        
        starting_index = STRONGHOLDS_OWNERS.index(clan)
        for index, v in enumerate(chart_data):
            self.chart.add(STRONGHOLDS[starting_index + index], v)

        # Return the rendered SVG
        rendered = self.chart.render(is_unicode=True)
        self.chart.config.style.colors = [COLORS[index] for index in range(7)] + ['rgb(0, 0, 0)']
        return rendered


class BaseDot(object):
    """
    Represents the average winrates.
    :param days: number of days the average is made out of
    """
    def __init__(self, manager):
        self.chart = pygal.Dot(height=350, style=L5RStyle)
        self.manager = manager

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
    def __init__(self, managers, **kwargs):
        self.managers = managers  # the first one is the latest
        self.params = kwargs

    def get_data(self):
        """Abstract"""
        raise Exception("Not implemented")

    def generate(self):
        chart_data = self.get_data(self.params)
        day_list = [datetime.now() - timedelta(days=self.managers[0].days * t) for t in range(len(self.managers))][::-1]
        labels = [str(day.month) + "/" + str(day.day) for day in day_list]
        chart = pygal.Line(style=L5RStyle, height=350)
        chart.x_labels = labels
        for index, serie in enumerate(chart_data):
            chart.add(CLANS[index], serie[::-1])
        return chart.render(is_unicode=True)

    def generate_clan(self, clan):
        chart_data = self.get_data(clan, self.params)
        day_list = [datetime.now() - timedelta(days=self.managers[0].days * t) for t in range(len(self.managers))][::-1]
        labels = [str(day.month) + "/" + str(day.day) for day in day_list]
        chart = pygal.Line(style=L5RStyle, height=350)
        chart.x_labels = labels
        for index, serie in enumerate(chart_data):
            chart.add(CLANS[index], serie[::-1])
        return chart.render(is_unicode=True)


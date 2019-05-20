import pygal
from stats.main import TierList
from stats.names import CLANS, COLORS
from datetime import datetime, timedelta
from pygal.style import LightSolarizedStyle


class L5RStyle(LightSolarizedStyle):
    
    colors = [COLORS[index] for index in range(7)] + ['rgb(0, 0, 0)']


class WinRateChart(object):
    """
    Represents the average winrates.
    :param days: number of days the average is made out of
    """
    def __init__(self, days):
        self.chart = pygal.HorizontalBar(show_legend=False, height=350, style=L5RStyle)
        self.tier = TierList(start_date=datetime.now() - timedelta(days=days))

    def get_data(self):
        winrate_list = self.tier.get_clan_tier()
        data = []
        for index, value in enumerate(winrate_list):
            if value is None:
                data.append(50.0)
            else:
                data.append(int(10000 * value) / 100)
        return data

    def generate(self):
        # Get chart data
        chart_data = self.get_data()

        # Add data to chart
        for index, v in enumerate(chart_data):
            self.chart.add(CLANS[index], v)

        # Return the rendered SVG
        return self.chart.render(is_unicode=True)

class WinRatePlot(object):
    """
    Represents the average winrates during time.
    :param interval: days to average on
    :param interval_nb: number of intervals
    """
    def __init__(self, interval, interval_nb=10):
        self.interval = interval
        self.interval_nb = interval_nb

    def get_data(self):
        now = datetime.now()
        # Cotains 7 lists (one for each clan) with the temporal evolution
        data_list = []
        for t in range(self.interval_nb):
            end_t = now - timedelta(days=self.interval * t)
            start_t = now - timedelta(days=self.interval * (t + 1))
            tier = TierList(end_date=end_t, start_date=start_t)
            winrate_list = tier.get_clan_tier()
            data = []
            for index, value in enumerate(winrate_list):
                if value is None:
                    data.append(50.0)
                else:
                    data.append(int(10000 * value) / 100)
            data_list.append(data)
        return list(map(list, zip(*data_list)))

    def generate(self):
        chart_data = self.get_data()
        day_list = [datetime.now() - timedelta(days=self.interval * t) for t in range(self.interval_nb)][::-1]
        labels = [str(day.month) + "/" + str(day.day) for day in day_list]
        chart = pygal.Line(style=L5RStyle, height=350)
        chart.x_labels = labels
        for index, serie in enumerate(chart_data):
            chart.add(CLANS[index], serie[::-1])
        return chart.render(is_unicode=True)


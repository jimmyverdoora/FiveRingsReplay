from datetime import datetime, timedelta
from stats.charts_base import BaseBar, BasePie, BaseDot, BaseTime
from stats.main import Manager
from stats.names import STRONGHOLDS_OWNERS


class WinRateChart(BaseBar):
    """
    Represents the average winrates.
    :param days: number of days the average is made out of
    """
    def get_data(self, top=False, filt3r=None):
        tier = Manager(start_date=datetime.now() - timedelta(days=self.days))
        winrate_list = tier.get_clan_tier(top, filt3r)
        data = []
        for value in winrate_list:
            if value is None:
                data.append(0.0)
            else:
                data.append(int(10000 * value) / 100)
        return data


class WinRateStrongholdChart(BaseBar):
    """
    Represents the average winrates.
    :param days: number of days the average is made out of
    """
    def get_data(self, clan):
        tier = Manager(start_date=datetime.now() - timedelta(days=self.days))
        winrate_list, _ = tier.get_stronghold_tier(clan)
        index_list = [i for i, c in enumerate(STRONGHOLDS_OWNERS) if c == clan]
        data = []
        for value in winrate_list[index_list[0]:index_list[-1]+1]:
            if value is None:
                data.append(0.0)
            else:
                data.append(int(10000 * value) / 100)
        return data


class WinRatePlot(BaseTime):
    """
    Represents the average winrates during time.
    :param interval: days to average on
    :param interval_nb: number of intervals
    """
    def get_data(self, top=False):
        now = datetime.now()
        # Cotains 7 lists (one for each clan) with the temporal evolution
        data_list = []
        for t in range(self.interval_nb):
            end_t = now - timedelta(days=self.interval * t)
            start_t = now - timedelta(days=self.interval * (t + 1))
            tier = Manager(end_date=end_t, start_date=start_t)
            winrate_list = tier.get_clan_tier(top)
            data = []
            for index, value in enumerate(winrate_list):
                if value is None:
                    data.append(0.0)
                else:
                    data.append(int(10000 * value) / 100)
            data_list.append(data)
        return list(map(list, zip(*data_list)))


class AttendingsChart(BasePie):
    """
    Represents the average winrates.
    :param days: number of days the average is made out of
    """
    def get_data(self):
        manager = Manager(start_date=datetime.now() - timedelta(days=self.days))
        return manager.get_clan_attendings()


class AttendingsStrongholdChart(BasePie):
    """
    Represents the average winrates.
    :param days: number of days the average is made out of
    """
    def get_data(self, clan):
        manager = Manager(start_date=datetime.now() - timedelta(days=self.days))
        att_list = manager.get_stronghold_attendings(clan)
        index_list = [i for i, c in enumerate(STRONGHOLDS_OWNERS) if c == clan]
        data = []
        return att_list[index_list[0]:index_list[-1]+1] 


class AdmissionChart(BasePie):
    def get_data(self):
        manager = Manager(start_date=datetime.now() - timedelta(days=self.days))
        return manager.get_clan_admission()


class AttendingsPlot(BaseTime):
    """
    Represents the average attendings during time.
    :param interval: days to average on
    :param interval_nb: number of intervals
    """
    def get_data(self):
        now = datetime.now()
        # Cotains 7 lists (one for each clan) with the temporal evolution
        data_list = []
        for t in range(self.interval_nb):
            end_t = now - timedelta(days=self.interval * t)
            start_t = now - timedelta(days=self.interval * (t + 1))
            manager = Manager(end_date=end_t, start_date=start_t)
            attendings_list = manager.get_clan_attendings() 
            total = sum(attendings_list)
            data = []
            for index, value in enumerate(attendings_list):
                data.append(int(10000 * value / total) / 100)
            data_list.append(data)
        return list(map(list, zip(*data_list)))


class Matchups(BaseDot):
    """
    Matchup winrates
    :param days: number of days the average is made out of
    """
    def get_data(self):
        tier = Manager(start_date=datetime.now() - timedelta(days=self.days))
        winrate_matrix = tier.get_clan_tier_matrix()
        data = []
        for winrate_list in winrate_matrix:
            tmp_data = []
            for value in winrate_list:
                if value is None:
                    tmp_data.append(50.0)
                else:
                    tmp_data.append(int(10000 * value) / 100)
            data.append(tmp_data)
        return data


class WinRateMatchup(BaseBar):
    """
    Represents the average winrates.
    :param days: number of days the average is made out of
    """
    def get_data(self, clan, top=False, filt3r=None):
        tier = Manager(start_date=datetime.now() - timedelta(days=self.days))
        winrate_list = tier.get_clan_matchups(clan, top, filt3r)
        data = []
        for value in winrate_list:
            if value is None:
                data.append(0.0)
            else:
                data.append(int(10000 * value) / 100)
        return data


class WinRateMatchupPlot(BaseTime):
    """
    Represents the average winrates during time.
    :param interval: days to average on
    :param interval_nb: number of intervals
    """
    def get_data(self, clan, top=False):
        now = datetime.now()
        # Cotains 7 lists (one for each clan) with the temporal evolution
        data_list = []
        for t in range(self.interval_nb):
            end_t = now - timedelta(days=self.interval * t)
            start_t = now - timedelta(days=self.interval * (t + 1))
            tier = Manager(end_date=end_t, start_date=start_t)
            winrate_list = tier.get_clan_matchups(clan, top)
            data = []
            for index, value in enumerate(winrate_list):
                if value is None:
                    data.append(0.0)
                else:
                    data.append(int(10000 * value) / 100)
            data_list.append(data)
        return list(map(list, zip(*data_list)))



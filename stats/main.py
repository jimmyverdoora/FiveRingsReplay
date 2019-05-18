from datetime import datetime, timedelta
from stats.models import Tournament
from stats.names import CLANS, REV_CLANS


class TierList(object):
    """
    Prints the tierlist of the clans and strongholds into a given time frame
    """
    def __init__(self, end_date=None, start_date=None):

        if end_date is None:
            self.end_date = datetime.now()
        else:
            self.end_date = end_date

        if start_date is None:
            self.start_date = self.end_date - timedelta(days=30)
        else:
            self.start_date = start_date

        self.games = self._get_games()

    def _get_games(self):
        # Fetches the games
        games = []
        tournaments = Tournament.objects.all()
        total = len(tournaments)
        tournament_index = 1

        # Cuts the tournaments after end_date
        while tournament_index <= total and tournaments[total - tournament_index].tournament_date > self.end_date:
            tournament_index += 1

        # Adds the games inside the interval
        while tournament_index <= total and tournaments[total - tournament_index].tournament_date > self.start_date:
            games += list(tournaments[total - tournament_index].games.all())
        
        return games

    def get_clan_tier(self):
        """
        Returns the tier list by each clan
        """
        # Calculates wins/losses
        wins = [0] * 7
        losses = [0] * 7
        for game in self.games:
            if game.p1_points > game.p2_points:
                winner = game.p1_clan
                loser = game.p2_clan
            else:
                winner = game.p2_clan
                loser = game.p1_clan
            wins[REV_CLANS[winner]] += 1
            losses[REV_CLANS[loser]] += 1

        # Calculates winrates
        winrates = []
        for index in range(7):
            winrates.append(wins[index] / (wins[index] + losses[index]))
        
        return winrates

    def print_clan_tier(self):
        """
        Prints the tier list to console
        """
        winrates = self.get_clan_tier()
        for index, rate in enumerate(winrates):
            print(10 * " " + str(int(10000 * rate) / 100), end='\r')
            print(CLANS[index])


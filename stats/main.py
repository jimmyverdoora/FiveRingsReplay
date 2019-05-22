from datetime import datetime, timedelta
from stats.models import Tournament
from stats.names import CLANS, REV_CLANS, STRONGHOLDS, REV_STRONGHOLDS
from numpy import zeros


class Manager(object):
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
            tournament_index += 1
        
        return games

    def get_clan_attendings(self):
        attendings = zeros(7)
        current_id = self.games[0].tournament_id
        player_set = set()  # Of their ids
        tmp_attendings = zeros(7)
        for game in self.games:
            if game.tournament_id != current_id:
                if player_set:
                    rounds = sum(tmp_attendings) / len(player_set)
                    attendings += tmp_attendings / rounds
                tmp_attendings = zeros(7)
                player_set = set()
                current_id = game.tournament_id
            if game.topx == 0:
                player_set.add(game.p1_id)
                player_set.add(game.p2_id)
                tmp_attendings[REV_CLANS[game.p1_clan]] += 1
                tmp_attendings[REV_CLANS[game.p2_clan]] += 1

        return [int(attendings[index]) for index in range(7)]

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
            tot = wins[index] + losses[index]
            if tot > 0:
                winrates.append(wins[index] / tot)
            else:
                winrates.append(None)        
        return winrates

    def get_clan_tier_matrix(self):
        """
        Returns the tier list by each clan
        """
        # Calculates wins/losses
        wins = [[0] * 7 for _ in range(7)]
        losses = [[0] * 7 for _ in range(7)]
        for game in self.games:
            if game.p1_points > game.p2_points:
                winner = game.p1_clan
                loser = game.p2_clan
            else:
                winner = game.p2_clan
                loser = game.p1_clan
            wins[REV_CLANS[winner]][REV_CLANS[loser]] += 1
            losses[REV_CLANS[loser]][REV_CLANS[winner]] += 1

        # Calculates winrates
        winrates = []
        for i in range(7):
            tmp_list = []
            for j in range(7):
                tot = wins[i][j] + losses[i][j]
                if tot > 0:
                    tmp_list.append(wins[i][j] / tot)
                else:
                    tmp_list.append(None)        
            winrates.append(tmp_list)
        return winrates

    def get_stronghold_tier(self):
        """
        Returns the tier list by each clan
        """
        # Calculates wins/losses
        n = len(STRONGHOLDS.keys())
        wins = [0] * n
        losses = [0] * n
        for game in self.games:
            if self._check_stronghold(game):
                if game.p1_points > game.p2_points:
                    winner = self._stronghold(game, "p1")
                    loser = self._stronghold(game, "p2")
                else:
                    winner = self._stronghold(game, "p2")
                    loser = self._stronghold(game, "p1") 
                wins[REV_STRONGHOLDS[winner]] += 1
                losses[REV_STRONGHOLDS[loser]] += 1

        # Calculates winrates
        winrates = []
        tots = []
        for index in range(n):
            tot = wins[index] + losses[index]
            if tot > 0:
                winrates.append(wins[index] / tot)
            else:
                winrates.append(None) 
            tots.append(tot)
        return winrates, tots

    def print_clan_tier(self):
        """
        Prints the tier list to console
        """
        winrates = self.get_clan_tier()
        for index, rate in enumerate(winrates):
            if rate is None:
                print(10 * " " + "--.--", end='\r')
            else:
                print(10 * " " + str(int(10000 * rate) / 100), end='\r')
            print(CLANS[index])

    def print_stronghold_tier(self):
        """
        Prints the tier list to console
        """
        winrates, tots = self.get_stronghold_tier()
        for index, rate in enumerate(winrates):
            print(36 * " " + "(%d)" % tots[index], end='\r')
            if rate is None:
                print(30 * " " + "--.--", end='\r')
            else:
                print(30 * " " + str(int(10000 * rate) / 100), end='\r')
            print(STRONGHOLDS[index])
    
    @staticmethod
    def _stronghold(game, player):
        # Hardcoded because it's an exception
        if player == "p1":
            if game.p1_stronghold == "Hisu Mori Toride":
                return "Hisu Mori Toride (%s)" % game.p1_clan
            else:
                return game.p1_stronghold
        else:
            if game.p2_stronghold == "Hisu Mori Toride":
                return "Hisu Mori Toride (%s)" % game.p2_clan
            else:
                return game.p2_stronghold
    
    def _check_stronghold(self, game):
        if game.p1_stronghold is None or game.p2_stronghold is None:
            return False
        if self._stronghold(game, "p1") not in REV_STRONGHOLDS.keys():
            return False
        if self._stronghold(game, "p2") not in REV_STRONGHOLDS.keys():
            return False
        return True


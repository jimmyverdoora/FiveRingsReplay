from stats.models import Tournament, Game
import datetime
import requests


"""DB SYNCHRONIZER"""


def update_db(filter_byes=True):

    # Fetches with the API - tournaments are ordered by end_time. Going backwards until I find the day with the last tourney
    date = datetime.datetime.now()
    while True:
        response = requests.get("http://thelotuspavilion.com/api/v3/tournaments?after=" + date.strftime("%Y-%m-%d"))
        data = response.json()
        if data:
            break
        else:
            date = date - datetime.timedelta(days=1)

    # Reads the last tourney from txt
    with open('stats/tournament.last', 'r') as f:
        last_tournament_id = int(f.readlines()[0])
    if data[-1]['tournament_id'] == last_tournament_id:
        return

    # Launches the update. Gets the date of the last tourney in MY DB
    response = requests.get("http://thelotuspavilion.com/api/v3/tournaments?tournament_id=" + str(last_tournament_id))
    response = response.json()
    tournament_time = datetime.datetime.strptime(response[0]['end_time'], '%Y-%m-%d %H:%M:%S')
    strdate = tournament_time.strftime("%Y-%m-%d")
    index = 1
    result = []

    # Fetches all the new tourneys
    print("Fetching tournaments from lotus pavilion API...")
    while True:
        response = requests.get("http://thelotuspavilion.com/api/v3/tournaments?after=" + strdate + "&page=" + str(index))
        data = response.json()
        if data:
            result += data
            print("Date: " + data[0]['end_time'] + ", Total tournaments fetched: " + str(len(result)), end = "\r")
        else:
            break
        index += 1
    print("Done.")

    # There may be a couples of tournaments I already have in DB
    total = len(result)
    print(str(total) + " new tournaments to add.")
    outside = True
    current_tournament = None
    for index, tourney in enumerate(result):
        print("Current tourney: " + str(index) + " over " + str(total) + ".", end="\r")
        if outside:
            if tourney["tournament_id"] == last_tournament_id: outside = False
        else:
            tier = tourney['tournament_tier']
            country = tourney['country']
            region = tourney['region']
            tournament_date = tourney['end_time']
            tournament_name = tourney['tournament_name']
            tournament_id = tourney["tournament_id"]

            current_tournament = Tournament.objects.create(
                tournament_date=tournament_date,
                tournament_name=tournament_name,
                tournament_id=tournament_id,
                tournament_tier=tier,
                country=country,
                region=region)

            # Fetching games of the specific tourney I just created
            games = []
            # It is possible that more than 50 games are played in a tournament
            while True:
                response = requests.get("http://thelotuspavilion.com/api/v3/games?tournament_id="\
                        + str(tourney['tournament_id']) + "&page=" + str(index))
                data = response.json()
                if data:
                    games += data
                else:
                    break
                index += 1

            # Kills the games with "BYE" or without clan or role or result
            if filter_byes:
                tot_games = len(games)
                for index in range(tot_games):
                    tmp_game = games[tot_games - index - 1]
                    if tmp_game['p2_name'] == "BYE" or tmp_game['p1_name'] == "BYE"\
                            or (tmp_game.get('p1_clan', None) is None) or (tmp_game.get('p2_clan', None) is None)\
                            or (tmp_game.get('p1_role', None) is None) or (tmp_game.get('p2_role', None) is None)\
                            or (tmp_game.get('p1_points', None) is None) or (tmp_game.get('p2_points', None) is None):
                        del games[tot_games - index - 1]

            # Create the games in DB
            for game in games:
                Game.objects.create(
                        tournament=current_tournament,
                        topx=game.get('topx', None),
                        p1_id=game.get('p1_id', None),
                        p1_clan=game['p1_clan'],
                        p1_stronghold=game.get('p1_stronghold', None),
                        p1_role=game['p1_role'],
                        p1_points=game['p1_points'],
                        p2_id=game.get('p2_id', None),
                        p2_clan=game['p2_clan'],
                        p2_stronghold=game.get('p2_stronghold', None),
                        p2_role=game['p2_role'],
                        p2_points=game['p2_points'])

    # Updates last tournament
    with open('stats/tournament.last', 'w') as f:
        f.write(str(tournament_id))


from django.shortcuts import render
from stats.charts import AttendingsChart, AttendingsPlot, Matchups, WinRateChart, WinRatePlot
from stats.names import CLANS


def homepage(request):
    """
    Renders the general stats.
    """
    chart_m = WinRateChart(30)
    time_chart_m = WinRatePlot(30)
    attendings_m = AttendingsChart(30)
    #time_attendings_m = AttendingsPlot(30)
    matchups = Matchups(30)
    # Build numbers to be printed
    attendings = attendings_m.get_data()
    attendings_dict = dict()
    for index, number in enumerate(attendings):
        attendings_dict[CLANS[index]] = number
    attendings_dict["Total"] = sum(attendings)
    context = {
            'winrates': chart_m.generate(),
            'time_winrates': time_chart_m.generate(),
            'attendings': attendings_m.generate(),
            #'time_attendings': time_attendings_m.generate(),
            'matchups': matchups.generate(),
            'clans': CLANS,
            'clans_att': attendings_dict
            }
    return render(request, "homepage.html", context)


def clan_view(request, clan):
    context = print(clan)
    return render(request, "clan.html", context)


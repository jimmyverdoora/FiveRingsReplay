from django.shortcuts import render
from stats.charts import AdmissionChart, AttendingsChart, AttendingsPlot, AttendingsStrongholdChart, Matchups, WinRateChart, WinRatePlot, WinRateStrongholdChart, WinRateMatchup, WinRateMatchupPlot
from stats.names import COLORS, CLANS, REV_CLANS, STRONGHOLDS, STRONGHOLDS_OWNERS
from datetime import datetime, timedelta
from stats.main import Manager


def homepage(request):
    """
    Renders the general stats.
    """
    # premade the manager to spare cpu time
    interval_nb = 6
    interval = 30

    managers = []
    now = datetime.now()
    for t in range(interval_nb):
            end_t = now - timedelta(days=interval * t)
            start_t = now - timedelta(days=interval * (t + 1))
            managers.append(Manager(end_date=end_t, start_date=start_t))

    chart_m = WinRateChart(managers[0], horizontal=True)
    chart_m_top = WinRateChart(managers[0], horizontal=True, top=True)
    time_chart_m = WinRatePlot(managers)
    time_chart_m_top = WinRatePlot(managers, top=True)
    attendings_m = AttendingsChart(managers[0])
    admission_m = AdmissionChart(managers[0])
    chart_formal_m = WinRateChart(managers[0], horizontal=True, filt3r=['formal', 'premier'])
    #chart_formal_m_top = WinRateChart(30, top=True, filt3r=['formal', 'premier'])
    chart_premier_m = WinRateChart(managers[0], horizontal=True, filt3r=['premier'])
    #chart_premier_m_top = WinRateChart(30, top=True, filt3r=['premier'])
    #time_attendings_m = AttendingsPlot(30)
    #matchups = Matchups(30)
    # Build numbers to be printed
    attendings = attendings_m.get_data()
    attendings_dict = dict()
    for index, number in enumerate(attendings):
        attendings_dict[CLANS[index]] = number
    attendings_dict["Total"] = sum(attendings)
    admission = admission_m.get_data()
    admission_dict = dict()
    for index, number in enumerate(admission):
        admission_dict[CLANS[index]] = number
    admission_dict["Total"] = sum(admission)

    context = {
            'winrates': chart_m.generate(),
            'winrates_top': chart_m_top.generate(),
            'time_winrates': time_chart_m.generate(),
            'time_winrates_top': time_chart_m_top.generate(),
            'attendings': attendings_m.generate(),
            'admission': admission_m.generate(),
            'formal': chart_formal_m.generate(),
            #'formal_top': chart_formal_m_top.generate(),
            'premier': chart_premier_m.generate(),
            #'premier_top': chart_premier_m_top.generate(),
            #'time_attendings': time_attendings_m.generate(),
            #'matchups': matchups.generate(),
            'clans': CLANS,
            'clans_att': attendings_dict,
            'clans_add': admission_dict
            }
    return render(request, "homepage.html", context)


def clan_view(request, clan):
    # premade the manager to spare cpu time
    interval_nb = 6
    interval = 30

    managers = []
    now = datetime.now()
    for t in range(interval_nb):
            end_t = now - timedelta(days=interval * t)
            start_t = now - timedelta(days=interval * (t + 1))
            managers.append(Manager(end_date=end_t, start_date=start_t))

    chart_stronghold = WinRateStrongholdChart(managers[0])
    att_stronghold = AttendingsStrongholdChart(managers[0])
    attendings = att_stronghold.get_data(clan)
    attendings_dict = dict()
    starting_index = STRONGHOLDS_OWNERS.index(clan)
    for index, number in enumerate(attendings):
        attendings_dict[STRONGHOLDS[starting_index + index]] = number
    attendings_dict["Total"] = sum(attendings)

    matchups = WinRateMatchup(managers[0], horizontal=True)
    time_chart_m = WinRateMatchupPlot(managers)

    context = {"winrates_stronghold": chart_stronghold.generate_stronghold(clan),
               "att_stronghold": att_stronghold.generate_stronghold(clan),
               "stronghold_att": attendings_dict,
               "matchups": matchups.generate_clan(clan),
               "matchups_time": time_chart_m.generate_clan(clan),
               "color": COLORS[REV_CLANS[clan]],
               'clans': CLANS,
               "clan": clan}
    return render(request, "clan.html", context)


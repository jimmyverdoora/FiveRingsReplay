from django.shortcuts import render
from stats.charts import WinRateChart, WinRatePlot


def homepage(request):
    """
    Renders the general stats.
    """
    chart_m = WinRateChart(30)
    time_chart_m = WinRatePlot(30)
    context = {
            'chart': chart_m.generate(),
            'time_chart': time_chart_m.generate()
            }
    return render(request, "homepage.html", context)

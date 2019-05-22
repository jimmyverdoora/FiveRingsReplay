from django.contrib import admin
from django.urls import path
from stats.views import homepage, clan_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage),
    path('<slug:clan>', clan_view),
]

from django.db import models


"""Fetching lotuspavilion games to avoid stressing api calls"""


class Tournament(models.Model):

    tournament_date = models.DateTimeField()
    tournament_name = models.CharField(max_length=255) 
    tournament_id = models.IntegerField()
    tournament_tier = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    region = models.CharField(max_length=32)

    class Meta:
        ordering = ['tournament_date']


class Game(models.Model):
    
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, related_name='games')
    topx = models.IntegerField(null=True)
    p1_id = models.IntegerField(null=True)
    p1_clan = models.CharField(max_length=16)
    p1_stronghold = models.CharField(max_length=32, null=True)
    p1_role = models.CharField(max_length=32)
    p1_points = models.IntegerField()
    p2_id = models.IntegerField(null=True)
    p2_clan = models.CharField(max_length=16)
    p2_stronghold = models.CharField(max_length=32, null=True)
    p2_role = models.CharField(max_length=32)
    p2_points = models.IntegerField()

    class Meta:
        order_with_respect_to = 'tournament'


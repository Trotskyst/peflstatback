from fill.models import *
from django.contrib import admin


class ChempsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link')


class DivsAdmin(admin.ModelAdmin):
    list_display = ('id', 'chemp', 'name', 'link', 'sort')


class TeamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'div', 'name', 'link')


class TursAdmin(admin.ModelAdmin):
    list_display = ('id', 'div', 'number', 'date', 'link', 'season')


class GamesTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'tur', 'link')


# class GamesTextReportAdmin(admin.ModelAdmin):
#     list_display = ('id', 'gametext', 'report')


class GamesTextReport_MainAdmin(admin.ModelAdmin):
    list_display = ('gametext', 'city', 'stadium', 'viewers', 'wheater', 'arbitr', 'minutes',
                    'team_home', 'team_guest', 'goals_home', 'goals_guest', 'manager_home', 'manager_guest',
                    'kick_home', 'kick_guest', 'kick_target_home', 'kick_target_guest',
                    'goalpost_home', 'offside_home', 'goalpost_guest', 'offside_guest',
                    'corner_home', 'corner_guest', 'corner_cross_home', 'corner_cross_guest', 'corner_playout_home',
                    'corner_playout_guest',
                    'possession_home', 'possession_guest',
                    'kick_near_home', 'kick_near_guest', 'kick_near_target_home', 'kick_near_target_guest',
                    'kick_far_home', 'kick_far_guest', 'kick_far_target_home', 'kick_far_target_guest',
                    'kick_blocked_home', 'kick_blocked_guest',
                    'pass_home', 'pass_guest', 'pass_accurate_home', 'pass_accurate_guest',
                    'bend_home', 'bend_guest', 'bend_accurate_home', 'bend_accurate_guest',
                    'dribbling_home', 'dribbling_guest', 'dribbling_successful_home', 'dribbling_successful_guest',
                    'tackle_home', 'tackle_guest', 'tackle_successful_home', 'tackle_successful_guest',
                    'height_fight_home', 'height_fight_guest', 'height_fight_successful_home',
                    'height_fight_successful_guest',
                    'intercept_home', 'intercept_guest',
                    'turnover_home', 'turnover_guest',
                    'foul_home', 'foul_guest', 'penalty_home', 'penalty_guest',
                    'freekick_home', 'freekick_guest', 'freekick_cross_home', 'freekick_cross_guest',
                    'freekick_kick_home',
                    'freekick_kick_guest', 'freekick_playout_home', 'freekick_playout_guest')


class GamesTextReport_GoalsAdmin(admin.ModelAdmin):
    list_display = ('gametext', 'home', 'minutes', 'team', 'player_goal', 'player_pass', 'own_goal', 'penalty')

class Stat_Players_BombardersAdmin(admin.ModelAdmin):
    list_display = ('div','number', 'name', 'team', 'goal', 'played')

class Stat_Players_PivotsAdmin(admin.ModelAdmin):
    list_display = ('div','number', 'name', 'team', 'pases', 'played')

admin.site.register(Season)
admin.site.register(Chemps, ChempsAdmin)
admin.site.register(Divs, DivsAdmin)
admin.site.register(Teams, TeamsAdmin)
admin.site.register(Turs, TursAdmin)
admin.site.register(GamesText, GamesTextAdmin)
# admin.site.register(GamesTextReport, GamesTextReportAdmin)
admin.site.register(GamesTextReport_Main, GamesTextReport_MainAdmin)
admin.site.register(GamesTextReport_Player)
admin.site.register(GamesTextReport_Goals, GamesTextReport_GoalsAdmin)
admin.site.register(Stat_Players_Bombarders, Stat_Players_BombardersAdmin)
admin.site.register(Stat_Players_Pivot, Stat_Players_PivotsAdmin)

from django.urls import path, include
from api.views import *

urlpatterns = [
    path("countries/", ChempsCountriesView.as_view()),
    path("country/<str:country>/", DivsCountriesView.as_view()),
    path("main/<str:season>/<str:country>/<str:division>/", StatMainView.as_view()),
    path("players/<str:season>/<str:country>/<str:division>/", StatPlayerView.as_view()),
    path("goals/<str:season>/<str:country>/<str:division>/", StatGoalsView.as_view()),
    path("additional/teamlist/<str:season>/<str:country>/<str:division>/", StatTeamListView.as_view()),
    path("additional/players_list_goal/<str:season>/<str:country>/<str:division>/", StatPlayersListGoalView.as_view()),
    path("additional/players_list_pass/<str:season>/<str:country>/<str:division>/", StatPlayersListPassView.as_view()),
    path("additional/players_list_goal_and_pass/<str:season>/<str:country>/<str:division>/",
         StatPlayersListGoalAndPassView.as_view()),
    path("additional/players_bombarders/<str:season>/<str:country>/<str:division>/",
         StatPlayersBombardersView.as_view()),
    path("additional/players_pivots/<str:season>/<str:country>/<str:division>/",
         StatPlayersPivotsView.as_view()),
    path("additional/players_goal_and_pases/<str:season>/<str:country>/<str:division>/",
         StatPlayersGoalAndPassView.as_view()),
    path("additional/team_playedmaxtime/<str:season>/<str:country>/<str:division>/<str:team>/",
         StatPlayersPlayedMaxTimeView.as_view()),
    path("additional/player/<str:season>/<str:player_id>/", GamesTextReportPlayerStatView.as_view()),
]

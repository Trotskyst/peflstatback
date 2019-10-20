from django.urls import path, include
from fill.views import *


urlpatterns = [
    path('', index_view, name='index'),
    path('fill/download_chemp/', fill_chemp, name='fill_chemp'),
    path('fill/download_rasp/<str:season>/', fill_rasp, name='fill_rasp'),
    path('fill/download_tur/<str:season>/', fill_tur, name='fill_tur'),
    path('fill/download_gametext/<str:season>/', fill_gametext, name='fill_gametext'),
    path('fill/download_report_processing/<str:season>/', fill_report_processing, name='fill_report_processing'),
    path('fill/download_report_players_processing/<str:season>/', fill_report_players_processing, name='fill_report_players_processing'),
    path('fill/download_report_goals_processing/<str:season>/', fill_report_goals_processing, name='fill_report_goals_processing'),
    path('fill/download_makedir/<str:season>/', fill_makedir, name='fill_makedir'),
    path('fill/tests/<str:season>/', fill_tests, name='fill_tests'),
    # path('fill/fill_test_ttd/', fill_test_ttd, name='fill_test_ttd'),
]
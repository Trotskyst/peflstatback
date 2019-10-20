from django.shortcuts import render
import psycopg2
from fill.functions_pefl import *
from fill.functions import *
from fill.functions_tests import *
import os


def index_view(request):
    season = '17'
    data = {'season': season}
    # data = {'fill_makedir': 'fill_makedir/' + season}
    return render(request, 'fill_index.html', data)


def fill_chemp(request):
    # res = CheckAuth()
    # if res != 'yes':  # если авторизация прошла неуспешно
    #     return res
    # else:
    download_chemp(request)
    # data = {}
    return render(request, 'download.html', {})


def fill_rasp(request, **kwargs):
    season = kwargs['season']
    # res = CheckAuth()
    # if res != 'yes':  # если авторизация прошла неуспешно
    #     return res
    # else:
    download_rasp(request, season)
    # data = {}
    return render(request, 'download.html', {})


def fill_tur(request, **kwargs):
    season = kwargs['season']
    # res = CheckAuth()
    # if res != 'yes':  # если авторизация прошла неуспешно
    #     return res
    # else:
    download_tur(request, season)
    # data = {}
    return render(request, 'download.html', {})


def fill_gametext(request, **kwargs):
    CheckAuth()
    season = kwargs['season']
    # res = CheckAuth()
    # if res != 'yes':  # если авторизация прошла неуспешно
    #     return res
    # else:
    download_gametext(request, season)
    # data = {}
    return render(request, 'download.html', {})


def fill_report_processing(request, **kwargs):
    season = kwargs['season']
    download_report_processing(request, season)
    # data = {}
    return render(request, 'download.html', {})


def fill_report_players_processing(request, **kwargs):
    season = kwargs['season']
    download_report_players_processing(request, season)
    # data = {}
    return render(request, 'download.html', {})

def fill_report_goals_processing(request, **kwargs):
    start_time = time.time()
    season = kwargs['season']
    print("Запуск")
    download_tur(request, season)
    download_gametext(request, season)
    download_report_processing(request, season)
    download_report_players_processing(request, season)
    download_report_goals_processing(request, season)
    update_stat(request, season)


    print('Время выполнения -', secondsToStr(time.time() - start_time))
    return render(request, 'download.html', {})


def fill_makedir(request, **kwargs):
    season = kwargs['season']
    chemp_list = Chemps.objects.all()
    divs_list = Divs.objects.all()
    # Чемпионаты
    for d in chemp_list:
        directory = 'F:/Github/peflstat/download/' + season + '/' + d.name
        if not os.path.exists(directory):
            os.makedirs(directory)
    # Дивизионы
    for d in divs_list:
        directory = 'F:/Github/peflstat/download/' + season + '/' + d.chemp.name + '/' + d.name
        if not os.path.exists(directory):
            os.makedirs(directory)

    data = {}
    return render(request, 'download.html', data)

def fill_tests(request, **kwargs):
    season = kwargs['season']
    test_viewers(request, season, 1)


# def fill_test_ttd(request):
#     url = 'http://pefl.ru/plug.php?p=refl&t=ttddiv&j=14&v=17&z=330119f5f7e2aede884f02c96c7830f0'
#     # скачиваем матч
#     res = CheckAuth()
#     if res != 'yes':  # если авторизация прошла неуспешно
#         return res
#     else:
#         pefl_cookies = GetFromJSON('pefl_auth', 'cookies')
#         print(pefl_cookies)
#         text = text_from_link(pefl_cookies, url)
    # разбиваем на матч на строки
    # text_lines = text.splitlines()

import time
from django.shortcuts import render
import requests
import json
from fill.models import *
import psycopg2
from fill.functions import *
from fill.functions_stat_players import *
from lxml import etree
from itertools import chain
from django.db.models import Q
from django.db import connection, transaction


def CheckAuth() -> str:
    pefl_username = GetFromJSON('pefl_auth', 'username')
    pefl_cookies = GetFromJSON('pefl_auth', 'cookies')
    if pefl_cookies == '':
        # авторизуемся
        pefl_password = GetFromJSON('pefl_auth', 'password')
        res = Auth(pefl_username, pefl_password)
    else:
        res = 'yes'
    return res


def Auth(username: str, password: str) -> str:
    with requests.Session() as s:
        payload = "rusername=" + username + "&rpassword=" + password
        headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            'Cache-Control': "max-age=0",
            'Connection': "keep-alive",
            'Content-Length': "36",
            'Content-Type': "application/x-www-form-urlencoded",
            'Host': "pefl.ru",
            'Origin': "http://pefl.ru",
            'Referer': "http://pefl.ru/auth.php",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            'x-compress': "null"
        }

        querystring = {"m": "login", "a": "check"}
        page = s.request("POST", 'http://pefl.ru/auth.php', data=payload,
                         headers=headers, params=querystring)
        page.encoding = 'windows-1251'

        print(page.text, file=open('F:/Github/peflstat/file2.htm', 'w'))

        msg = 'Неверное имя или пароль'
        if msg in page.text:
            res = msg
        else:
            cookies = page.headers['Set-Cookie']
            SetToJSON('pefl_auth', 'cookies', cookies)
            res = 'yes'
    return res


def download_chemp(request) -> str:
    cookies = GetFromJSON('pefl_auth', 'cookies')
    pefl_url = 'http://pefl.ru/'
    doc = text_from_link(cookies, pefl_url)

    # ссылка на Турниры
    url = pefl_url + find_link_by_link_text(doc, ' Турниры')
    doc = text_from_link(cookies, url)

    elements = doc.xpath('//a[contains(@href, "plug.php?p=refl&t=t&")]')

    chemps = []
    divs = []
    commands = []

    # составлям список стран
    for links in elements:
        link = links.get('href').replace('plug.php?p=refl&t=t&j=', '')
        text = links.text
        chemps.append([text, link])

    chemps = sorted(set(map(tuple, chemps)), reverse=False)

    count_chemp = len(chemps)

    Chemps.objects.all().delete()
    Chemps.objects.bulk_create(
        Chemps(name=name, link=link) for name, link in chemps)

    print('Всего стран =', len(chemps))

    print('Составлям список дивизионов')

    count = 0
    count_all = 0

    for name, link in chemps:
        chemp = name
        chemp_link = 'plug.php?p=refl&t=t&j=' + link

        count += 1
        print(count, 'страна из', count_chemp)

        doc = text_from_link(cookies, pefl_url + chemp_link)
        number = 0

        # составлям список дивизионов
        elements = doc.xpath('//td/a[contains(@href, "plug.php?p=refl&t=v&")]')
        for links in elements:
            div_link = links.get('href').replace('plug.php?p=refl&t=v&j=', '')
            div = links.text
            count_all += 1
            number += 1

            try:
                chemp_id = Chemps.objects.get(name__iexact=chemp)
            except Exception:
                chemp_id = None

            divs.append([chemp_id, div, div_link, number])

        # break

    Divs.objects.all().delete()
    Divs.objects.bulk_create(
        Divs(chemp=chemp_id, name=name, link=link, sort=number) for chemp_id, name, link, number in divs)

    print('Всего дивизионов =', count_all)
    print('Составлям список команд')

    count = 0
    count_commands = 0

    for chemp_id, name, link, number in divs:
        div = name
        div_link = link = 'plug.php?p=refl&t=v&j=' + link
        count += 1

        try:
            div_id = Divs.objects.get(name__iexact=div, chemp=chemp_id)
        except Exception:
            div_id = None

        if count_commands // 5 == count_commands / 5:
            print(count, 'дивизион из', count_all)

        doc = text_from_link(cookies, pefl_url + div_link)

        # ссылка на Таблицу
        url = pefl_url + find_link_by_link_text(doc, 'Таблица')
        doctxt = text_from_link2(cookies, url)

        json_list = []
        for s in doctxt.split('\n'):
            if s.startswith('getjson'):
                json_list = s.split('\'')
                # print(json_list)
                url = json_list[1]

        json_text = text_from_json(cookies, pefl_url + 'json.php?' + url)
        command_list = []
        for text in json_text['data']:
            # print(text[1]);
            command_list.append(text[1].split('|'))
        # print(command_list)

        for command in command_list:
            commands.append([div_id, command[0], '!' + command[1]])

        # if count == 3:
        #     break

    # print(commands)

    count_all = len(commands)

    # очищаем список команд
    Teams.objects.all().delete()

    info_for_adding = []
    count = 0

    # print(commands)

    for div_id, command, command_link in commands:
        count += 1

        info_for_adding.append([div_id, command, command_link])

        if count // 100 == count / 100:
            print(count, 'из', count_all)

        if count // 100 == count / 100:
            # Добавляем их
            Teams.objects.bulk_create(
                Teams(div=div_id, name=command, link=command_link) for
                div_id, command, command_link in info_for_adding)
            info_for_adding = []

    # Добавляем оставшиеся
    Teams.objects.bulk_create(
        Teams(div=div_id, name=command, link=command_link) for
        div_id, command, command_link in info_for_adding)

    print('Всего команд:', count)
    data = {
        # 'text1': 'Всего стран =' + str(len(chemps)),
        'text1': pefl_url,
    }
    return render(request, 'fill_index.html', data)


def download_rasp(request, season):
    divs_list = Divs.objects.all()
    print('Всего дивизионов =', len(divs_list))
    cookies = GetFromJSON('pefl_auth', 'cookies')
    pefl_url = 'http://pefl.ru/'

    turs = []
    count = 0
    count_div_all = len(divs_list)
    count_div = 0

    # очищаем список туров
    Turs.objects.filter(season__number=season).delete()

    # ссылка на сезон
    try:
        season_id = Season.objects.get(number=season)
    except Exception:
        season_id = None

    for d in divs_list:
        count_div += 1
        print(count_div, ' дивизион из', count_div_all)

        url = 'plug.php?p=refl&t=v&j=' + d.link
        # скачиваем дивизион
        doc = text_from_link(cookies, pefl_url + url)
        url = find_link_by_link_text(doc, 'Расписание и результаты')
        # скачиваем список туров
        doc = text_from_link(cookies, pefl_url + url)
        # список туров
        elements = doc.xpath('//a[contains(@href, "plug.php?p=refl&t=x&")]')

        if not elements:
            url = None
            text = None
        else:
            for links in elements:
                count += 1
                # ссылка на тур
                url = links.get('href')
                url = url.replace('http://pefl.ru/', '')
                url = url.replace('http://www.pefl.ru/', '')
                url = url.replace('plug.php?p=refl&t=x&j=', '')
                # текст ссылки
                text = links.text
                # обрабатываем информацию о туре
                text_list = text.split(' ')
                tur_number = text_list[0]
                tur_date = text_list[2].replace('(', '')
                tur_date = tur_date.replace(')', '')
                tur_date_list = tur_date.split('.')
                tur_date = '20' + tur_date_list[2] + '-' + tur_date_list[1] + '-' + tur_date_list[0]
                # ссылка на дивизион
                try:
                    div_id = Divs.objects.get(link=d.link)
                except Exception:
                    div_id = None

                turs.append([div_id, url, tur_number, tur_date, season_id])

                if count // 100 == count / 100:
                    # Добавляем их
                    Turs.objects.bulk_create(
                        Turs(div=div_id, link=url, number=tur_number, date=tur_date, season=season_id) for
                        div_id, url, tur_number, tur_date, season_id in turs)
                    turs = []

                # print(div_id, url, tur_number, tur_date)

        # break

    Turs.objects.bulk_create(
        Turs(div=div_id, link=url, number=tur_number, date=tur_date, season=season_id) for
        div_id, url, tur_number, tur_date, season_id in turs)

    print('Всего туров:', count)

    # data = {}
    # return render(request, 'fill_index.html', data)


def download_tur(request, season):
    turs_list = Turs.objects.filter(gamestext__isnull=True, season__number=season)
    # turs_list = Turs.objects.filter(season__number=season)
    print('Всего туров =', len(turs_list))

    cookies = GetFromJSON('pefl_auth', 'cookies')
    pefl_url = 'http://pefl.ru/'

    games = []
    count = 0
    count_tur_all = len(turs_list)
    count_tur = 0

    # очищаем список матчей
    # GamesText.objects.all().delete()

    for d in turs_list:
        count_tur += 1
        print(count_tur, 'тур из', count_tur_all)

        url = 'plug.php?p=refl&t=x&j=' + d.link
        # скачиваем тур
        doc = text_from_link(cookies, pefl_url + url)
        # список матчей
        elements = doc.xpath('//a[contains(@href, "plug.php?p=refl&t=if&")]')

        if not elements:
            url = None
            text = None
        else:
            for links in elements:
                count += 1
                # ссылка на тур
                url = links.get('href')
                url = url.replace('http://pefl.ru/', '')
                url = url.replace('http://www.pefl.ru/', '')
                url = url.replace('plug.php?p=refl&t=if&j=', '')

                # ссылка на тур
                try:
                    tur_id = Turs.objects.get(link=d.link)
                except Exception:
                    tur_id = None

                games.append([tur_id, url])

                if count // 100 == count / 100:
                    # Добавляем их
                    GamesText.objects.bulk_create(
                        GamesText(tur=tur_id, link=url) for
                        tur_id, url in games)
                    games = []

        # print(url)
        # break

    GamesText.objects.bulk_create(
        GamesText(tur=tur_id, link=url) for
        tur_id, url in games)

    print('Всего матчей:', count)

    # data = {}
    # return render(request, 'download.html', data)


def download_gametext(request, season):
    # country = 'Украина'
    # division = 'Первая лига'
    # games_list = GamesText.objects.filter(
    #     tur__div__chemp__name__iexact=country).filter(
    #     tur__div__name__iexact=division, gamestextreport_main__isnull=True, tur__season__number=season)

    # games_list = GamesText.objects.all()
    games_list = GamesText.objects.filter(gamestextreport_main__isnull=True, tur__season__number=season)
    # cookies = GetFromJSON('pefl_auth', 'cookies')
    pefl_url = 'http://pefl.ru/'

    games = []
    count = 0
    count_game_all = len(games_list)
    # print(count_game_all)
    count_game = 0

    # очищаем список матчей
    # GamesTextReport_Main.objects.all().delete()

    for d in games_list:
        count_game += 1

        chemp_name = d.tur.div.chemp.name
        division_name = d.tur.div.name

        directory = 'F:/Github/peflstat/download/' + season + '/' + chemp_name + '/' + division_name
        filename = directory + '/' + str(d.id)

        # print(filename)

        if count_game // 100 == count_game / 100:
            print(count_game, 'матч из', count_game_all)

        if os.path.exists(filename) == False:

            # if chemp_name != 'Украина':
            #     continue

            url = 'plug.php?p=refl&t=if&j=' + d.link
            # скачиваем матч
            text = text_from_link2(pefl_url + url)
            # разбиваем на матч на строки
            text_lines = text.splitlines()
            j1 = 0
            j2 = 0
            report = ''
            # отсекаем лишнее
            b = False
            for i in range(len(text_lines)):
                s = text_lines[i]
                if 'Матч начался' in s:
                    j1 = i
                    b = True
                if b:
                    report += s + "\n"

                if 'Послематчевое интервью' in s:
                    break

            # сохраняем файл
            print(report, file=open(filename, 'w'))

            # if count_game > 50:
            # break

    # data = {}
    # return render(request, 'download.html', data)


def download_report_processing_mainstatistic8(s_current: str, s_next: str):
    s = s_current[0:s_current.find('<') - 1].replace(',', '(')
    s_tags_b_array = s.split('(')
    value1 = int(s_tags_b_array[0])
    value2 = int(s_tags_b_array[1])
    value3 = int(s_tags_b_array[2])
    value4 = int(s_tags_b_array[3])

    s = s_next[0:s_next.find('<') - 1].replace(',', '(')
    s_tags_b_array = s.split('(')
    value5 = int(s_tags_b_array[0])
    value6 = int(s_tags_b_array[1])
    value7 = int(s_tags_b_array[2])
    value8 = int(s_tags_b_array[3])
    return [value1, value2, value3, value4, value5, value6, value7, value8]


def download_report_processing_mainstatistic6(s_current: str, s_next: str):
    s = s_current[0:s_current.find('<') - 1].replace(',', '(')
    s_tags_b_array = s.split('(')
    value1 = int(s_tags_b_array[0])
    value2 = int(s_tags_b_array[1])
    value3 = int(s_tags_b_array[2])

    s = s_next[0:s_next.find('<') - 1].replace(',', '(')
    s_tags_b_array = s.split('(')
    value4 = int(s_tags_b_array[0])
    value5 = int(s_tags_b_array[1])
    value6 = int(s_tags_b_array[2])
    return [value1, value2, value3, value4, value5, value6]


def download_report_processing_mainstatistic4(s_current: str, s_next: str):
    s = s_current[0:s_current.find('<') - 1]
    s_tags_b_array = s.split('(')
    value1 = int(s_tags_b_array[0])
    value2 = int(s_tags_b_array[1])

    s = s_next[0:s_next.find('<') - 1]
    s_tags_b_array = s.split('(')
    value3 = int(s_tags_b_array[0])
    value4 = int(s_tags_b_array[1])
    return [value1, value2, value3, value4]


def download_report_processing_mainstatistic2(s_current: str, s_next: str):
    value1 = int(s_current[0:s_current.find('<')])
    value2 = int(s_next[0:s_next.find('<')])
    return [value1, value2]


def download_report_processing(request, season):
    # country = 'Австралия'
    # division = 'Хёндай А-Лига'
    games_list = GamesText.objects.filter(gamestextreport_main__isnull=True, tur__season__number=season)
    # games_list = GamesText.objects.filter(
    #     tur__div__chemp__name__iexact=country).filter(
    #     tur__div__name__iexact=division)

    # games_list = GamesTextReport.objects.all()
    print('Всего матчей =', len(games_list))

    info_for_adding = []

    count = 0
    count_all = len(games_list)

    # очищаем матчи
    # GamesTextReport_Main.objects.all().delete()

    for d in games_list:
        chemp_name = d.tur.div.chemp.name
        division_name = d.tur.div.name

        # if d.id != 65565:
        #     continue

        lines = []
        directory = 'F:/Github/peflstat/download/' + season + '/' + chemp_name + '/' + division_name
        with open(directory + '/' + str(d.id)) as f:
            lines = f.read().splitlines()

        # print(directory + '/' + str(d.id))

        count += 1
        s = lines[0]
        s_html = html.document_fromstring(s)

        # minutes = 0

        # Зрители
        viewers = -1
        if 'Зрителей' not in s:
            viewers = 0

        # Город + Стадион
        if 'Нейтральное поле' in s:
            city = 'нет'
            stadium = 'нет'
        else:
            s_tags_b = s_html.xpath('//b')
            s_tmp_array = s_tags_b[0].text_content().split('.')
            city = s_tmp_array[0].strip()
            stadium = s_tmp_array[1].strip()

            # Зрители
            if viewers != 0:
                viewers = int(s_tags_b[1].text_content().strip())

        # Погода
        if 'system/img/w0.png' in s:
            wheater = 'sun'
        elif 'system/img/w1.png' in s:
            wheater = 'rain'
        elif 'system/img/w2.png' in s:
            wheater = 'snow'

        s = lines[1]

        # Арбитр
        if 'Главный арбитр' not in s:
            arbitr = 'нет'
        else:
            arbitr = s.split(':')[1].strip()[:-1].replace("'", "`")

        i = 0
        for s in lines:
            i += 1
            # Минут в матче
            # if 'Главный судья добав' in s:
            #     minutes = 90 + only_digit(s)
            if 'удья добав' in s or 'К основному времени' in s or 'добавляет к' in s:
                minutes = 90 + only_digit(s)

            if 'Финальный свисток' in s:
                s_html = html.document_fromstring(s)
                s_tags_b = s_html.xpath('//b')

                team_home = s_tags_b[0].text_content().strip()
                team_guest = s_tags_b[2].text_content().strip()

                s_tags_b_array = s_tags_b[1].text_content().split(':')
                goals_home = int(s_tags_b_array[0].strip())
                goals_guest = int(s_tags_b_array[1].strip())

                manager_home = s_tags_b[3].text_content().strip()
                manager_guest = s_tags_b[4].text_content().strip()

            if '>Удары (в створ)<' in s:
                s = download_report_processing_mainstatistic4(s, lines[i])
                kick_home = s[0]
                kick_target_home = s[1]
                kick_guest = s[2]
                kick_target_guest = s[3]

            if '>Штанги, перекладины<' in s:
                s = download_report_processing_mainstatistic2(s, lines[i])
                goalpost_home = s[0]
                goalpost_guest = s[1]

            if '>Офсайды<' in s:
                s = download_report_processing_mainstatistic2(s, lines[i])
                offside_home = s[0]
                offside_guest = s[1]

            if '>Угловые<' in s:
                s = download_report_processing_mainstatistic6(s, lines[i])
                corner_home = s[0]
                corner_cross_home = s[1]
                corner_playout_home = s[2]
                corner_guest = s[3]
                corner_cross_guest = s[4]
                corner_playout_guest = s[5]

            if '>Владение мячом' in s:
                s = download_report_processing_mainstatistic2(s, lines[i])
                possession_home = s[0]
                possession_guest = s[1]

            if '>Удары из штрафной<' in s:
                s = download_report_processing_mainstatistic4(s, lines[i])
                kick_near_home = s[0]
                kick_near_target_home = s[1]
                kick_near_guest = s[2]
                kick_near_target_guest = s[3]

            if '>Удары из-за штрафной<' in s:
                s = download_report_processing_mainstatistic4(s, lines[i])
                kick_far_home = s[0]
                kick_far_target_home = s[1]
                kick_far_guest = s[2]
                kick_far_target_guest = s[3]

            if '>Заблокированные удары<' in s:
                s = download_report_processing_mainstatistic2(s, lines[i])
                kick_blocked_home = s[0]
                kick_blocked_guest = s[1]

            if '>Передачи<' in s:
                s = download_report_processing_mainstatistic4(s, lines[i])
                pass_home = s[0]
                pass_accurate_home = s[1]
                pass_guest = s[2]
                pass_accurate_guest = s[3]

            if '>Навесы<' in s:
                s = download_report_processing_mainstatistic4(s, lines[i])
                bend_home = s[0]
                bend_accurate_home = s[1]
                bend_guest = s[2]
                bend_accurate_guest = s[3]

            if '>Дриблинг<' in s:
                s = download_report_processing_mainstatistic4(s, lines[i])
                dribbling_home = s[0]
                dribbling_successful_home = s[1]
                dribbling_guest = s[2]
                dribbling_successful_guest = s[3]

            if '>Отбор<' in s:
                s = download_report_processing_mainstatistic4(s, lines[i])
                tackle_home = s[0]
                tackle_successful_home = s[1]
                tackle_guest = s[2]
                tackle_successful_guest = s[3]

            if '>Верховые единоборства<' in s:
                s = download_report_processing_mainstatistic4(s, lines[i])
                height_fight_home = s[0]
                height_fight_successful_home = s[1]
                height_fight_guest = s[2]
                height_fight_successful_guest = s[3]

            if '>Перехваты<' in s:
                s = download_report_processing_mainstatistic2(s, lines[i])
                intercept_home = s[0]
                intercept_guest = s[1]

            if '>Потери<' in s:
                s = download_report_processing_mainstatistic2(s, lines[i])
                turnover_home = s[0]
                turnover_guest = s[1]

            if '>Нарушения (пенальти)<' in s:
                s = download_report_processing_mainstatistic4(s, lines[i])
                foul_home = s[0]
                penalty_home = s[1]
                foul_guest = s[2]
                penalty_guest = s[3]

            if '>Штрафные' in s:
                s = download_report_processing_mainstatistic8(s, lines[i])
                freekick_home = s[0]
                freekick_cross_home = s[1]
                freekick_kick_home = s[2]
                freekick_playout_home = s[3]
                freekick_guest = s[4]
                freekick_cross_guest = s[5]
                freekick_kick_guest = s[6]
                freekick_playout_guest = s[7]

        # print(city, stadium, viewers, wheater, arbitr, minutes)
        # print(team_home, team_guest, goals_home, goals_guest, manager_home, manager_guest)
        # print(kick_home, kick_guest, kick_target_home, kick_target_guest)
        # print(goalpost_home, offside_home, goalpost_guest, offside_guest)
        # print(corner_home, corner_guest, corner_cross_home, corner_cross_guest, corner_playout_home,
        #       corner_playout_guest)
        # print(possession_home, possession_guest)
        # print(kick_near_home, kick_near_guest, kick_near_target_home, kick_near_target_guest)
        # print(kick_far_home, kick_far_guest, kick_far_target_home, kick_far_target_guest)
        # print(kick_blocked_home, kick_blocked_guest)
        # print(pass_home, pass_guest, pass_accurate_home, pass_accurate_guest)
        # print(bend_home, bend_guest, bend_accurate_home, bend_accurate_guest)
        # print(dribbling_home, dribbling_guest, dribbling_successful_home, dribbling_successful_guest)
        # print(tackle_home, tackle_guest, tackle_successful_home, tackle_successful_guest)
        # print(height_fight_home, height_fight_guest, height_fight_successful_home, height_fight_successful_guest)
        # print(intercept_home, intercept_guest)
        # print(turnover_home, turnover_guest)
        # print(foul_home, foul_guest, penalty_home, penalty_guest)
        # print(freekick_home, freekick_guest, freekick_cross_home, freekick_cross_guest, freekick_kick_home,
        #       freekick_kick_guest, freekick_playout_home, freekick_playout_guest)

        # ссылка на тур
        try:
            gametext_id = GamesText.objects.get(id=d.id)
        except Exception:
            gametext_id = None

        info_for_adding.append([gametext_id, city, stadium, viewers, wheater, arbitr, minutes,
                                team_home, team_guest, goals_home, goals_guest, manager_home, manager_guest,
                                kick_home, kick_guest, kick_target_home, kick_target_guest,
                                goalpost_home, offside_home, goalpost_guest, offside_guest,
                                corner_home, corner_guest, corner_cross_home, corner_cross_guest, corner_playout_home,
                                corner_playout_guest,
                                possession_home, possession_guest,
                                kick_near_home, kick_near_guest, kick_near_target_home, kick_near_target_guest,
                                kick_far_home, kick_far_guest, kick_far_target_home, kick_far_target_guest,
                                kick_blocked_home, kick_blocked_guest,
                                pass_home, pass_guest, pass_accurate_home, pass_accurate_guest,
                                bend_home, bend_guest, bend_accurate_home, bend_accurate_guest,
                                dribbling_home, dribbling_guest, dribbling_successful_home, dribbling_successful_guest,
                                tackle_home, tackle_guest, tackle_successful_home, tackle_successful_guest,
                                height_fight_home, height_fight_guest, height_fight_successful_home,
                                height_fight_successful_guest,
                                intercept_home, intercept_guest,
                                turnover_home, turnover_guest,
                                foul_home, foul_guest, penalty_home, penalty_guest,
                                freekick_home, freekick_guest, freekick_cross_home, freekick_cross_guest,
                                freekick_kick_home,
                                freekick_kick_guest, freekick_playout_home, freekick_playout_guest])

        if count // 100 == count / 100:
            print(count, 'из', count_all)

        if count // 100 == count / 100:
            # Добавляем их
            GamesTextReport_Main.objects.bulk_create(
                GamesTextReport_Main(

                    gametext=gametext_id, city=city, stadium=stadium, viewers=viewers, wheater=wheater,
                    arbitr=arbitr, minutes=minutes,
                    team_home=team_home, team_guest=team_guest, goals_home=goals_home, goals_guest=goals_guest,
                    manager_home=manager_home, manager_guest=manager_guest,
                    kick_home=kick_home, kick_guest=kick_guest, kick_target_home=kick_target_home,
                    kick_target_guest=kick_target_guest,
                    goalpost_home=goalpost_home,
                    offside_home=offside_home, goalpost_guest=goalpost_guest, offside_guest=offside_guest,
                    corner_home=corner_home, corner_guest=corner_guest, corner_cross_home=corner_cross_home,
                    corner_cross_guest=corner_cross_guest, corner_playout_home=corner_playout_home,
                    corner_playout_guest=corner_playout_guest,
                    possession_home=possession_home, possession_guest=possession_guest,
                    kick_near_home=kick_near_home, kick_near_guest=kick_near_guest,
                    kick_near_target_home=kick_near_target_home, kick_near_target_guest=kick_near_target_guest,
                    kick_far_home=kick_far_home, kick_far_guest=kick_far_guest,
                    kick_far_target_home=kick_far_target_home, kick_far_target_guest=kick_far_target_guest,
                    kick_blocked_home=kick_blocked_home, kick_blocked_guest=kick_blocked_guest,
                    pass_home=pass_home, pass_guest=pass_guest, pass_accurate_home=pass_accurate_home,
                    pass_accurate_guest=pass_accurate_guest,
                    bend_home=bend_home, bend_guest=bend_guest, bend_accurate_home=bend_accurate_home,
                    bend_accurate_guest=bend_accurate_guest,
                    dribbling_home=dribbling_home, dribbling_guest=dribbling_guest,
                    dribbling_successful_home=dribbling_successful_home,
                    dribbling_successful_guest=dribbling_successful_guest,
                    tackle_home=tackle_home, tackle_guest=tackle_guest, tackle_successful_home=tackle_successful_home,
                    tackle_successful_guest=tackle_successful_guest,
                    height_fight_home=height_fight_home, height_fight_guest=height_fight_guest,
                    height_fight_successful_home=height_fight_successful_home,
                    height_fight_successful_guest=height_fight_successful_guest,
                    intercept_home=intercept_home, intercept_guest=intercept_guest,
                    turnover_home=turnover_home, turnover_guest=turnover_guest,
                    foul_home=foul_home, foul_guest=foul_guest, penalty_home=penalty_home, penalty_guest=penalty_guest,
                    freekick_home=freekick_home, freekick_guest=freekick_guest, freekick_cross_home=freekick_cross_home,
                    freekick_cross_guest=freekick_cross_guest,
                    freekick_kick_home=freekick_kick_home,
                    freekick_kick_guest=freekick_kick_guest, freekick_playout_home=freekick_playout_home,
                    freekick_playout_guest=freekick_playout_guest

                ) for

                gametext_id, city, stadium, viewers, wheater, arbitr, minutes,
                team_home, team_guest, goals_home, goals_guest, manager_home, manager_guest,
                kick_home, kick_guest, kick_target_home, kick_target_guest,
                goalpost_home, offside_home, goalpost_guest, offside_guest,
                corner_home, corner_guest, corner_cross_home, corner_cross_guest, corner_playout_home,
                corner_playout_guest,
                possession_home, possession_guest,
                kick_near_home, kick_near_guest, kick_near_target_home, kick_near_target_guest,
                kick_far_home, kick_far_guest, kick_far_target_home, kick_far_target_guest,
                kick_blocked_home, kick_blocked_guest,
                pass_home, pass_guest, pass_accurate_home, pass_accurate_guest,
                bend_home, bend_guest, bend_accurate_home, bend_accurate_guest,
                dribbling_home, dribbling_guest, dribbling_successful_home, dribbling_successful_guest,
                tackle_home, tackle_guest, tackle_successful_home, tackle_successful_guest,
                height_fight_home, height_fight_guest, height_fight_successful_home,
                height_fight_successful_guest,
                intercept_home, intercept_guest,
                turnover_home, turnover_guest,
                foul_home, foul_guest, penalty_home, penalty_guest,
                freekick_home, freekick_guest, freekick_cross_home, freekick_cross_guest,
                freekick_kick_home,
                freekick_kick_guest, freekick_playout_home, freekick_playout_guest
                in info_for_adding)
            info_for_adding = []

        # if count > 5:
        #     break

    # Добавляем оставшиеся
    GamesTextReport_Main.objects.bulk_create(
        GamesTextReport_Main(

            gametext=gametext_id, city=city, stadium=stadium, viewers=viewers, wheater=wheater,
            arbitr=arbitr, minutes=minutes,
            team_home=team_home, team_guest=team_guest, goals_home=goals_home, goals_guest=goals_guest,
            manager_home=manager_home, manager_guest=manager_guest,
            kick_home=kick_home, kick_guest=kick_guest, kick_target_home=kick_target_home,
            kick_target_guest=kick_target_guest,
            goalpost_home=goalpost_home,
            offside_home=offside_home, goalpost_guest=goalpost_guest, offside_guest=offside_guest,
            corner_home=corner_home, corner_guest=corner_guest, corner_cross_home=corner_cross_home,
            corner_cross_guest=corner_cross_guest, corner_playout_home=corner_playout_home,
            corner_playout_guest=corner_playout_guest,
            possession_home=possession_home, possession_guest=possession_guest,
            kick_near_home=kick_near_home, kick_near_guest=kick_near_guest,
            kick_near_target_home=kick_near_target_home, kick_near_target_guest=kick_near_target_guest,
            kick_far_home=kick_far_home, kick_far_guest=kick_far_guest,
            kick_far_target_home=kick_far_target_home, kick_far_target_guest=kick_far_target_guest,
            kick_blocked_home=kick_blocked_home, kick_blocked_guest=kick_blocked_guest,
            pass_home=pass_home, pass_guest=pass_guest, pass_accurate_home=pass_accurate_home,
            pass_accurate_guest=pass_accurate_guest,
            bend_home=bend_home, bend_guest=bend_guest, bend_accurate_home=bend_accurate_home,
            bend_accurate_guest=bend_accurate_guest,
            dribbling_home=dribbling_home, dribbling_guest=dribbling_guest,
            dribbling_successful_home=dribbling_successful_home,
            dribbling_successful_guest=dribbling_successful_guest,
            tackle_home=tackle_home, tackle_guest=tackle_guest, tackle_successful_home=tackle_successful_home,
            tackle_successful_guest=tackle_successful_guest,
            height_fight_home=height_fight_home, height_fight_guest=height_fight_guest,
            height_fight_successful_home=height_fight_successful_home,
            height_fight_successful_guest=height_fight_successful_guest,
            intercept_home=intercept_home, intercept_guest=intercept_guest,
            turnover_home=turnover_home, turnover_guest=turnover_guest,
            foul_home=foul_home, foul_guest=foul_guest, penalty_home=penalty_home, penalty_guest=penalty_guest,
            freekick_home=freekick_home, freekick_guest=freekick_guest, freekick_cross_home=freekick_cross_home,
            freekick_cross_guest=freekick_cross_guest,
            freekick_kick_home=freekick_kick_home,
            freekick_kick_guest=freekick_kick_guest, freekick_playout_home=freekick_playout_home,
            freekick_playout_guest=freekick_playout_guest

        ) for

        gametext_id, city, stadium, viewers, wheater, arbitr, minutes,
        team_home, team_guest, goals_home, goals_guest, manager_home, manager_guest,
        kick_home, kick_guest, kick_target_home, kick_target_guest,
        goalpost_home, offside_home, goalpost_guest, offside_guest,
        corner_home, corner_guest, corner_cross_home, corner_cross_guest, corner_playout_home,
        corner_playout_guest,
        possession_home, possession_guest,
        kick_near_home, kick_near_guest, kick_near_target_home, kick_near_target_guest,
        kick_far_home, kick_far_guest, kick_far_target_home, kick_far_target_guest,
        kick_blocked_home, kick_blocked_guest,
        pass_home, pass_guest, pass_accurate_home, pass_accurate_guest,
        bend_home, bend_guest, bend_accurate_home, bend_accurate_guest,
        dribbling_home, dribbling_guest, dribbling_successful_home, dribbling_successful_guest,
        tackle_home, tackle_guest, tackle_successful_home, tackle_successful_guest,
        height_fight_home, height_fight_guest, height_fight_successful_home,
        height_fight_successful_guest,
        intercept_home, intercept_guest,
        turnover_home, turnover_guest,
        foul_home, foul_guest, penalty_home, penalty_guest,
        freekick_home, freekick_guest, freekick_cross_home, freekick_cross_guest,
        freekick_kick_home,
        freekick_kick_guest, freekick_playout_home, freekick_playout_guest
        in info_for_adding)

    # data = {}
    # return render(request, 'fill_index.html', data)


def download_report_players_processing(request, season):
    # country = 'Австралия'
    # division = 'Хёндай А-Лига'
    games_list = GamesText.objects.filter(gamestextreport_player__isnull=True, tur__season__number=season)
    # games_list = GamesText.objects.filter(tur__div__chemp__name__iexact=country).filter(tur__div__name__iexact=division).filter(id=174680)
    # games_list = GamesText.objects.filter(id=174680)

    # games_list = GamesTextReport.objects.all()
    print('Всего матчей =', len(games_list))

    info_for_adding = []

    count = 0
    count_all = len(games_list)

    # очищаем матчи
    # GamesTextReport_Player.objects.all().delete()

    info_for_adding = []

    for d in games_list:
        count += 1

        # if d.id != 65565:
        #     # print(d.link)
        #     continue

        chemp_name = d.tur.div.chemp.name
        division_name = d.tur.div.name

        directory = 'F:/Github/peflstat/download/' + season + '/' + chemp_name + '/' + division_name
        with open(directory + '/' + str(d.id)) as f:
            file = html.document_fromstring(f.read())

        with open(directory + '/' + str(d.id)) as f:
            lines = f.read().splitlines()

        for s in lines:
            # Минут в матче
            if 'удья добав' in s or 'К основному времени' in s or 'добавляет к' in s:
                minutes_all = 90 + only_digit(s)

            if 'Финальный свисток' in s:
                s_html = html.document_fromstring(s)
                s_tags_b = s_html.xpath('//b')

                team_home = s_tags_b[0].text_content().strip()
                team_guest = s_tags_b[2].text_content().strip()
                break

        # ссылка на тур
        try:
            gametext_id = GamesText.objects.get(id=d.id)
        except Exception:
            gametext_id = None

        for i in range(36):
            number = ('0' + str(i + 1))[-2:]
            id = "//td[@id='pl" + number + "']"
            td = file.xpath(id)[0]

            s = str(html.tostring(td))
            j = s.find('<a id="p')
            s = s[j + 8:]
            player_id = int(s.split('"')[0])

            name = td.text_content().strip()
            if '(к)' in name:
                capitan = 1
            else:
                capitan = 0

            if '(T)' in name:
                trauma = 1
            else:
                trauma = 0

            name = name.replace("(к)", "").replace("(T)", "")

            minutes_s = td.getnext().text_content().strip().replace('(', '').split(')')

            if len(minutes_s) == 1:
                minutes = 0
            elif len(minutes_s) > 2:
                minutes = int(minutes_s[0]) - int(minutes_s[1]) + 1
            else:
                minutes = int(minutes_s[0])

            # minutes = get_object_without_bracket(td.getnext().text_content().strip().replace('(', '').replace(')', ''))

            if i < 18:
                home = 1
                team = team_home
            else:
                home = 0
                team = team_guest

            if (i < 11) or (i > 17 and i < 29):
                basis = 1
                if minutes == 0:
                    minutes = minutes_all
            else:
                basis = 0
                if minutes != 0:
                    minutes = minutes_all - minutes + 1

            card = str(html.tostring(td.getnext().getnext()))
            if 'r.gif' in card:
                card = 'red'
            elif 'y.gif' in card:
                card = 'yellow'
            else:
                card = ''
            try:
                rating = float(td.getnext().getnext().text_content().strip())
            except:
                rating = 0

            stat_kick0 = get_object_from_bracket(td.getnext().getnext().getnext().text_content().strip())
            stat_shtanga = get_object_without_bracket(td.getnext().getnext().getnext().getnext().text_content().strip())
            stat_offside = get_object_without_bracket(
                td.getnext().getnext().getnext().getnext().getnext().text_content().strip())
            stat_kick_far0 = get_object_from_bracket(
                td.getnext().getnext().getnext().getnext().getnext().getnext().text_content().strip())
            stat_head0 = get_object_from_bracket(
                td.getnext().getnext().getnext().getnext().getnext().getnext().getnext().text_content().strip())
            stat_block = get_object_without_bracket(
                td.getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().text_content().strip())
            stat_pass0 = get_object_from_bracket(
                td.getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().text_content().strip())
            stat_cross0 = get_object_from_bracket(
                td.getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().text_content().strip())
            stat_dribbling0 = get_object_from_bracket(
                td.getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().
                    getnext().text_content().strip())
            stat_tackle0 = get_object_from_bracket(
                td.getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().
                    getnext().getnext().text_content().strip())
            stat_up0 = get_object_from_bracket(
                td.getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().
                    getnext().getnext().getnext().text_content().strip())
            stat_perehvat = get_object_without_bracket(
                td.getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().
                    getnext().getnext().getnext().getnext().text_content().strip())
            stat_poter = get_object_without_bracket(
                td.getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().
                    getnext().getnext().getnext().getnext().getnext().text_content().strip())
            stat_foul = get_object_without_bracket(
                td.getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().
                    getnext().getnext().getnext().getnext().getnext().getnext().text_content().strip())
            stat_foul_him = get_object_without_bracket(
                td.getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().
                    getnext().getnext().getnext().getnext().getnext().getnext().getnext().text_content().strip())
            stat_save0 = get_object_from_bracket(
                td.getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().
                    getnext().getnext().getnext().getnext().getnext().getnext().getnext().getnext().text_content().strip())

            im = str(html.tostring(td))

            if '<font color="red">' in im.replace('<font color=red><b>T</b>', '').replace('<font color="red"><b>T</b></font>', ''):
                im = 1
            else:
                im = 0

            count_find = int(file.xpath('count(//font[@class="p' + number + '"])'))

            if rating > 0:
                number = i + 1
                stat_kick = stat_kick0[0]
                stat_kick_ok = stat_kick0[1]
                stat_kick_far = stat_kick_far0[0]
                stat_kick_far_ok = stat_kick_far0[1]
                stat_head = stat_head0[0]
                stat_head_ok = stat_head0[1]
                stat_pass = stat_pass0[0]
                stat_pass_ok = stat_pass0[1]
                stat_cross = stat_cross0[0]
                stat_cross_ok = stat_cross0[1]
                stat_dribbling = stat_dribbling0[0]
                stat_dribbling_ok = stat_dribbling0[1]
                stat_tackle = stat_tackle0[0]
                stat_tackle_ok = stat_tackle0[1]
                stat_up = stat_up0[0]
                stat_up_ok = stat_up0[1]
                stat_save = stat_save0[0]
                stat_save_ok = stat_save0[1]

                info_for_adding.append([gametext_id, number, name, rating, minutes, card,
                                        capitan, im, count_find, stat_kick, stat_kick_ok, stat_shtanga, stat_offside,
                                        stat_kick_far, stat_kick_far_ok, stat_head, stat_head_ok,
                                        stat_block, stat_pass, stat_pass_ok, stat_cross,
                                        stat_cross_ok, stat_dribbling, stat_dribbling_ok, stat_tackle,
                                        stat_tackle_ok, stat_up, stat_up_ok, stat_perehvat,
                                        stat_poter, stat_foul, stat_foul_him, stat_save, stat_save_ok,
                                        team, player_id, home, trauma, basis])

        #     break
        #
        # break

        if count // 10 == count / 10:
            print(count, 'из', count_all)

        if count // 10 == count / 10:
            # Добавляем их

            GamesTextReport_Player.objects.bulk_create(
                GamesTextReport_Player(

                    gametext=gametext_id, number=number, name=name, rating=rating, minutes=minutes, card=card,
                    capitan=capitan, im=im, count_find=count_find, stat_kick=stat_kick, stat_kick_ok=stat_kick_ok,
                    stat_shtanga=stat_shtanga, stat_offside=stat_offside, stat_kick_far=stat_kick_far,
                    stat_kick_far_ok=stat_kick_far_ok, stat_head=stat_head, stat_head_ok=stat_head_ok,
                    stat_block=stat_block, stat_pass=stat_pass, stat_pass_ok=stat_pass_ok, stat_cross=stat_cross,
                    stat_cross_ok=stat_cross_ok, stat_dribbling=stat_dribbling, stat_dribbling_ok=stat_dribbling_ok,
                    stat_tackle=stat_tackle, stat_tackle_ok=stat_tackle_ok, stat_up=stat_up,
                    stat_up_ok=stat_up_ok, stat_perehvat=stat_perehvat, stat_poter=stat_poter, stat_foul=stat_foul,
                    stat_foul_him=stat_foul_him, stat_save=stat_save, stat_save_ok=stat_save_ok,
                    team=team, player_id=player_id, home=home, trauma=trauma, basis=basis

                ) for
                gametext_id, number, name, rating, minutes, card, capitan, im, count_find, stat_kick, stat_kick_ok, stat_shtanga,
                stat_offside, stat_kick_far, stat_kick_far_ok, stat_head, stat_head_ok, stat_block, stat_pass,
                stat_pass_ok, stat_cross, stat_cross_ok, stat_dribbling, stat_dribbling_ok, stat_tackle, stat_tackle_ok, stat_up, stat_up_ok,
                stat_perehvat, stat_poter, stat_foul, stat_foul_him, stat_save, stat_save_ok,
                team, player_id, home, trauma, basis in info_for_adding)

            info_for_adding = []

    # Добавляем оставшиеся
    GamesTextReport_Player.objects.bulk_create(
        GamesTextReport_Player(

            gametext=gametext_id, number=number, name=name, rating=rating, minutes=minutes, card=card,
            capitan=capitan, im=im, count_find=count_find, stat_kick=stat_kick, stat_kick_ok=stat_kick_ok,
            stat_shtanga=stat_shtanga, stat_offside=stat_offside, stat_kick_far=stat_kick_far,
            stat_kick_far_ok=stat_kick_far_ok, stat_head=stat_head, stat_head_ok=stat_head_ok,
            stat_block=stat_block, stat_pass=stat_pass, stat_pass_ok=stat_pass_ok, stat_cross=stat_cross,
            stat_cross_ok=stat_cross_ok, stat_dribbling=stat_dribbling, stat_dribbling_ok=stat_dribbling_ok,
            stat_tackle=stat_tackle, stat_tackle_ok=stat_tackle_ok, stat_up=stat_up,
            stat_up_ok=stat_up_ok, stat_perehvat=stat_perehvat, stat_poter=stat_poter, stat_foul=stat_foul,
            stat_foul_him=stat_foul_him, stat_save=stat_save, stat_save_ok=stat_save_ok,
            team=team, player_id=player_id, home=home, trauma=trauma, basis=basis

        ) for
        gametext_id, number, name, rating, minutes, card, capitan, im, count_find, stat_kick, stat_kick_ok, stat_shtanga,
        stat_offside, stat_kick_far, stat_kick_far_ok, stat_head, stat_head_ok, stat_block, stat_pass,
        stat_pass_ok, stat_cross, stat_cross_ok, stat_dribbling, stat_dribbling_ok, stat_tackle, stat_tackle_ok, stat_up, stat_up_ok,
        stat_perehvat, stat_poter, stat_foul, stat_foul_him, stat_save, stat_save_ok,
        team, player_id, home, trauma, basis in info_for_adding)


def download_report_goals_processing(request, season):
    # country = 'Украина'
    # division = 'Первая лига'
    games_list = GamesText.objects.filter(gamestextreport_goals__isnull=True, tur__season__number=season)
    # games_list = GamesText.objects.filter(tur__div__chemp__name__iexact=country).filter(tur__div__name__iexact=division)
    # games_list = GamesText.objects.filter(tur__div__chemp__name__iexact=country)

    # games_list = GamesTextReport.objects.all()
    print('Всего матчей =', len(games_list))

    info_for_adding = []

    count = 0
    count_all = len(games_list)

    # очищаем матчи
    # GamesTextReport_Goals.objects.all().delete()

    info_for_adding = []
    foul_array = []

    for d in games_list:
        count += 1

        # if d.id != 96619:
        #     # print(d.link)
        #     continue
        # print(d.link)

        chemp_name = d.tur.div.chemp.name
        division_name = d.tur.div.name

        directory = 'F:/Github/peflstat/download/' + season + '/' + chemp_name + '/' + division_name
        with open(directory + '/' + str(d.id)) as f:
            file = html.document_fromstring(f.read())

        with open(directory + '/' + str(d.id)) as f:
            lines = f.read().splitlines()

        for s in lines:
            if 'Финальный свисток' in s:
                s_html = html.document_fromstring(s)
                s_tags_b = s_html.xpath('//b')

                team_home = s_tags_b[0].text_content().strip()
                team_guest = s_tags_b[2].text_content().strip()
                # print(team_home, team_guest)
                break

        # ссылка на тур
        try:
            gametext_id = GamesText.objects.get(id=d.id)
        except Exception:
            gametext_id = None

        allgoals = file.xpath("//*[contains(text(), 'Голы:')]")

        i = 0
        for team_goal in allgoals:
            i += 1
            s = str(html.tostring(team_goal, encoding="unicode")).replace('<br></font>', '').replace('</font>', '')
            t = 'Голы:<br>'
            s = s[s.find(t) + len(t):]

            if s != 'нет':
                if '<br>' in s:
                    goals = s.split('<br>')
                else:
                    goals = [s]

                for goal in goals:
                    minutes = only_digit(goal)
                    if i == 1:
                        home = 1
                        team = team_home
                    else:
                        home = 0
                        team = team_guest

                    if '(a)' in goal or '(a)' in goal:
                        goal = goal.replace('(a)', '')
                        own_goal = 1
                    else:
                        own_goal = 0

                    if '(п)' in goal:
                        goal = goal.replace('(п)', '')
                        penalty = 1
                    else:
                        penalty = 0

                    goal = remove_digit(goal).strip()
                    if '(' in goal:
                        goal = goal.split('(')
                        player_goal = goal[0]
                        player_pass = goal[1].replace(')', '')
                    else:
                        player_goal = goal
                        player_pass = ''

                    if '(' in player_goal:
                        foul_array.append(d.id)
                    if '(' in player_pass:
                        foul_array.append(d.id)
                        # print(d.id, home, minute, team, player_goal, player_pass, own_goal)

                    info_for_adding.append(
                        [gametext_id, home, minutes, team, player_goal, player_pass, own_goal, penalty])

        if count // 10 == count / 10:
            print(count, 'из', count_all)

        if count // 10 == count / 10:
            # Добавляем их

            GamesTextReport_Goals.objects.bulk_create(
                GamesTextReport_Goals(

                    gametext=gametext_id, home=home, minutes=minutes, team=team, player_goal=player_goal,
                    player_pass=player_pass, own_goal=own_goal, penalty=penalty

                ) for
                gametext_id, home, minutes, team, player_goal, player_pass, own_goal, penalty in info_for_adding)

            info_for_adding = []

    # Добавляем оставшиеся
    GamesTextReport_Goals.objects.bulk_create(
        GamesTextReport_Goals(

            gametext=gametext_id, home=home, minutes=minutes, team=team, player_goal=player_goal,
            player_pass=player_pass, own_goal=own_goal, penalty=penalty

        ) for
        gametext_id, home, minutes, team, player_goal, player_pass, own_goal, penalty in info_for_adding)

    # print(info_for_adding)


def update_stat(request, season):
#     # country = 'Украина'
#     # division = 'Первая лига'
#     # .filter(gametext__tur__number__lte=2)
#     # .filter(gametext__tur__div__chemp__name__iexact=country).filter(gametext__tur__div__name__iexact=division)
#
    # ссылка на сезон
    try:
        season_id = Season.objects.get(number=season)
    except Exception:
        season_id = None
    #
    # список команд
    team_list_home = GamesTextReport_Main.objects.values_list(
        "gametext__tur__div", "gametext__tur__season", "team_home").filter(gametext__tur__season__number=season)
    team_list_guest = GamesTextReport_Main.objects.values_list(
        "gametext__tur__div", "gametext__tur__season", "team_guest").filter(gametext__tur__season__number=season)
    team_list = set(chain(team_list_home, team_list_guest))

    info_for_adding = []
    for team in team_list:
        try:
            div_id = Divs.objects.get(id=team[0])
        except Exception:
            div_id = None
        info_for_adding.append([div_id, season_id, team[2]])

    Stat_Team_List.objects.all().delete()
    Stat_Team_List.objects.bulk_create(
        Stat_Team_List(div=div, season=season, name=name) for div, season, name in info_for_adding)

    print("Список команд =", str(len(Stat_Team_List.objects.all())))

    # список игроков, забивших гол
    players_list_goal = set(GamesTextReport_Goals.objects.values_list(
        "gametext__tur__div", "gametext__tur__season", "player_goal", "team").filter(
        gametext__tur__season__number=season).exclude(own_goal=1))

    info_for_adding = []
    count = 0
    count_all = len(players_list_goal)
    for team in players_list_goal:
        count += 1
        try:
            div_id = Divs.objects.get(id=team[0])
        except Exception:
            div_id = None
        info_for_adding.append([div_id, season_id, team[2], team[3]])
        if count / 200 == count // 200:
            print("Список игроков, забивших гол.", count, 'из', count_all)

    Stat_Players_List_Goal.objects.all().delete()
    Stat_Players_List_Goal.objects.bulk_create(
        Stat_Players_List_Goal(div=div, season=season, name=name, team=team) for div, season, name, team in
        info_for_adding)

    print("Список игроков, забивших гол =", str(len(Stat_Players_List_Goal.objects.all())))

    # список игроков, отдавших пас
    players_list_pass = set(GamesTextReport_Goals.objects.values_list(
        "gametext__tur__div", "gametext__tur__season", "player_pass", "team").filter(
        gametext__tur__season__number=season).exclude(player_pass__isnull=True).exclude(player_pass=""))

    info_for_adding = []
    count = 0
    count_all = len(players_list_pass)
    for team in players_list_pass:
        count += 1
        try:
            div_id = Divs.objects.get(id=team[0])
        except Exception:
            div_id = None
        info_for_adding.append([div_id, season_id, team[2], team[3]])
        if count / 200 == count // 200:
            print("Список игроков, отдавших пас.", count, 'из', count_all)

    Stat_Players_List_Pass.objects.all().delete()
    Stat_Players_List_Pass.objects.bulk_create(
        Stat_Players_List_Pass(div=div, season=season, name=name, team=team) for div, season, name, team in
        info_for_adding)

    print("Список игроков, отдавших пас =", str(len(Stat_Players_List_Pass.objects.all())))

    players_list_goal_and_pass = set(chain(players_list_goal, players_list_pass))

    info_for_adding = []
    count = 0
    count_all = len(players_list_goal_and_pass)
    for team in players_list_goal_and_pass:
        count += 1
        try:
            div_id = Divs.objects.get(id=team[0])
        except Exception:
            div_id = None
        info_for_adding.append([div_id, season_id, team[2], team[3]])
        if count / 200 == count // 200:
            print("Список игроков, забивших гол или отдавших пас.", count, 'из', count_all)

    Stat_Players_List_GoalAndPass.objects.all().delete()
    Stat_Players_List_GoalAndPass.objects.bulk_create(
        Stat_Players_List_GoalAndPass(div=div, season=season, name=name, team=team) for div, season, name, team in
        info_for_adding)

    print("Список игроков, забивших гол или отдавших пас =", str(len(Stat_Players_List_GoalAndPass.objects.all())))

    # список команд и номер последних 5 туров

    Stat_Players_PlayedMaxTime_List_MinTur.objects.all().delete()
    cursor = connection.cursor()
    sql = "insert into fill_stat_players_playedmaxtime_list_mintur (timestamp, season_id, div_id, number, team) select \
    datetime() \
    ,season_id \
    ,div_id \
    ,max(number) number \
    ,team \
from ( \
select \
    turs.season_id \
    ,turs.div_id \
    ,max(turs.number) number \
    ,main.team_guest team \
from fill_turs turs \
inner join fill_season season on season.id = turs.season_id \
inner join fill_gamestext g on g.tur_id = turs.id \
inner join fill_gamestextreport_main main on main.gametext_id = g.id \
where season.number = " + season + " \
group by \
    turs.season_id \
    ,turs.div_id \
    ,main.team_guest \
\
union all \
\
select \
    turs.season_id \
    ,turs.div_id \
    ,max(turs.number) number \
    ,main.team_home team \
from fill_turs turs \
inner join fill_season season on season.id = turs.season_id \
inner join fill_gamestext g on g.tur_id = turs.id \
inner join fill_gamestextreport_main main on main.gametext_id = g.id \
where season.number = " + season + " \
group by \
    turs.season_id \
    ,turs.div_id \
    ,main.team_guest \
) s \
group by \
    season_id \
    ,div_id \
    ,team \
"
    cursor.execute(sql)
    transaction.commit()

    print("Список команд =", str(len(Stat_Players_PlayedMaxTime_List_MinTur.objects.all())))

    # список игроков, которые играли в последних 5 туров

    Stat_Players_PlayedMaxTime_List.objects.all().delete()
    cursor = connection.cursor()
    sql = "insert into fill_Stat_Players_PlayedMaxTime_List (timestamp, div_id, season_id, name, team, player_id, number) select \
            datetime() \
            ,t.div_id \
            ,t.season_id \
            ,p.name \
            ,t.team \
            ,p.player_id \
            ,turs.number \
from fill_Stat_Players_PlayedMaxTime_List_MinTur t  \
inner join fill_season season on season.id = t.season_id  \
inner join fill_gamestextreport_player p on p.team = t.team and ifnull(p.rating, 0.0) <> 0.0  \
inner join fill_gamestext g on g.id = p.gametext_id  \
inner join fill_turs turs on turs.id = g.tur_id and turs.number >= (t.number - 4)  \
where season.number = " + season + " \
    "
    cursor.execute(sql)
    transaction.commit()

    print("Список игроков =", str(len(Stat_Players_PlayedMaxTime_List.objects.all())))

    # статистика игроков, которые играли в последних 5 турах

    Stat_Players_PlayedMaxTime.objects.all().delete()

    sql = "insert into fill_Stat_Players_PlayedMaxTime (timestamp, \
        div_id, season_id, name, team, player_id, goal, pases, played, number_in_team, rating \
        , minutes, card, capitan, im, basis, count_find, stat_kick, stat_kick_ok, stat_kick_no, stat_shtanga, stat_offside, stat_kick_far \
        , stat_kick_far_ok, stat_kick_far_no, stat_head, stat_head_ok, stat_head_no, stat_block, stat_pass, stat_pass_ok, stat_pass_no \
        , stat_cross, stat_cross_ok, stat_cross_no, stat_dribbling, stat_dribbling_ok, stat_dribbling_no, stat_tackle, stat_tackle_ok \
        , stat_tackle_no, stat_up, stat_up_ok, stat_up_no, stat_perehvat, stat_poter, stat_foul, stat_foul_him, stat_save, stat_save_ok, stat_save_no) \
            select \
                datetime() \
                ,t.div_id \
                ,t.season_id \
                ,p.name \
                ,t.team \
                ,t.player_id \
                ,0 goal \
                ,0 pases \
                ,count(rating) played \
                ,sum(case when p.home = 1 then p.number else p.number - 18 end) / cast(count(p.rating) as float) number_in_team \
                ,round(sum(rating * minutes)/sum(minutes), 2) \
                ,sum(minutes) \
                ,sum(card) \
                ,sum(capitan) \
                ,sum(im) \
                ,sum(basis) \
                ,sum(count_find) \
                ,sum(stat_kick) \
                ,sum(stat_kick_ok) \
                ,sum(stat_kick)-sum(stat_kick_ok) \
                ,sum(stat_shtanga) \
                ,sum(stat_offside) \
                ,sum(stat_kick_far) \
                ,sum(stat_kick_far_ok) \
                ,sum(stat_kick_far)-sum(stat_kick_far_ok) \
                ,sum(stat_head) \
                ,sum(stat_head_ok) \
                ,sum(stat_head)-sum(stat_head_ok) \
                ,sum(stat_block) \
                ,sum(stat_pass) \
                ,sum(stat_pass_ok) \
                ,sum(stat_pass)-sum(stat_pass_ok) \
                ,sum(stat_cross) \
                ,sum(stat_cross_ok) \
                ,sum(stat_cross)-sum(stat_cross_ok) \
                ,sum(stat_dribbling) \
                ,sum(stat_dribbling_ok) \
                ,sum(stat_dribbling)-sum(stat_dribbling_ok) \
                ,sum(stat_tackle) \
                ,sum(stat_tackle_ok) \
                ,sum(stat_tackle)-sum(stat_tackle_ok) \
                ,sum(stat_up) \
                ,sum(stat_up_ok) \
                ,sum(stat_up)-sum(stat_up_ok) \
                ,sum(stat_perehvat) \
                ,sum(stat_poter) \
                ,sum(stat_foul) \
                ,sum(stat_foul_him) \
                ,sum(stat_save) \
                ,sum(stat_save_ok) \
                ,sum(stat_save)-sum(stat_save_ok) \
 \
from fill_Stat_Players_PlayedMaxTime_List t \
inner join fill_season season on season.id = t.season_id \
inner join fill_gamestextreport_player p on p.team = t.team and p.player_id = t.player_id \
inner join fill_gamestext g on g.id = p.gametext_id \
inner join fill_turs turs on turs.id = g.tur_id and turs.number = t.number \
    where season.number = " + season + " \
    group by \
        t.div_id \
        , t.season_id \
        , p.name \
        , t.team \
        , t.player_id \
        "

    # print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    transaction.commit()

    # голы игроков, которые играли в последних 5 турах

    Stat_Players_PlayedMaxTime_Goals.objects.all().delete()

    sql = "insert into fill_Stat_Players_PlayedMaxTime_Goals (timestamp, div_id, season_id, name, team, player_id, goal) \
    select \
        datetime() \
        ,t.div_id \
        ,t.season_id \
        ,t.name \
        ,t.team \
        ,t.player_id \
        ,count(*) goal \
    from fill_Stat_Players_PlayedMaxTime t \
    inner join fill_Stat_Players_PlayedMaxTime_List t2 on t.team = t2.team and t.player_id = t2.player_id \
    inner join fill_gamestextreport_goals goals on goals.gametext_id = p.gametext_id and t.name = goals.player_goal and goals.own_goal <> 1 \
    inner join fill_season season on season.id = t.season_id \
    inner join fill_gamestextreport_player p on p.team = t.team and p.player_id = t.player_id \
    inner join fill_gamestext g on g.id = p.gametext_id \
    inner join fill_turs turs on turs.id = g.tur_id and turs.number = t2.number \
    where season.number = " + season + " \
    group by \
        t.div_id \
        ,t.season_id \
        ,t.name \
        ,t.team \
        ,t.player_id"

    cursor = connection.cursor()
    cursor.execute(sql)
    transaction.commit()

    print("Голы игроков =", str(len(Stat_Players_PlayedMaxTime_Goals.objects.all())))

    # пасы игроков, которые играли в последних 5 турах

    Stat_Players_PlayedMaxTime_Pass.objects.all().delete()

    sql = "insert into fill_Stat_Players_PlayedMaxTime_Pass (timestamp, div_id, season_id, name, team, player_id, pases) \
    select \
        datetime() \
        ,t.div_id \
        ,t.season_id \
        ,t.name \
        ,t.team \
        ,t.player_id \
        ,count(*) pases \
    from fill_Stat_Players_PlayedMaxTime t \
    inner join fill_Stat_Players_PlayedMaxTime_List t2 on t.team = t2.team and t.player_id = t2.player_id \
    inner join fill_gamestextreport_goals goals on goals.gametext_id = p.gametext_id and t.name = goals.player_pass and length(player_pass) > 0 \
    inner join fill_season season on season.id = t.season_id \
    inner join fill_gamestextreport_player p on p.team = t.team and p.player_id = t.player_id \
    inner join fill_gamestext g on g.id = p.gametext_id \
    inner join fill_turs turs on turs.id = g.tur_id and turs.number = t2.number \
    where season.number = " + season + " \
    group by \
        t.div_id \
        ,t.season_id \
        ,t.name \
        ,t.team \
        ,t.player_id"

    cursor = connection.cursor()
    cursor.execute(sql)
    transaction.commit()

    print("Пасы игроков =", str(len(Stat_Players_PlayedMaxTime_Pass.objects.all())))

    sql = "update fill_Stat_Players_PlayedMaxTime set goal = ( \
         select goal from fill_Stat_Players_PlayedMaxTime_Goals t \
         inner join fill_season season on season.id = t.season_id \
         where season.number = " + season + " \
             and fill_Stat_Players_PlayedMaxTime.div_id = t.div_id \
             and fill_Stat_Players_PlayedMaxTime.season_id = t.season_id \
             and fill_Stat_Players_PlayedMaxTime.team = t.team \
             and fill_Stat_Players_PlayedMaxTime.player_id = t.player_id)"

    cursor = connection.cursor()
    cursor.execute(sql)
    transaction.commit()

    sql = "update fill_Stat_Players_PlayedMaxTime set pases = ( \
         select pases from fill_Stat_Players_PlayedMaxTime_Pass t \
         inner join fill_season season on season.id = t.season_id \
         where season.number = " + season + " \
             and fill_Stat_Players_PlayedMaxTime.div_id = t.div_id \
             and fill_Stat_Players_PlayedMaxTime.season_id = t.season_id \
             and fill_Stat_Players_PlayedMaxTime.team = t.team \
             and fill_Stat_Players_PlayedMaxTime.player_id = t.player_id )"

    cursor = connection.cursor()
    cursor.execute(sql)
    transaction.commit()

    print("Пасы игроков =", str(len(Stat_Players_PlayedMaxTime.objects.all())))

    # статистика игроков

    GamesTextReport_PlayerStat.objects.all().delete()

    sql = "insert into fill_GamesTextReport_PlayerStat (timestamp, \
        player_id, played, goal, pases, rating \
        , capitan, trauma, im, basis, minutes, count_find, stat_kick, stat_kick_ok, stat_offside, stat_kick_far \
        , stat_kick_far_ok, stat_head, stat_head_ok, stat_block, stat_pass, stat_pass_ok \
        , stat_cross, stat_cross_ok, stat_dribbling, stat_dribbling_ok, stat_tackle, stat_tackle_ok \
        , stat_up, stat_up_ok, stat_perehvat, stat_poter, stat_foul, stat_foul_him) \
    select \
        datetime() \
        ,p.player_id \
        ,count(rating) played \
        ,max(goal) goal \
        ,max(pases.pases) pases \
        ,round(sum(rating * minutes) / sum(minutes), 2) \
        ,sum(capitan) capitan \
        ,ifnull(sum(trauma), 0) trauma \
        ,sum(im) im \
        ,sum(basis) basis \
        ,round(sum(p.minutes) / count(rating), 2) minutes \
        ,round(sum(count_find) / count(rating), 2) count_find \
        ,round(sum(stat_kick) / count(rating), 2) stat_kick \
        ,round(sum(stat_kick_ok) / count(rating), 2) stat_kick_ok \
        ,round(sum(stat_offside) / count(rating), 2) stat_offside \
        ,round(sum(stat_kick_far) / count(rating), 2) stat_kick_far \
        ,round(sum(stat_kick_far_ok) / count(rating), 2) stat_kick_far_ok \
        ,round(sum(stat_head) / count(rating), 2) stat_head \
        ,round(sum(stat_head_ok) / count(rating), 2) stat_head_ok \
        ,round(sum(stat_block) / count(rating), 2) stat_block \
        ,round(sum(stat_pass) / count(rating), 2) stat_pass \
        ,round(sum(stat_pass_ok) / count(rating), 2) stat_pass_ok \
        ,round(sum(stat_cross) / count(rating), 2) stat_cross \
        ,round(sum(stat_cross_ok) / count(rating), 2) stat_cross_ok \
        ,round(sum(stat_dribbling) / count(rating), 2) stat_dribbling \
        ,round(sum(stat_dribbling_ok) / count(rating), 2) stat_dribbling_ok \
        ,round(sum(stat_tackle) / count(rating), 2) stat_tackle \
        ,round(sum(stat_tackle_ok) / count(rating), 2) stat_tackle_ok \
        ,round(sum(stat_up) / count(rating), 2) stat_up \
        ,round(sum(stat_up_ok) / count(rating), 2) stat_up_ok \
        ,round(sum(stat_perehvat) / count(rating), 2) stat_perehvat \
        ,round(sum(stat_poter) / count(rating), 2) stat_poter \
        ,round(sum(stat_foul) / count(rating), 2) stat_foul \
        ,round(sum(stat_foul_him) / count(rating), 2) stat_foul_him \
    from fill_gamestextreport_player p \
    inner join fill_gamestext g on g.id = p.gametext_id \
    inner join fill_turs turs on turs.id = g.tur_id \
    inner join fill_season season on season.id = turs.season_id \
    left join ( \
        select \
            player_goal \
            ,team \
            ,count(*) goal \
        from fill_gamestextreport_goals goals \
        where goals.own_goal <> 1 \
        group by \
            player_goal \
            ,team \
    ) goals on goals.player_goal = p.name and goals.team = p.team \
    left join ( \
        select \
            player_pass \
            ,team \
            ,count(*) pases \
        from fill_gamestextreport_goals goals \
        where ifnull(player_pass, '') <> '' \
        group by \
            player_pass \
            ,team \
    ) pases on pases.player_pass = p.name and pases.team = p.team \
    where season.number = " + season + " \
    group by p.player_id"

    # print(sql)

    cursor = connection.cursor()
    cursor.execute(sql)
    transaction.commit()

    print("Игроков =", str(len(GamesTextReport_PlayerStat.objects.all())))

    update_stat_players(request, season)



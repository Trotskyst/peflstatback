from fill.models import *
from django.db.models import Count, Case, When
from fill.functions_pefl import *
from fill.functions import *
import os


def update_GamesTextReport_Player_NameTeam():
    from django.db import connection, transaction

    GamesTextReport_Player_NameTeam.objects.all().delete()
    cursor = connection.cursor()
    cursor.execute(
        "insert into fill_gamestextreport_player_nameteam(timestamp, team, name) select datetime(), team, name from fill_gamestextreport_player")
    transaction.commit()


def update_GamesTextReport_Goal_PlayerGoalTeam():
    from django.db import connection, transaction

    GamesTextReport_Goal_PlayerGoalTeam.objects.all().delete()
    cursor = connection.cursor()
    cursor.execute(
        "insert into fill_gamestextreport_goal_playergoalteam(timestamp, team, name) select datetime(), team, player_goal from fill_gamestextreport_goals")
    transaction.commit()


def update_GamesTextReport_Goal_PlayerPassTeam():
    from django.db import connection, transaction

    GamesTextReport_Goal_PlayerPassTeam.objects.all().delete()
    cursor = connection.cursor()
    cursor.execute(
        "insert into fill_gamestextreport_goal_playerpassteam(timestamp, team, name) select datetime(), team, player_pass from fill_gamestextreport_goals where ifnull(player_pass, '')<>''")
    transaction.commit()


def update_stat_bombarders(season, season_id, players_list):
    """Список борбардиров"""
    info_for_adding = []
    div = 0
    number = 0
    count = 0
    count_all = len(players_list)
    Stat_Players_Bombarders.objects.all().delete()
    start_time = time.time()

    for players in players_list:
        count += 1

        goal = GamesTextReport_Goal_PlayerGoalTeam.objects.filter(team=players.team).filter(name=players.name).count()
        played = GamesTextReport_Player_NameTeam.objects.filter(team=players.team).filter(name=players.name).count()

        if players.div_id == div:
            number += 1
        else:
            number = 1

        try:
            div_id = Divs.objects.get(id=players.div_id)
        except Exception:
            div_id = None

        info_for_adding.append([div_id, season_id, players.team, players.name, goal, played, number])

        if count / 500 == count // 500:
            print("Бомбардиры", count, 'из', count_all, 'Время выполнения -', secondsToStr(time.time() - start_time))
            Stat_Players_Bombarders.objects.bulk_create(
                Stat_Players_Bombarders(div=div, season=season, team=team, name=name, goal=goal, played=played,
                                        number=number)
                for div, season, team, name, goal, played, number in info_for_adding)

            info_for_adding = []

    Stat_Players_Bombarders.objects.bulk_create(
        Stat_Players_Bombarders(div=div, season=season, team=team, name=name, goal=goal, played=played,
                                number=number)
        for div, season, team, name, goal, played, number in info_for_adding)

    print("Список бомбардиров =", str(len(Stat_Players_Bombarders.objects.all())))


def update_stat_pivots(season, season_id, players_list):
    """Список игроков, отдавших пас"""
    info_for_adding = []
    div = 0
    number = 0
    count = 0
    count_all = len(players_list)
    Stat_Players_Pivot.objects.all().delete()
    start_time = time.time()
    for players in players_list:
        count += 1
        pases = GamesTextReport_Goal_PlayerPassTeam.objects.filter(team=players.team).filter(name=players.name).count()
        played = GamesTextReport_Player_NameTeam.objects.filter(team=players.team).filter(name=players.name).count()

        if players.div_id == div:
            number += 1
        else:
            number = 1

        try:
            div_id = Divs.objects.get(id=players.div_id)
        except Exception:
            div_id = None

        info_for_adding.append([div_id, season_id, players.team, players.name, pases, played, number])

        if count / 500 == count // 500:
            print("Отдавшие голевой пас", count, 'из', count_all, 'Время выполнения -',
                  secondsToStr(time.time() - start_time))

            Stat_Players_Pivot.objects.bulk_create(
                Stat_Players_Pivot(div=div, season=season, team=team, name=name, pases=pases, played=played,
                                   number=number)
                for div, season, team, name, pases, played, number in info_for_adding)
            info_for_adding = []

    Stat_Players_Pivot.objects.bulk_create(
        Stat_Players_Pivot(div=div, season=season, team=team, name=name, pases=pases, played=played, number=number)
        for div, season, team, name, pases, played, number in info_for_adding)
    print("Список отдавших пас =", str(len(Stat_Players_Pivot.objects.all())))


def update_stat_goal_and_pass(season, season_id, players_list):
    """Список игроков, забивших гол или отдавших пас"""
    info_for_adding = []
    div = 0
    number = 0
    count = 0
    count_all = len(players_list)
    Stat_Players_GoalAndPass.objects.all().delete()
    start_time = time.time()
    for players in players_list:
        count += 1

        goal = GamesTextReport_Goal_PlayerGoalTeam.objects.filter(team=players.team).filter(name=players.name).count()
        pases = GamesTextReport_Goal_PlayerPassTeam.objects.filter(team=players.team).filter(name=players.name).count()
        played = GamesTextReport_Player_NameTeam.objects.filter(team=players.team).filter(name=players.name).count()

        if players.div_id == div:
            number += 1
        else:
            number = 1

        try:
            div_id = Divs.objects.get(id=players.div_id)
        except Exception:
            div_id = None

        info_for_adding.append([div_id, season_id, players.team, players.name, goal, pases, goal + pases, played, number])

        if count / 500 == count // 500:
            print("Гол+Пас", count, 'из', count_all, 'Время выполнения -',
                  secondsToStr(time.time() - start_time))

            Stat_Players_GoalAndPass.objects.bulk_create(
                Stat_Players_GoalAndPass(div=div, season=season, team=team, name=name, goal=goal, pases=pases,
                                         goal_and_pases=goal_and_pases, played=played, number=number)
            for div, season, team, name, goal, pases, goal_and_pases, played, number in info_for_adding)
            info_for_adding = []


    Stat_Players_GoalAndPass.objects.bulk_create(
        Stat_Players_GoalAndPass(div=div, season=season, team=team, name=name, goal=goal, pases=pases,
                                 goal_and_pases=goal_and_pases, played=played, number=number)
        for div, season, team, name, goal, pases, goal_and_pases, played, number in info_for_adding)

    print("Список Гол+Пас =", str(len(Stat_Players_GoalAndPass.objects.all())))



def update_stat_players(request, season):
    # country = 'Украина'
    # division = 'Первая лига'
    # .filter(gametext__tur__number__lte=2)
    # .filter(gametext__tur__div__chemp__name__iexact=country).filter(gametext__tur__div__name__iexact=division)

    # ссылка на сезон
    try:
        season_id = Season.objects.get(number=season)
    except Exception:
        season_id = None

    # # список игроков, забивших гол
    # players_list_goal = Stat_Players_List_Goal.objects.filter(season__number=season).filter(
    #     div__chemp__name__iexact=country).filter(div__name__iexact=division).order_by('div')
    # # список игроков, отдавших пас
    # players_list_pass = Stat_Players_List_Pass.objects.filter(season__number=season).filter(
    #     div__chemp__name__iexact=country).filter(div__name__iexact=division).order_by('div')
    # # список игроков, забивших гол или отдавших пас
    # players_list_goalandpass = Stat_Players_List_GoalAndPass.objects.filter(season__number=season).filter(
    #     div__chemp__name__iexact=country).filter(div__name__iexact=division).order_by('div')
    # # статистика голов
    # goals_list = GamesTextReport_Goals.objects.filter(gametext__tur__season__number=season).filter(
    #     gametext__tur__div__chemp__name__iexact=country).filter(gametext__tur__div__name__iexact=division)
    # # статистика игроков
    # stat_list = GamesTextReport_Player.objects.filter(gametext__tur__season__number=season).filter(
    #     gametext__tur__div__chemp__name__iexact=country).filter(gametext__tur__div__name__iexact=division)

    # список игроков, забивших гол
    players_list_goal = Stat_Players_List_Goal.objects.filter(season__number=season).order_by('div')
    # список игроков, отдавших пас
    players_list_pass = Stat_Players_List_Pass.objects.filter(season__number=season).order_by('div')
    # # список игроков, забивших гол или отдавших пас
    players_list_goalandpass = Stat_Players_List_GoalAndPass.objects.filter(season__number=season).order_by('div')

    # print(len(players_list_goal))
    # print(len(players_list_pass))
    # print(len(players_list_goalandpass))

    update_GamesTextReport_Player_NameTeam()
    update_GamesTextReport_Goal_PlayerGoalTeam()
    update_GamesTextReport_Goal_PlayerPassTeam()
    update_stat_bombarders(season, season_id, players_list_goal)
    update_stat_pivots(season, season_id, players_list_pass)
    update_stat_goal_and_pass(season, season_id, players_list_goalandpass)

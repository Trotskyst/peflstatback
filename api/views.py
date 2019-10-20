from rest_framework import generics
from api.serializers import *
from django.db.models import Q


class ChempsCountriesView(generics.ListAPIView):
    """Список стран"""
    serializer_class = CounriesListSerializer
    queryset = Chemps.objects.all()


class DivsCountriesView(generics.ListAPIView):
    """Список дивизионов выбранной страны"""
    serializer_class = DivcListSerializer

    def get_queryset(self):
        country = self.kwargs['country']
        queryset = Divs.objects.filter(chemp__name__iexact=country)
        return queryset


class StatMainView(generics.ListAPIView):
    """Основная статистика по выбранному дивизиону выбранной страны"""
    serializer_class = GamesTextReport_MainSerializer

    def get_queryset(self):
        season = self.kwargs['season']
        country = self.kwargs['country']
        division = self.kwargs['division']
        queryset = GamesTextReport_Main.objects.filter(gametext__tur__season__number=season).filter(
            gametext__tur__div__chemp__name__iexact=country).filter(
            gametext__tur__div__name__iexact=division)
        # filter(Q(team_home='Кривбасс') | Q(team_guest='Кривбасс'))
        return queryset


class StatPlayerView(generics.ListAPIView):
    """Статистика ТТД по выбранному дивизиону выбранной страны"""
    serializer_class = GamesTextReport_PlayersSerializer

    def get_queryset(self):
        season = self.kwargs['season']
        country = self.kwargs['country']
        division = self.kwargs['division']
        queryset = GamesTextReport_Player.objects.filter(gametext__tur__season__number=season).filter(
            gametext__tur__div__chemp__name__iexact=country).filter(
            gametext__tur__div__name__iexact=division)
        # .filter(
        # Q(gametext__gamestextreport_main__team_home='Кривбасс') | Q(
        #     gametext__gamestextreport_main__team_guest='Кривбасс'))
        return queryset


class StatGoalsView(generics.ListAPIView):
    """Статистика голов по выбранному дивизиону выбранной страны"""
    serializer_class = GamesTextReport_GoalsSerializer

    def get_queryset(self):
        season = self.kwargs['season']
        country = self.kwargs['country']
        division = self.kwargs['division']
        queryset = GamesTextReport_Goals.objects.filter(gametext__tur__season__number=season).filter(
            gametext__tur__div__chemp__name__iexact=country).filter(
            gametext__tur__div__name__iexact=division)
        # .filter(
        # Q(gametext__gamestextreport_main__team_home='Кривбасс') | Q(
        #     gametext__gamestextreport_main__team_guest='Кривбасс'))
        return queryset


class StatTeamListView(generics.ListAPIView):
    """Список команд по выбранному дивизиону выбранной страны"""
    serializer_class = Stat_Team_ListSerializer

    def get_queryset(self):
        season = self.kwargs['season']
        country = self.kwargs['country']
        division = self.kwargs['division']
        queryset = Stat_Team_List.objects.filter(season__number=season).filter(
            div__chemp__name__iexact=country).filter(
            div__name__iexact=division).order_by("name")
        return queryset


class StatPlayersListGoalView(generics.ListAPIView):
    """Список игроков, забивших гол по выбранному дивизиону выбранной страны"""
    serializer_class = Stat_Players_List_GoalSerializer

    def get_queryset(self):
        season = self.kwargs['season']
        country = self.kwargs['country']
        division = self.kwargs['division']
        queryset = Stat_Players_List_Goal.objects.filter(season__number=season).filter(
            div__chemp__name__iexact=country).filter(
            div__name__iexact=division).order_by("name")
        return queryset


class StatPlayersListPassView(generics.ListAPIView):
    """Список игроков, отдавших пас по выбранному дивизиону выбранной страны"""
    serializer_class = Stat_Players_List_PassSerializer

    def get_queryset(self):
        season = self.kwargs['season']
        country = self.kwargs['country']
        division = self.kwargs['division']
        queryset = Stat_Players_List_Pass.objects.filter(season__number=season).filter(
            div__chemp__name__iexact=country).filter(
            div__name__iexact=division).exclude(name="").order_by("name")
        return queryset


class StatPlayersListGoalAndPassView(generics.ListAPIView):
    """Список игроков, забивших гол или отдавших пас по выбранному дивизиону выбранной страны"""
    serializer_class = Stat_Players_List_GoalAndPassSerializer

    def get_queryset(self):
        season = self.kwargs['season']
        country = self.kwargs['country']
        division = self.kwargs['division']
        queryset = Stat_Players_List_GoalAndPass.objects.filter(season__number=season).filter(
            div__chemp__name__iexact=country).filter(
            div__name__iexact=division).exclude(name="").order_by("name")
        return queryset


class StatPlayersBombardersView(generics.ListAPIView):
    """Список бомбардиров"""
    serializer_class = Stat_Players_BombardersSerializer

    def get_queryset(self):
        season = self.kwargs['season']
        country = self.kwargs['country']
        division = self.kwargs['division']
        queryset = Stat_Players_Bombarders.objects.filter(season__number=season).filter(
            div__chemp__name__iexact=country).filter(
            div__name__iexact=division).order_by("-goal", "-played")
        return queryset


class StatPlayersPivotsView(generics.ListAPIView):
    """Список голевых распасовщиков"""
    serializer_class = Stat_Players_PivotsSerializer

    def get_queryset(self):
        season = self.kwargs['season']
        country = self.kwargs['country']
        division = self.kwargs['division']
        queryset = Stat_Players_Pivot.objects.filter(season__number=season).filter(
            div__chemp__name__iexact=country).filter(
            div__name__iexact=division).order_by("-pases", "-played")
        return queryset


class StatPlayersGoalAndPassView(generics.ListAPIView):
    """Список Гол+Пас"""
    serializer_class = Stat_Players_GoalAndPassSerializer

    def get_queryset(self):
        season = self.kwargs['season']
        country = self.kwargs['country']
        division = self.kwargs['division']
        queryset = Stat_Players_GoalAndPass.objects.filter(season__number=season).filter(
            div__chemp__name__iexact=country).filter(
            div__name__iexact=division).order_by("-goal_and_pases", "-goal", "-played")
        return queryset


class StatPlayersPlayedMaxTimeView(generics.ListAPIView):
    """Список игроков, игравших в последних 5 турах"""
    serializer_class = Stat_Players_PlayedMaxTimeSerializer

    def get_queryset(self):
        season = self.kwargs['season']
        country = self.kwargs['country']
        division = self.kwargs['division']
        team = self.kwargs['team']
        queryset = Stat_Players_PlayedMaxTime.objects.filter(season__number=season).filter(
            div__chemp__name__iexact=country).filter(
            div__name__iexact=division).filter(
            team__iexact=team).order_by("number_in_team", "-played", "-minutes")
        return queryset


class GamesTextReportPlayerStatView(generics.ListAPIView):
    """Статистика игроков"""
    serializer_class = GamesTextReport_PlayerStatSerializer

    def get_queryset(self):
        player_id = self.kwargs['player_id']
        queryset = GamesTextReport_PlayerStat.objects.filter(player_id=player_id)
        return queryset

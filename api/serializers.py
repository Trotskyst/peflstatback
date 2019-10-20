from rest_framework import serializers
from fill.models import *


class CounriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chemps
        fields = ('id', 'name', 'link')


class DivcListSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='div.chemp.name', read_only=True)

    class Meta:
        model = Divs
        fields = ('id', 'name', 'link', 'country')


class GamesTextReport_MainSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='gametext.tur.div.chemp.name', read_only=True)
    season = serializers.CharField(source='gametext.tur.season.number', read_only=True)
    div = serializers.CharField(source='gametext.tur.div.name', read_only=True)
    tur_number = serializers.CharField(source='gametext.tur.number', read_only=True)
    tur_date = serializers.CharField(source='gametext.tur.date', read_only=True)
    game_link = serializers.CharField(source='gametext.link', read_only=True)

    class Meta:
        model = GamesTextReport_Main
        fields = '__all__'
        extra_fields = ['season', 'country', 'div', 'tur_number', 'tur_date', 'game_link']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(GamesTextReport_MainSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class GamesTextReport_PlayersSerializer(serializers.ModelSerializer):
    # country = serializers.CharField(source='gametext.tur.div.chemp.name', read_only=True)
    # season= serializers.CharField(source='gametext.tur.season.number', read_only=True)
    # div = serializers.CharField(source='gametext.tur.div.name', read_only=True)
    # tur_number = serializers.CharField(source='gametext.tur.number', read_only=True)
    # tur_date = serializers.CharField(source='gametext.tur.date', read_only=True)
    # game_link = serializers.CharField(source='gametext.link', read_only=True)

    class Meta:
        model = GamesTextReport_Player
        fields = '__all__'
        # fields = ['id']
        # extra_fields = ['season', 'country', 'div', 'tur_number', 'tur_date', 'game_link']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(GamesTextReport_PlayersSerializer, self).get_field_names(declared_fields, info)

        # if getattr(self.Meta, 'extra_fields', None):
        #     return expanded_fields + self.Meta.extra_fields
        # else:
        return expanded_fields


class GamesTextReport_GoalsSerializer(serializers.ModelSerializer):
    # country = serializers.CharField(source='gametext.tur.div.chemp.name', read_only=True)
    # season= serializers.CharField(source='gametext.tur.season.number', read_only=True)
    # div = serializers.CharField(source='gametext.tur.div.name', read_only=True)
    tur_number = serializers.CharField(source='gametext.tur.number', read_only=True)

    # tur_date = serializers.CharField(source='gametext.tur.date', read_only=True)
    # game_link = serializers.CharField(source='gametext.link', read_only=True)

    class Meta:
        model = GamesTextReport_Goals
        fields = '__all__'
        # fields = ['id']
        # extra_fields = ['season', 'country', 'div', 'tur_number', 'tur_date', 'game_link']
        extra_fields = ['tur_number']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(GamesTextReport_GoalsSerializer, self).get_field_names(declared_fields, info)

        # if getattr(self.Meta, 'extra_fields', None):
        #     return expanded_fields + self.Meta.extra_fields
        # else:
        return expanded_fields


class Stat_Team_ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat_Team_List
        fields = ('name',)


class Stat_Players_List_GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat_Players_List_Goal
        fields = ('name', 'team')


class Stat_Players_List_PassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat_Players_List_Pass
        fields = ('name', 'team')


class Stat_Players_List_GoalAndPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat_Players_List_GoalAndPass
        fields = ('name', 'team')


class Stat_Players_BombardersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat_Players_Bombarders
        fields = ('number', 'name', 'team', 'goal', 'played')


class Stat_Players_PivotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat_Players_Pivot
        fields = ('number', 'name', 'team', 'pases', 'played')


class Stat_Players_GoalAndPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat_Players_GoalAndPass
        fields = ('name', 'team', 'goal', 'pases', 'goal_and_pases', 'played')


class Stat_Players_PlayedMaxTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stat_Players_PlayedMaxTime
        fields = '__all__'
        # fields = ['id']
        # extra_fields = ['season', 'country', 'div', 'tur_number', 'tur_date', 'game_link']

class GamesTextReport_PlayerStatSerializer(serializers.ModelSerializer):

    class Meta:
        model = GamesTextReport_PlayerStat
        fields = '__all__'

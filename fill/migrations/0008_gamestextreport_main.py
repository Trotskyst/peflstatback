# Generated by Django 2.2.5 on 2019-09-11 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fill', '0007_gamestextreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='GamesTextReport_Main',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('city', models.CharField(default='', max_length=200, verbose_name='Город')),
                ('stadium', models.CharField(default='', max_length=200, verbose_name='Стадион')),
                ('viewers', models.IntegerField(verbose_name='Зрители')),
                ('minutes', models.IntegerField(verbose_name='Минут')),
                ('team_home', models.CharField(default='', max_length=50, verbose_name='Команда Дома')),
                ('team_guest', models.CharField(default='', max_length=50, verbose_name='Команда Гость')),
                ('manager_home', models.CharField(default='', max_length=50, verbose_name='Менеджер Дома')),
                ('manager_guest', models.CharField(default='', max_length=50, verbose_name='Менеджер Гость')),
                ('goals_home', models.IntegerField(verbose_name='Голы Дома')),
                ('goals_guest', models.IntegerField(verbose_name='Голы Гость')),
                ('kick_home', models.IntegerField(verbose_name='Удары Дома')),
                ('kick_guest', models.IntegerField(verbose_name='Удары Гость')),
                ('kick_target_home', models.IntegerField(verbose_name='Удары в створ Дома')),
                ('kick_target_guest', models.IntegerField(verbose_name='Удары в створ Гость')),
                ('goalpost_home', models.IntegerField(verbose_name='Штанги Дома')),
                ('goalpost_guest', models.IntegerField(verbose_name='Штанги Гость')),
                ('offside_home', models.IntegerField(verbose_name='Офсайды Дома')),
                ('offside_guest', models.IntegerField(verbose_name='Офсайды Гость')),
                ('corner_home', models.IntegerField(verbose_name='Угловые Дома')),
                ('corner_guest', models.IntegerField(verbose_name='Угловые Гость')),
                ('corner_cross_home', models.IntegerField(verbose_name='Угловые Навес Дома')),
                ('corner_cross_guest', models.IntegerField(verbose_name='Угловые Навес Гость')),
                ('corner_playout_home', models.IntegerField(verbose_name='Угловые Розыгрыш Дома')),
                ('corner_playout_guest', models.IntegerField(verbose_name='Угловые Розыгрыш Гость')),
                ('possession_home', models.IntegerField(verbose_name='Владение Дома')),
                ('possession_guest', models.IntegerField(verbose_name='Владение Гость')),
                ('kick_near_home', models.IntegerField(verbose_name='Удары из штрафной Дома')),
                ('kick_near_guest', models.IntegerField(verbose_name='Удары из штрафной Гость')),
                ('kick_near_target_home', models.IntegerField(verbose_name='Удары из штрафной в створ Дома')),
                ('kick_near_target_guest', models.IntegerField(verbose_name='Удары из штрафной в створ Гость')),
                ('kick_far_home', models.IntegerField(verbose_name='Удары из-за штрафной Дома')),
                ('kick_far_guest', models.IntegerField(verbose_name='Удары из-за штрафной Гость')),
                ('kick_far_target_home', models.IntegerField(verbose_name='Удары из-за штрафной в створ Дома')),
                ('kick_far_target_guest', models.IntegerField(verbose_name='Удары из-за штрафной в створ Гость')),
                ('kick_blocked_home', models.IntegerField(verbose_name='Заблокированные удары Дома')),
                ('kick_blocked_guest', models.IntegerField(verbose_name='Заблокированные удары Гость')),
                ('pass_home', models.IntegerField(verbose_name='Передачи Дома')),
                ('pass_guest', models.IntegerField(verbose_name='Передачи Гость')),
                ('pass_accurate_home', models.IntegerField(verbose_name='Передачи Точные Дома')),
                ('pass_accurate_guest', models.IntegerField(verbose_name='Передачи Точные Гость')),
                ('bend_home', models.IntegerField(verbose_name='Навесы Дома')),
                ('bend_guest', models.IntegerField(verbose_name='Навесы Гость')),
                ('bend_accurate_home', models.IntegerField(verbose_name='Навесы Точные Дома')),
                ('bend_accurate_guest', models.IntegerField(verbose_name='Навесы Точные Гость')),
                ('dribbling_home', models.IntegerField(verbose_name='Дриблинг Дома')),
                ('dribbling_guest', models.IntegerField(verbose_name='Дриблинг Гость')),
                ('dribbling_successful_home', models.IntegerField(verbose_name='Дриблинг Успешный Дома')),
                ('dribbling_successful_guest', models.IntegerField(verbose_name='Дриблинг Успешный Гость')),
                ('tackle_home', models.IntegerField(verbose_name='Отбор Дома')),
                ('tackle_guest', models.IntegerField(verbose_name='Отбор Гость')),
                ('tackle_successful_home', models.IntegerField(verbose_name='Отбор Успешный Дома')),
                ('tackle_successful_guest', models.IntegerField(verbose_name='Отбор Успешный Гость')),
                ('height_fight_home', models.IntegerField(verbose_name='Верховые единоборства Дома')),
                ('height_fight_guest', models.IntegerField(verbose_name='Верховые единоборства Гость')),
                ('height_fight_successful_home', models.IntegerField(verbose_name='Верховые единоборства Успешные Дома')),
                ('height_fight_successful_guest', models.IntegerField(verbose_name='Верховые единоборства Успешные Гость')),
                ('intercept_home', models.IntegerField(verbose_name='Перехваты Дома')),
                ('intercept_guest', models.IntegerField(verbose_name='Перехваты Гость')),
                ('turnover_home', models.IntegerField(verbose_name='Потери Дома')),
                ('turnover_guest', models.IntegerField(verbose_name='Потери Гость')),
                ('foul_home', models.IntegerField(verbose_name='Нарушения Дома')),
                ('foul_guest', models.IntegerField(verbose_name='Нарушения Гость')),
                ('penalty_home', models.IntegerField(verbose_name='Пенальти Дома')),
                ('penalty_guest', models.IntegerField(verbose_name='Пенальти Гость')),
                ('freekick_home', models.IntegerField(verbose_name='Штрафные Дома')),
                ('freekick_guest', models.IntegerField(verbose_name='Штрафные Гость')),
                ('freekick_cross_home', models.IntegerField(verbose_name='Штрафные Навес Дома')),
                ('freekick_cross_guest', models.IntegerField(verbose_name='Штрафные Навес Гость')),
                ('freekick_kick_home', models.IntegerField(verbose_name='Штрафные Удар Дома')),
                ('freekick_kick_guest', models.IntegerField(verbose_name='Штрафные Удар Гость')),
                ('freekick_playout_home', models.IntegerField(verbose_name='Штрафные Розыгрыш Дома')),
                ('freekick_playout_guest', models.IntegerField(verbose_name='Штрафные Розыгрыш Гость')),
                ('gametext', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fill.GamesText', verbose_name='Игра')),
            ],
            options={
                'verbose_name': 'Основная статистика матчей',
                'verbose_name_plural': 'Основная статистика Матчей',
                'ordering': ['id'],
            },
        ),
    ]

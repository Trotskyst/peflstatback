# Generated by Django 2.2.5 on 2019-10-16 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fill', '0040_auto_20191009_0931'),
    ]

    operations = [
        migrations.CreateModel(
            name='GamesTextReport_PlayerStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('player_id', models.IntegerField(verbose_name='ID игрока')),
                ('played', models.FloatField(verbose_name='Сыграно матчей')),
                ('rating', models.FloatField(verbose_name='Оценка')),
                ('capitan', models.FloatField(verbose_name='Капитан')),
                ('trauma', models.FloatField(verbose_name='Травма')),
                ('im', models.FloatField(verbose_name='ИМ')),
                ('basis', models.FloatField(verbose_name='Основа')),
                ('minutes', models.FloatField(verbose_name='Минут в матче')),
                ('count_find', models.FloatField(verbose_name='Количество в матче')),
                ('stat_kick', models.FloatField(verbose_name='Удары ногой')),
                ('stat_kick_ok', models.FloatField(verbose_name='Удары ногой OK')),
                ('stat_offside', models.FloatField(verbose_name='Офсайд')),
                ('stat_kick_far', models.FloatField(verbose_name='Дальние удары')),
                ('stat_kick_far_ok', models.FloatField(verbose_name='Дальние удары OK')),
                ('stat_head', models.FloatField(verbose_name='Удары головой')),
                ('stat_head_ok', models.FloatField(verbose_name='Удары головой OK')),
                ('stat_block', models.FloatField(verbose_name='Блокированные')),
                ('stat_pass', models.FloatField(verbose_name='Пасы')),
                ('stat_pass_ok', models.FloatField(verbose_name='Пасы OK')),
                ('stat_cross', models.FloatField(verbose_name='Навесы')),
                ('stat_cross_ok', models.FloatField(verbose_name='Навесы OK')),
                ('stat_dribbling', models.FloatField(verbose_name='Дриблинг')),
                ('stat_dribbling_ok', models.FloatField(verbose_name='Дриблинг OK')),
                ('stat_tackle', models.FloatField(verbose_name='Отбор')),
                ('stat_tackle_ok', models.FloatField(verbose_name='Отбор OK')),
                ('stat_up', models.FloatField(verbose_name='Верховые единоборства')),
                ('stat_up_ok', models.FloatField(verbose_name='Верховые единоборства OK')),
                ('stat_perehvat', models.FloatField(verbose_name='Перехваты')),
                ('stat_poter', models.FloatField(verbose_name='Потери')),
                ('stat_foul', models.FloatField(verbose_name='Фолы')),
                ('stat_foul_him', models.FloatField(verbose_name='Фолы на нём')),
            ],
        ),
    ]

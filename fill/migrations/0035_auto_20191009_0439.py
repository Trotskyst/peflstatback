# Generated by Django 2.2.5 on 2019-10-09 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fill', '0034_stat_players_playedmaxtime_list_mintur'),
    ]

    operations = [
        migrations.AddField(
            model_name='stat_players_playedmaxtime_list',
            name='number',
            field=models.IntegerField(default=0, verbose_name='Номер тура'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stat_players_playedmaxtime_list_mintur',
            name='number',
            field=models.IntegerField(verbose_name='Номер тура'),
        ),
    ]

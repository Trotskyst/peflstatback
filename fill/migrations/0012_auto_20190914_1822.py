# Generated by Django 2.2.5 on 2019-09-14 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fill', '0011_auto_20190913_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamestextreport_main',
            name='gametext',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fill.GamesText', verbose_name='Игра'),
        ),
        migrations.DeleteModel(
            name='GamesTextReport',
        ),
    ]

# Generated by Django 2.2.5 on 2019-09-11 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fill', '0005_turs_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='GamesText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('link', models.CharField(default='', max_length=1000, verbose_name='Ссылка на матч')),
                ('tur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fill.Turs', verbose_name='Тур')),
            ],
            options={
                'verbose_name': 'Список матчей',
                'verbose_name_plural': 'Матчи',
                'ordering': ['link'],
            },
        ),
    ]

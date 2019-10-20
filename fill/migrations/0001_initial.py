# Generated by Django 2.2.5 on 2019-09-09 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chemps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('name', models.CharField(db_index=True, max_length=1000, verbose_name='Чемпионат')),
                ('link', models.CharField(db_index=True, max_length=1000, verbose_name='Ссылка на чемпионат')),
            ],
            options={
                'verbose_name': 'Чемпионат',
                'verbose_name_plural': 'Чемпионаты',
                'ordering': ['name'],
            },
        ),
    ]

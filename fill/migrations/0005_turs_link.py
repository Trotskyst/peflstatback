# Generated by Django 2.2.5 on 2019-09-11 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fill', '0004_turs'),
    ]

    operations = [
        migrations.AddField(
            model_name='turs',
            name='link',
            field=models.CharField(default='', max_length=1000, verbose_name='Ссылка на тур'),
        ),
    ]

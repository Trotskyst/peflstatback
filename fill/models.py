from django.db import models


class Season(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    number = models.IntegerField(verbose_name='Сезон')

    class Meta:
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезон'
        ordering = ['number']

    def __str__(self):
        return str(self.number)


class Chemps(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    name = models.CharField(verbose_name='Чемпионат', db_index=True, max_length=1000)
    link = models.CharField(verbose_name='Ссылка на чемпионат', db_index=True, max_length=1000)

    class Meta:
        verbose_name = 'Чемпионат'
        verbose_name_plural = 'Чемпионаты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Divs(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    chemp = models.ForeignKey(Chemps, verbose_name='Чемпионат', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name='Дивизион', db_index=True, max_length=1000)
    link = models.CharField(verbose_name='Ссылка на дивизион', db_index=True, max_length=1000)
    sort = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Дивизион'
        verbose_name_plural = 'Дивизионы'
        ordering = ['sort']

    def __str__(self):
        return str(self.chemp.name) + '. ' + self.name


class Teams(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    div = models.ForeignKey(Divs, verbose_name='Дивизион', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name='Команда', db_index=True, max_length=1000)
    link = models.CharField(verbose_name='Ссылка на команду', db_index=True, max_length=1000)

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        ordering = ['name']


class Turs(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    div = models.ForeignKey(Divs, verbose_name='Дивизион', on_delete=models.CASCADE, null=True, blank=True)
    number = models.IntegerField(verbose_name='Номер')
    date = models.DateField(verbose_name='Дата')
    link = models.CharField(verbose_name='Ссылка на тур', default='', max_length=1000)
    season = models.ForeignKey(Season, verbose_name='Сезон', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Список туров'
        verbose_name_plural = 'Туры'
        ordering = ['number']

    def __str__(self):
        return str(self.div.chemp.name) + '. ' + str(self.div.name) + '. ' + str(self.number) + ' (' + str(
            self.date) + ')'


class GamesText(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    tur = models.ForeignKey(Turs, verbose_name='Тур', on_delete=models.CASCADE, null=True, blank=True)
    link = models.CharField(verbose_name='Ссылка на матч', default='', max_length=1000)

    class Meta:
        verbose_name = 'Список матчей'
        verbose_name_plural = 'Матчи'
        ordering = ['link']

    def __str__(self):
        return str(self.id)


# class GamesTextReport(models.Model):
#     timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
#     gametext = models.ForeignKey(GamesText, verbose_name='Игра', on_delete=models.CASCADE, null=True, blank=True)
#     report = models.TextField(verbose_name='Текстовый отчет')
#
#     class Meta:
#         verbose_name = 'Текст матчей'
#         verbose_name_plural = 'Тексты Матчей'
#         ordering = ['id']
#
#     def __str__(self):
#         return str(self.id)


class GamesTextReport_Main(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    gametext = models.ForeignKey(GamesText, verbose_name='Игра', on_delete=models.CASCADE, null=True, blank=True)

    # http://study-english.info/football.php
    # http://nskhuman.ru/fbdocs/fbslovar.php?letter=%CF

    city = models.CharField(verbose_name='Город', default='', max_length=200)
    stadium = models.CharField(verbose_name='Стадион', default='', max_length=200)
    viewers = models.IntegerField(verbose_name='Зрители')
    minutes = models.IntegerField(verbose_name='Минут')
    arbitr = models.CharField(verbose_name='Арбитр', default='', max_length=200)
    wheater = models.CharField(verbose_name='Погода', default='', max_length=10)

    team_home = models.CharField(verbose_name='Команда Дома', default='', max_length=50)
    team_guest = models.CharField(verbose_name='Команда Гость', default='', max_length=50)

    manager_home = models.CharField(verbose_name='Менеджер Дома', default='', max_length=50)
    manager_guest = models.CharField(verbose_name='Менеджер Гость', default='', max_length=50)

    goals_home = models.IntegerField(verbose_name='Голы Дома')
    goals_guest = models.IntegerField(verbose_name='Голы Гость')

    kick_home = models.IntegerField(verbose_name='Удары Дома')
    kick_guest = models.IntegerField(verbose_name='Удары Гость')

    kick_target_home = models.IntegerField(verbose_name='Удары в створ Дома')
    kick_target_guest = models.IntegerField(verbose_name='Удары в створ Гость')

    goalpost_home = models.IntegerField(verbose_name='Штанги Дома')
    goalpost_guest = models.IntegerField(verbose_name='Штанги Гость')

    offside_home = models.IntegerField(verbose_name='Офсайды Дома')
    offside_guest = models.IntegerField(verbose_name='Офсайды Гость')

    corner_home = models.IntegerField(verbose_name='Угловые Дома')
    corner_guest = models.IntegerField(verbose_name='Угловые Гость')

    corner_cross_home = models.IntegerField(verbose_name='Угловые Навес Дома')
    corner_cross_guest = models.IntegerField(verbose_name='Угловые Навес Гость')

    corner_playout_home = models.IntegerField(verbose_name='Угловые Розыгрыш Дома')
    corner_playout_guest = models.IntegerField(verbose_name='Угловые Розыгрыш Гость')

    possession_home = models.IntegerField(verbose_name='Владение Дома')
    possession_guest = models.IntegerField(verbose_name='Владение Гость')

    kick_near_home = models.IntegerField(verbose_name='Удары из штрафной Дома')
    kick_near_guest = models.IntegerField(verbose_name='Удары из штрафной Гость')

    kick_near_target_home = models.IntegerField(verbose_name='Удары из штрафной в створ Дома')
    kick_near_target_guest = models.IntegerField(verbose_name='Удары из штрафной в створ Гость')

    kick_far_home = models.IntegerField(verbose_name='Удары из-за штрафной Дома')
    kick_far_guest = models.IntegerField(verbose_name='Удары из-за штрафной Гость')

    kick_far_target_home = models.IntegerField(verbose_name='Удары из-за штрафной в створ Дома')
    kick_far_target_guest = models.IntegerField(verbose_name='Удары из-за штрафной в створ Гость')

    kick_blocked_home = models.IntegerField(verbose_name='Заблокированные удары Дома')
    kick_blocked_guest = models.IntegerField(verbose_name='Заблокированные удары Гость')

    pass_home = models.IntegerField(verbose_name='Передачи Дома')
    pass_guest = models.IntegerField(verbose_name='Передачи Гость')

    pass_accurate_home = models.IntegerField(verbose_name='Передачи Точные Дома')
    pass_accurate_guest = models.IntegerField(verbose_name='Передачи Точные Гость')

    bend_home = models.IntegerField(verbose_name='Навесы Дома')
    bend_guest = models.IntegerField(verbose_name='Навесы Гость')

    bend_accurate_home = models.IntegerField(verbose_name='Навесы Точные Дома')
    bend_accurate_guest = models.IntegerField(verbose_name='Навесы Точные Гость')

    dribbling_home = models.IntegerField(verbose_name='Дриблинг Дома')
    dribbling_guest = models.IntegerField(verbose_name='Дриблинг Гость')

    dribbling_successful_home = models.IntegerField(verbose_name='Дриблинг Успешный Дома')
    dribbling_successful_guest = models.IntegerField(verbose_name='Дриблинг Успешный Гость')

    tackle_home = models.IntegerField(verbose_name='Отбор Дома')
    tackle_guest = models.IntegerField(verbose_name='Отбор Гость')

    tackle_successful_home = models.IntegerField(verbose_name='Отбор Успешный Дома')
    tackle_successful_guest = models.IntegerField(verbose_name='Отбор Успешный Гость')

    height_fight_home = models.IntegerField(verbose_name='Верховые единоборства Дома')
    height_fight_guest = models.IntegerField(verbose_name='Верховые единоборства Гость')

    height_fight_successful_home = models.IntegerField(verbose_name='Верховые единоборства Успешные Дома')
    height_fight_successful_guest = models.IntegerField(verbose_name='Верховые единоборства Успешные Гость')

    intercept_home = models.IntegerField(verbose_name='Перехваты Дома')
    intercept_guest = models.IntegerField(verbose_name='Перехваты Гость')

    turnover_home = models.IntegerField(verbose_name='Потери Дома')
    turnover_guest = models.IntegerField(verbose_name='Потери Гость')

    foul_home = models.IntegerField(verbose_name='Нарушения Дома')
    foul_guest = models.IntegerField(verbose_name='Нарушения Гость')

    penalty_home = models.IntegerField(verbose_name='Пенальти Дома')
    penalty_guest = models.IntegerField(verbose_name='Пенальти Гость')

    freekick_home = models.IntegerField(verbose_name='Штрафные Дома')
    freekick_guest = models.IntegerField(verbose_name='Штрафные Гость')

    freekick_cross_home = models.IntegerField(verbose_name='Штрафные Навес Дома')
    freekick_cross_guest = models.IntegerField(verbose_name='Штрафные Навес Гость')

    freekick_kick_home = models.IntegerField(verbose_name='Штрафные Удар Дома')
    freekick_kick_guest = models.IntegerField(verbose_name='Штрафные Удар Гость')

    freekick_playout_home = models.IntegerField(verbose_name='Штрафные Розыгрыш Дома')
    freekick_playout_guest = models.IntegerField(verbose_name='Штрафные Розыгрыш Гость')

    class Meta:
        verbose_name = 'Основная статистика матчей'
        verbose_name_plural = 'Основная статистика матчей'
        ordering = ['id']

    # def __str__(self):
    #     return str(self.id)


class GamesTextReport_Player(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    gametext = models.ForeignKey(GamesText, verbose_name='Игра', on_delete=models.CASCADE, null=True, blank=True)

    # http://study-english.info/football.php
    # http://nskhuman.ru/fbdocs/fbslovar.php?letter=%CF

    number = models.IntegerField(verbose_name='Номер')
    name = models.CharField(verbose_name='Имя', default='', max_length=200)
    team = models.CharField(verbose_name='Команда', default='', max_length=200)
    player_id = models.IntegerField(verbose_name='ID игрока')
    rating = models.FloatField(verbose_name='Оценка')
    minutes = models.IntegerField(verbose_name='Минута')
    card = models.CharField(verbose_name='Карточка', default='', max_length=50)
    capitan = models.IntegerField(verbose_name='Капитан')
    home = models.IntegerField(verbose_name='Дома')
    trauma = models.IntegerField(verbose_name='Травма')
    im = models.IntegerField(verbose_name='ИМ')
    basis = models.IntegerField(verbose_name='Основа')
    count_find = models.IntegerField(verbose_name='Количество в матче')
    stat_kick = models.IntegerField(verbose_name='Удары ногой')
    stat_kick_ok = models.IntegerField(verbose_name='Удары ногой OK')
    stat_shtanga = models.IntegerField(verbose_name='Штанги')
    stat_offside = models.IntegerField(verbose_name='Офсайд')
    stat_kick_far = models.IntegerField(verbose_name='Дальние удары')
    stat_kick_far_ok = models.IntegerField(verbose_name='Дальние удары OK')
    stat_head = models.IntegerField(verbose_name='Удары головой')
    stat_head_ok = models.IntegerField(verbose_name='Удары головой OK')
    stat_block = models.IntegerField(verbose_name='Блокированные')
    stat_pass = models.IntegerField(verbose_name='Пасы')
    stat_pass_ok = models.IntegerField(verbose_name='Пасы OK')
    stat_cross = models.IntegerField(verbose_name='Навесы')
    stat_cross_ok = models.IntegerField(verbose_name='Навесы OK')
    stat_dribbling = models.IntegerField(verbose_name='Дриблинг')
    stat_dribbling_ok = models.IntegerField(verbose_name='Дриблинг OK')
    stat_tackle = models.IntegerField(verbose_name='Отбор')
    stat_tackle_ok = models.IntegerField(verbose_name='Отбор OK')
    stat_up = models.IntegerField(verbose_name='Верховые единоборства')
    stat_up_ok = models.IntegerField(verbose_name='Верховые единоборства OK')
    stat_perehvat = models.IntegerField(verbose_name='Перехваты')
    stat_poter = models.IntegerField(verbose_name='Потери')
    stat_foul = models.IntegerField(verbose_name='Фолы')
    stat_foul_him = models.IntegerField(verbose_name='Фолы на нём')
    stat_save = models.IntegerField(verbose_name='Сейвы')
    stat_save_ok = models.IntegerField(verbose_name='Сейвы OK')

    class Meta:
        verbose_name = 'Статистика игроков из матчей'
        verbose_name_plural = 'Статистика игроков из матчей'
        ordering = ['id']


class GamesTextReport_Goals(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    gametext = models.ForeignKey(GamesText, verbose_name='Игра', on_delete=models.CASCADE, null=True, blank=True)

    minutes = models.IntegerField(verbose_name='Минута')
    player_goal = models.CharField(verbose_name='Забивший гол', default='', max_length=200)
    player_pass = models.CharField(verbose_name='Отдавший пас', default='', max_length=200)
    team = models.CharField(verbose_name='Команда', default='', max_length=200)
    home = models.IntegerField(verbose_name='Дома')
    own_goal = models.IntegerField(verbose_name='Автогол')
    penalty = models.IntegerField(verbose_name='Пенальти')
    type = models.CharField(verbose_name='Тип гола', default='', max_length=200)

    class Meta:
        verbose_name = 'Статистика голов из матчей'
        verbose_name_plural = 'Статистика голов из матчей'
        ordering = ['id']


class Stat_Team_List(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    div = models.ForeignKey(Divs, verbose_name='Дивизион', on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(Season, verbose_name='Сезон', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name='Команда', default='', max_length=200)


class Stat_Players_List_Goal(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    div = models.ForeignKey(Divs, verbose_name='Дивизион', on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(Season, verbose_name='Сезон', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name='Игрок', default='', db_index=True, max_length=200)
    team = models.CharField(verbose_name='Команда', default='', db_index=True, max_length=200)


class Stat_Players_List_Pass(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    div = models.ForeignKey(Divs, verbose_name='Дивизион', on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(Season, verbose_name='Сезон', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name='Игрок', default='', max_length=200)
    team = models.CharField(verbose_name='Команда', default='', max_length=200)


class Stat_Players_List_GoalAndPass(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    div = models.ForeignKey(Divs, verbose_name='Дивизион', on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(Season, verbose_name='Сезон', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name='Игрок', default='', max_length=200)
    team = models.CharField(verbose_name='Команда', default='', max_length=200)


class Stat_Players_Bombarders(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    div = models.ForeignKey(Divs, verbose_name='Дивизион', on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(Season, verbose_name='Сезон', on_delete=models.CASCADE, null=True, blank=True)
    number = models.IntegerField(verbose_name='Номер')
    name = models.CharField(verbose_name='Игрок', default='', max_length=200)
    team = models.CharField(verbose_name='Команда', default='', max_length=200)
    goal = models.IntegerField(verbose_name='Голов')
    played = models.IntegerField(verbose_name='Матчей')


class Stat_Players_Pivot(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    div = models.ForeignKey(Divs, verbose_name='Дивизион', db_index=True, on_delete=models.CASCADE, null=True,
                            blank=True)
    season = models.ForeignKey(Season, verbose_name='Сезон', db_index=True, on_delete=models.CASCADE, null=True,
                               blank=True)
    number = models.IntegerField(verbose_name='Номер')
    name = models.CharField(verbose_name='Игрок', default='', max_length=200)
    team = models.CharField(verbose_name='Команда', default='', max_length=200)
    pases = models.IntegerField(verbose_name='Пасов')
    played = models.IntegerField(verbose_name='Матчей')


class Stat_Players_GoalAndPass(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    div = models.ForeignKey(Divs, verbose_name='Дивизион', on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(Season, verbose_name='Сезон', on_delete=models.CASCADE, null=True, blank=True)
    number = models.IntegerField(verbose_name='Номер')
    name = models.CharField(verbose_name='Игрок', default='', max_length=200)
    team = models.CharField(verbose_name='Команда', default='', max_length=200)
    goal = models.IntegerField(verbose_name='Голов')
    pases = models.IntegerField(verbose_name='Пасов')
    goal_and_pases = models.IntegerField(verbose_name='Гол+Пас')
    played = models.IntegerField(verbose_name='Матчей')


class GamesTextReport_Player_NameTeam(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    name = models.CharField(verbose_name='Имя', default='', db_index=True, max_length=200)
    team = models.CharField(verbose_name='Команда', default='', db_index=True, max_length=200)


class GamesTextReport_Goal_PlayerGoalTeam(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    name = models.CharField(verbose_name='Имя', default='', db_index=True, max_length=200)
    team = models.CharField(verbose_name='Команда', default='', db_index=True, max_length=200)


class GamesTextReport_Goal_PlayerPassTeam(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    name = models.CharField(verbose_name='Имя', default='', db_index=True, max_length=200)
    team = models.CharField(verbose_name='Команда', default='', db_index=True, max_length=200)


class Stat_Players_PlayedMaxTime(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    div = models.ForeignKey(Divs, verbose_name='Дивизион', on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(Season, verbose_name='Сезон', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name='Имя', default='', db_index=True, max_length=200)
    team = models.CharField(verbose_name='Команда', default='', db_index=True, max_length=200)
    player_id = models.IntegerField(verbose_name='ID игрока')
    number_in_team = models.FloatField(verbose_name='Примерный номер')
    goal = models.IntegerField(verbose_name='Голов', null=True, blank=True)
    pases = models.IntegerField(verbose_name='Голевых пасов', null=True, blank=True)
    played = models.IntegerField(verbose_name='Матчей')
    rating = models.FloatField(verbose_name='Оценка')
    minutes = models.IntegerField(verbose_name='Минута')
    card = models.CharField(verbose_name='Карточка', default='', max_length=50)
    capitan = models.IntegerField(verbose_name='Капитан')
    im = models.IntegerField(verbose_name='ИМ')
    basis = models.IntegerField(verbose_name='Основа')
    count_find = models.IntegerField(verbose_name='Количество в матче')
    stat_kick = models.IntegerField(verbose_name='Удары ногой')
    stat_kick_ok = models.IntegerField(verbose_name='Удары ногой OK')
    stat_kick_no = models.IntegerField(verbose_name='Удары ногой NO')
    stat_shtanga = models.IntegerField(verbose_name='Штанги')
    stat_offside = models.IntegerField(verbose_name='Офсайд')
    stat_kick_far = models.IntegerField(verbose_name='Дальние удары')
    stat_kick_far_ok = models.IntegerField(verbose_name='Дальние удары OK')
    stat_kick_far_no = models.IntegerField(verbose_name='Дальние удары NO')
    stat_head = models.IntegerField(verbose_name='Удары головой')
    stat_head_ok = models.IntegerField(verbose_name='Удары головой OK')
    stat_head_no = models.IntegerField(verbose_name='Удары головой NO')
    stat_block = models.IntegerField(verbose_name='Блокированные')
    stat_pass = models.IntegerField(verbose_name='Пасы')
    stat_pass_ok = models.IntegerField(verbose_name='Пасы OK')
    stat_pass_no = models.IntegerField(verbose_name='Пасы NO')
    stat_cross = models.IntegerField(verbose_name='Навесы')
    stat_cross_ok = models.IntegerField(verbose_name='Навесы OK')
    stat_cross_no = models.IntegerField(verbose_name='Навесы NO')
    stat_dribbling = models.IntegerField(verbose_name='Дриблинг')
    stat_dribbling_ok = models.IntegerField(verbose_name='Дриблинг OK')
    stat_dribbling_no = models.IntegerField(verbose_name='Дриблинг NO')
    stat_tackle = models.IntegerField(verbose_name='Отбор')
    stat_tackle_ok = models.IntegerField(verbose_name='Отбор OK')
    stat_tackle_no = models.IntegerField(verbose_name='Отбор NO')
    stat_up = models.IntegerField(verbose_name='Верховые единоборства')
    stat_up_ok = models.IntegerField(verbose_name='Верховые единоборства OK')
    stat_up_no = models.IntegerField(verbose_name='Верховые единоборства NO')
    stat_perehvat = models.IntegerField(verbose_name='Перехваты')
    stat_poter = models.IntegerField(verbose_name='Потери')
    stat_foul = models.IntegerField(verbose_name='Фолы')
    stat_foul_him = models.IntegerField(verbose_name='Фолы на нём')
    stat_save = models.IntegerField(verbose_name='Сейвы')
    stat_save_ok = models.IntegerField(verbose_name='Сейвы OK')
    stat_save_no = models.IntegerField(verbose_name='Сейвы NO')


class Stat_Players_PlayedMaxTime_List(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    div = models.ForeignKey(Divs, verbose_name='Дивизион', on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(Season, verbose_name='Сезон', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name='Имя', default='', db_index=True, max_length=200)
    team = models.CharField(verbose_name='Команда', default='', db_index=True, max_length=200)
    player_id = models.IntegerField(verbose_name='ID игрока')
    number = models.IntegerField(verbose_name='Номер тура')


class Stat_Players_PlayedMaxTime_List_MinTur(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    div = models.ForeignKey(Divs, verbose_name='Дивизион', on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(Season, verbose_name='Сезон', on_delete=models.CASCADE, null=True, blank=True)
    team = models.CharField(verbose_name='Команда', default='', db_index=True, max_length=200)
    number = models.IntegerField(verbose_name='Номер тура')


class Stat_Players_PlayedMaxTime_Goals(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    div = models.ForeignKey(Divs, verbose_name='Дивизион', on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(Season, verbose_name='Сезон', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name='Имя', default='', db_index=True, max_length=200)
    team = models.CharField(verbose_name='Команда', default='', db_index=True, max_length=200)
    player_id = models.IntegerField(verbose_name='ID игрока')
    goal = models.IntegerField(verbose_name='Голов')


class Stat_Players_PlayedMaxTime_Pass(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    div = models.ForeignKey(Divs, verbose_name='Дивизион', on_delete=models.CASCADE, null=True, blank=True)
    season = models.ForeignKey(Season, verbose_name='Сезон', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(verbose_name='Имя', default='', db_index=True, max_length=200)
    team = models.CharField(verbose_name='Команда', default='', db_index=True, max_length=200)
    player_id = models.IntegerField(verbose_name='ID игрока')
    pases = models.IntegerField(verbose_name='Пасов')


class GamesTextReport_PlayerStat(models.Model):
    timestamp = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    player_id = models.IntegerField(verbose_name='ID игрока')
    played = models.FloatField(verbose_name='Сыграно матчей')
    goal = models.IntegerField(verbose_name='Голов', null=True, blank=True)
    pases = models.IntegerField(verbose_name='Голевых пасов', null=True, blank=True)
    rating = models.FloatField(verbose_name='Оценка')
    capitan = models.FloatField(verbose_name='Капитан')
    trauma = models.FloatField(verbose_name='Травма')
    im = models.FloatField(verbose_name='ИМ')
    basis = models.FloatField(verbose_name='Основа')
    minutes = models.FloatField(verbose_name='Минут в матче')
    count_find = models.FloatField(verbose_name='Количество в матче')
    stat_kick = models.FloatField(verbose_name='Удары ногой')
    stat_kick_ok = models.FloatField(verbose_name='Удары ногой OK')
    stat_offside = models.FloatField(verbose_name='Офсайд')
    stat_kick_far = models.FloatField(verbose_name='Дальние удары')
    stat_kick_far_ok = models.FloatField(verbose_name='Дальние удары OK')
    stat_head = models.FloatField(verbose_name='Удары головой')
    stat_head_ok = models.FloatField(verbose_name='Удары головой OK')
    stat_block = models.FloatField(verbose_name='Блокированные')
    stat_pass = models.FloatField(verbose_name='Пасы')
    stat_pass_ok = models.FloatField(verbose_name='Пасы OK')
    stat_cross = models.FloatField(verbose_name='Навесы')
    stat_cross_ok = models.FloatField(verbose_name='Навесы OK')
    stat_dribbling = models.FloatField(verbose_name='Дриблинг')
    stat_dribbling_ok = models.FloatField(verbose_name='Дриблинг OK')
    stat_tackle = models.FloatField(verbose_name='Отбор')
    stat_tackle_ok = models.FloatField(verbose_name='Отбор OK')
    stat_up = models.FloatField(verbose_name='Верховые единоборства')
    stat_up_ok = models.FloatField(verbose_name='Верховые единоборства OK')
    stat_perehvat = models.FloatField(verbose_name='Перехваты')
    stat_poter = models.FloatField(verbose_name='Потери')
    stat_foul = models.FloatField(verbose_name='Фолы')
    stat_foul_him = models.FloatField(verbose_name='Фолы на нём')

from fill.models import *

def test_viewers(self, season, n):
    limit = 100
    table = GamesTextReport_Main.objects.filter(gametext__tur__season__number=season).filter(viewers__lte=limit)
    if len(table) == 0:
        print('Тест '+str(n)+' OK (Количество зрителей)')
        return
    print('Количество зрителей меньше '+str(limit)+' в матчах:')
    for d in table:
         print(d.gametext.link)


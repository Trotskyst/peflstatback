import requests
import lxml.html as html
import os.path
import json
import time


def only_digit(s: str) -> int:
    return int(''.join(char for char in s if char.isdigit()))

def remove_digit(s: str) -> str:
    return (''.join(char for char in s if not char.isdigit()))


def text_from_json(cookies: str, link: str):
    """ Скачивает с сайта pefl.ru JSON страницу по её адресу """
    headers = {
        'Cookie': cookies,
        'cache-control': "no-cache"
    }
    page = requests.request("GET", link, headers=headers)
    return json.loads(page.text)


# def text_from_link(cookies: str, link: str):
def text_from_link(cookies: str, link: str):
    """ Скачивает страницу с Пефла по её адресу """
    headers = {
        'Cookie': cookies,
        'cache-control': "no-cache",
        # 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        # 'Accept-Encoding': "gzip, deflate",
        # 'Accept-Language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        # 'Connection': "keep-alive",
        # 'Content-Length': "36",
        # 'Content-Type': "application/x-www-form-urlencoded",
        # 'Host': "pefl.ru",
        # 'Origin': "http://pefl.ru",
        # 'Referer': "http://pefl.ru/auth.php",
        # 'Upgrade-Insecure-Requests': "1",
        # 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        # 'x-compress': "null"
    }
    page = ''
    # print()
    while page == '':
        try:
            page = requests.request("GET", link, headers=headers)
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    page.encoding = 'windows-1251'
    print(page.text, file=open('file1.htm', 'w'))
    return html.document_fromstring(page.text)


def text_from_link2(link: str):
    """ Скачивает страницу с Пефла по её адресу """
    headers = {
        # 'Cookie': cookies,
        'cache-control': "no-cache"
    }
    page = ''
    # print(link)
    while page == '':
        try:
            page = requests.request("GET", link, headers=headers)
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    page.encoding = 'windows-1251'
    print(page.text, file=open('file.htm', 'w'))
    return page.text


def find_link_by_link_text(cookies: str, doc, text_to_find: str) -> str:
    """ Находит в документе ссылку "a href=" по тексту ссылки """
    for links in doc.cssselect('a'):
        if links.text == text_to_find:
            return links.get('href')


def GetFromJSON(filename: str, key: str) -> str:
    """ Считываем значение из атрибута JSON-файла """
    filename = "config/" + filename + ".json"
    if os.path.exists(filename):  # если файл существует
        with open(filename, "r") as read_file:
            values = json.load(read_file)
            if key in values:
                return values[key]
            else:
                return ""
    else:
        return ""


def SetToJSON(filename: str, key: str, value: str) -> str:
    """ Сохраняем значение в определенный атрибута JSON-файла """
    filename = "config/" + filename + ".json"
    with open(filename, "r") as f:
        data = json.load(f)
    data[key] = value
    with open(filename, 'w') as f:
        json.dump(data, f)


def find_link_by_link_text(doc, text_to_find: str) -> str:
    """ Находит в документе ссылку "a href=" по тексту ссылки """
    for links in doc.cssselect('a'):
        if links.text == text_to_find:
            return links.get('href')


def get_object_from_bracket(text: str):
    """Извлекает текст из текста формата 15(5)"""
    if text == '':
        return [0, 0]
    s = text.split('(')
    # print(text)
    s[0] = int(s[0])
    s[1] = int(s[1].replace(')', ''))
    return s

def get_object_without_bracket(text: str) -> str:
    if text =='':
        return 0
    return int(text)


def secondsToStr(elapsed=None):
    from time import time, strftime, localtime
    from datetime import timedelta
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))
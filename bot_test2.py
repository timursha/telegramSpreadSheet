# -*- coding: utf-8 -*-

import requests

import gspread
from oauth2client.service_account import ServiceAccountCredentials

url = "https://api.telegram.org/bot610838817:AAF9xCiXNIKcTblYExMNMZfCvk0Ie3wnz0E/"

# авторизация в сервисах гугла
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('My_Project_11634-cd3fde229bdd.json', scope)  # client_email
gc = gspread.authorize(credentials)

sht = gc.open_by_url('')  # id таблицы
worksheet1 = sht.get_worksheet(0)



def get_updates_json(request):
    params = {'timeout': 100, 'offset': None}
    response = requests.get(request + 'getUpdates', data=params)
    return response.json()


def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]


def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id


def get_username(update):
    username = update['message']['from']['username']
    return username


def get_name(update):
    name = update['message']['from']['first_name'] + " " + update['message']['from']['last_name']
    return name


def get_text(update):
    text = update['message']['text']
    return text


def send_mess(chat, text, nosound):
    params = {'chat_id': chat, 'text': text, 'disable_notification': nosound}
    response = requests.post(url + 'sendMessage', data=params)
    return response


# заполенение ячеек в гугл таблице
def to_spreadsheet(data):
    row = str(worksheet1.acell('L1').value)  # в ячейке L1 должен быть номер первой свободной строке
    worksheet1.update_acell('A' + row, data['message']['date'])
    worksheet1.update_acell('B' + row,
                            data['message']['from']['first_name'] + " " + data['message']['from']['last_name'])
    worksheet1.update_acell('C' + row, data['message']['from']['username'])
    worksheet1.update_acell('D' + row, data['message']['chat']['id'])
    worksheet1.update_acell('E' + row, data['message']['text'])


def search(number):
    col = worksheet1.col_values(2)
    ok = False
    for cell in col:
        if cell == number:
            send_mess("xxxx", "Yes", 0)
            ok = True
            break
    if not ok:
        send_mess("xxxx", "No", 0)


def main():
    update_id = last_update(get_updates_json(url))['update_id']
    listen_for_number = False
    while True:
        if update_id == last_update(get_updates_json(url))['update_id']:
            l_update = last_update(get_updates_json(url))
            chat_id = get_chat_id(l_update)
            username = get_username(l_update)
            try:
                name = get_name(l_update)
            except:
                name = "idk"
            text = get_text(l_update)
            if listen_for_number:
                search(text)
                listen_for_number = False
            else:
                if text == "/search" or text == "/find":
                    send_mess("xxxx", "Please write number", 0)
                    listen_for_number = True
                else:

                    # отправляем ответ пользователю
                    send_mess(chat_id, "здравствуйте, " + name + ", скоро мы ответим " + text, 0)

                    # отправляем его сообщение себе
                    send_mess("xxxx", "@" + username + " wrote: " + text, 0)

                    # заносим сообщение в гугл таблицу
                    to_spreadsheet(l_update)

            update_id += 1
            # sleep(2)
            print("testing...")


if __name__ == '__main__':
    main()

import os.path

from googleapiclient.discovery import build
from google.oauth2 import service_account


SCOPES = ['не могу указать']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'vigruzka-plateg-d4a712e7c708.json')

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = 'не могу указать'
SAMPLE_RANGE_NAME = 'Лист1'

service1 = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
service2 = build('sheets', 'v4', credentials=credentials)


def del_dob(indec):

    if "добавить" in indec:
        range_1 = 'БД!A1'
        array = {'values': [[]]}
        service1.append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                        range=range_1,
                        valueInputOption='USER_ENTERED',
                        body=array).execute()

    elif "Тип платежа" in indec:

        data = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                              range="СПИСКИ ДЛЯ БОТА!A2:A").execute().get('values', [])
        return data

    elif "Кол-во касаний" in indec:

        data = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                              range="СПИСКИ ДЛЯ БОТА!B2:B").execute().get('values', [])
        return data

    elif "Куда поступила" in indec:

        data = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                              range="СПИСКИ ДЛЯ БОТА!C2:C").execute().get('values', [])
        return data

    elif "Откуда лид" in indec:

        data = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                              range="СПИСКИ ДЛЯ БОТА!D2:D").execute().get('values', [])
        return data

    elif "РГП" in indec:

        data = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                              range="СПИСКИ ДЛЯ БОТА!E2:E").execute().get('values', [])
        return data

    elif "ПРОЕКТ" in indec:

        data = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                              range="СПИСКИ ДЛЯ БОТА!F2:F").execute().get('values', [])
        return data

    elif "ХЕШТЕГ" in indec:
        data = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                    range="СПИСКИ ДЛЯ БОТА!G2:K").execute().get('values', [])
        return data

    elif "ФОТО" in indec:
        data = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                    range="СПИСКИ ДЛЯ БОТА!G2:L").execute().get('values', [])
        return data

    elif "ФИО ТМа" in indec:
        data = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                    range="СПИСКИ ДЛЯ БОТА!O2:P").execute().get('values', [])
        return data

    elif "удалить" in indec:
        batch_clear_values_request_body = {'ranges': ['Лист1!A:A']}
        request = service2.spreadsheets().values().batchClear(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                              body=batch_clear_values_request_body)
        request.execute()

    elif "закрыть все" in indec:
        batch_clear_values_request_body = {'ranges': ['Лист1!A:A']}
        request = service2.spreadsheets().values().batchClear(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                              body=batch_clear_values_request_body)
        request.execute()


def spiski(indec):
    return [item[0] for item in del_dob(indec)]


def hesteg(name_pgp):
    indec = 'ХЕШТЕГ'
    data = del_dob(indec)
    for item in data:
        if item[0] == name_pgp:
            heshteg = (f"{item[1]}\n"
                       f"{item[3]}")
            return heshteg


def podraz(name_pgp):
    indec = 'ХЕШТЕГ'
    data = del_dob(indec)
    for item in data:
        if item[0] == name_pgp:
            return item[4]


def fotog(name_pgp):
    indec = 'ФОТО'
    data = del_dob(indec)
    for item in data:
        if item[0] == name_pgp:
            return item[5]


def fio_tm(name):
    indec = 'ФИО ТМа'
    data = del_dob(indec)
    for item in data:
        if item[0] == name:
            return item[1]

    return 'Нет'


# if __name__ == '__main__':
#     name_pgp = "ИВАН"
#     print(hesteg(name_pgp))

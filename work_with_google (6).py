import os.path
import datetime

from googleapiclient.discovery import build
from google.oauth2 import service_account

import sbor_infi

SCOPES = ['не могу указать']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'vigruzka-plateg-d4a712e7c708.json')

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = 'не могу указать'
SAMPLE_RANGE_NAME = 'Лист1'

service1 = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
service2 = build('sheets', 'v4', credentials=credentials)

# class correc(StatesGroup):
#     nomber = State()
#     text = State()

list_znach_dla_pravki = {"СУММА": "I", "ОБЩАЯ СУММА": "J", "ТИП ПЛАТЕЖА": "P", "ПРОЕКТ": "R", "МЕНЕДЖЕР": "S",
                         "КАСАНИЯ": "T", "ТИМ-ЛИДЕР": "U", "РГП": "V", "НОМЕР ЛИДА": "F", "ДАТА ЛИДА": "H",
                         "ГОРОД": "X", "ИСТОЧНИК ЛИДА": "AA", "ФИО ТМа (при наличии)": "AB", "НОМЕР ДОГОВОРА": "Z",
                         "ЮР ЛИЦО, КУДА ПОСТУПИЛА ОПЛАТА": "Q", "ФИО ПЛАТЕЛЬЩИКА": "AF", "ИНН ПЛАТЕЛЬЩИКА": "AG",
                         "ДОГОВОР":"AE"}


def column_to_index(column):
    """
    Преобразует буквенное обозначение столбца в числовой индекс (нумерация начинается с 0).
    """
    index = 0
    for char in column:
        index = index * 26 + (ord(char.upper()) - ord('A')) + 1
    return index - 1


def del_dob(indec, list_otpr):
    if "добавить" in indec:
        range_1 = 'БД!A1'
        array = {'values': [list_otpr]}
        service1.append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                        range=range_1,
                        valueInputOption='USER_ENTERED',
                        body=array).execute()


def del_dob1(indec, stolb, stroka, text):
    if "добавить" in indec:
        range_1 = f'БД!{stolb}{stroka}'
        print(range_1)
        array = {'values': [[text]]}
        service1.append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                        range=range_1,
                        valueInputOption='USER_ENTERED',
                        body=array).execute()

        # Изменение цвета ячейки
        sheet_id = 0  # ID листа, обычно первый лист имеет ID 0
        start_row_index = int(stroka) - 1
        end_row_index = start_row_index + 1
        start_column_index = column_to_index(stolb)
        end_column_index = start_column_index + 1

        requests = [{
            'updateCells': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': start_row_index,
                    'endRowIndex': end_row_index,
                    'startColumnIndex': start_column_index,
                    'endColumnIndex': end_column_index,
                },
                'rows': [{
                    'values': [{
                        'userEnteredFormat': {
                            'backgroundColor': {
                                'red': 1.0,
                                'green': 0.0,
                                'blue': 0.0,
                                'alpha': 1.0
                            }
                        }
                    }]
                }],
                'fields': 'userEnteredFormat.backgroundColor'
            }
        }]

        body = {
            'requests': requests
        }

        service2.spreadsheets().batchUpdate(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            body=body
        ).execute()


def del_dob2(indec, stolb, stroka):
    if "удалить" in indec:
        # print(f'БД!{stolb}{stroka}')
        batch_clear_values_request_body = {'ranges': [f'БД!{stolb}{stroka}']}
        request = service2.spreadsheets().values().batchClear(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                              body=batch_clear_values_request_body)
        request.execute()


def del_dob3(indec):
    if "взять инфу" in indec:
        data = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                    range="БД!A3:A").execute().get('values', [])
        # print(data)
        return data


def del_dob4(logi):
    datess = str(datetime.datetime.today().strftime("%d.%m.%Y %H:%M"))
    logi.insert(0, datess)
    range_1 = 'ЛОГИРОВАНИЯ!A2'
    array = {'values': [logi]}
    service1.append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                    range=range_1,
                    valueInputOption='USER_ENTERED',
                    body=array).execute()


def clear_now(id_sotrudnica, page_number, item_number, text):
    list_otpr = sbor_infi.sbor_infi(id_sotrudnica)
    ids_lid = list(list_otpr)[page_number]

    indec = "взять инфу"
    data = del_dob3(indec)

    for i in range(len(data)):
        if ids_lid == data[i][0]:
            stroka = i + 3

            stolb = list_znach_dla_pravki[item_number]
            indec = "удалить"
            del_dob2(indec, stolb, stroka)

            indec = "добавить"
            del_dob1(indec, stolb, stroka, text)


# def del_dob4(indec):
#     if "айди соощбения" in indec:
#         data = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                                                     range="БД!A3:A").execute().get('values', [])
#         data2 = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                                                     range="БД!AH3:AH").execute().get('values', [])
#         # print(data)
#         return data, data2
#
#
# def id_message(page_number, id_sotrudnica):
#     list_otpr = sbor_infi.sbor_infi(id_sotrudnica)
#     ids_lid = list(list_otpr)[page_number]
#     indec = "айди соощбения"
#     data = del_dob4(indec)
#
#     for i in range(len(data[0])):
#         if ids_lid == data[0][i][0]:
#             id_messages = data[1][i][0]
#             return id_messages


# if __name__ == '__main__':
#     indec = "взять инфу"
#     print(del_dob3(indec)[0])

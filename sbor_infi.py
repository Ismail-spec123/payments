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
    global dev_nom
    if "добавить" in indec:
        range_1 = 'БД!A1'
        array = {'values': [[]]}
        service1.append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                        range=range_1,
                        valueInputOption='USER_ENTERED',
                        body=array).execute()

    elif "взять инфу" in indec:
        # id_user = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
        #                                                       range="БД!C2:C").execute().get('values', [])

        data = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                              range="БД!A2:AG").execute().get('values', [])
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


def sbor_infi(id_sotrudnica):
    indec = "взять инфу"
    data = del_dob(indec)
    list_otpr = {}

    for i in range(len(data)):
        if id_sotrudnica == data[i][2]:

            if len(data[i]) > 21:
                list_otpr[data[i][0]] = [f"Дата: {data[i][1]}\n"
                                "\n"
                                f"1. {data[i][8]} (общая {data[i][9]})\n"
                                f"2. {data[i][15]}\n"
                                f"3. {data[i][17]}\n"
                                f"4.1. {data[i][18]} (количесвто касании:{data[i][19]}\n"
                                f"4.2. {data[i][20]}\n"
                                f"4.3. {data[i][21]}\n"
                                f"5. {data[i][5]}\n"
                                f"6. {data[i][7]}\n"
                                f"7. {data[i][23]}\n"
                                f"8. {data[i][26]} {data[i][27]}\n"
                                f"9. {data[i][25]}\n"
                                f"10. {data[i][16]}\n"
                                f"11. {data[i][31]}\n"
                                f"12. {data[i][32]}\n"
                                "\n"
                                f"Договор: {data[i][30]}\n"]
            else:
                list_otpr[data[i][0]] = [f"Дата: {data[i][1]}\n"
                                "\n"
                                f"1. {data[i][8]} (общая {data[i][9]})\n"
                                f"2. не заполнено\n"
                                f"3. не заполнено\n"
                                f"4.1. {data[i][18]}\n"
                                f"4.2. {data[i][20]}\n"
                                f"4.3. не заполнено\n"
                                f"5. не заполнено\n"
                                f"6. не заполнено\n"
                                f"7. не заполнено\n"
                                f"8. не заполнено\n"
                                f"9. не заполнено\n"
                                f"10. не заполнено\n"
                                f"11. не заполнено\n"
                                f"12. не заполнено\n"]

    return list_otpr

# if __name__ == '__main__':
#     id_sotrudnica = "1006018804"
#     list_key = list(sbor_infi(id_sotrudnica))
#     data = sbor_infi(id_sotrudnica)
#     for ids in list_key:
#         print(data[ids][0])
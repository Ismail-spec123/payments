import os.path

from googleapiclient.discovery import build
from google.oauth2 import service_account


SCOPES = ['не могу указать']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'proverochka-bc4abdec38b4.json')

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = 'не могу указать'
SAMPLE_RANGE_NAME = 'Лист1'

service1 = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
service2 = build('sheets', 'v4', credentials=credentials)


list_dol = ['БРГП', 'БРОП', 'РГП', 'ТИМ-ЛИДЕР +2', 'ТИМ-ЛИДЕР +1', 'ТИМ-ЛИДЕР +4', 'ТИМ-ЛИДЕР +3', 'ТИМ-ЛИДЕР/РГП',
            'ТИМ-ЛИДЕР/РГПадм', 'ДП', 'ТИМ-ЛИДЕР +1 (адм отпуск)', 'и.о. РГП', 'РОП', 'РД', 'ТИМ-ЛИДЕР/РД', 'и.о. РД', 'ТИМ-ЛИДЕР',
            'ФД', 'ДМ/ДА', 'ГД', "СТМ", "МПЦ", "ГД"]


def del_dob(indec):
    global dev_nom
    if "добавить" in indec:
        range_1 = 'Лист1!A1'
        array = {'values': [[]]}
        service1.append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                        range=range_1,
                        valueInputOption='USER_ENTERED',
                        body=array).execute()

    elif "проверка" in indec:
        aidi_sotrudnic = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                              range="БД!C2:C").execute().get('values', [])
        return aidi_sotrudnic

    elif "идентификация" in indec:
        name = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                    range="БД!A2:A").execute().get('values', [])
        aidi_sotrudnic = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                              range="БД!C2:C").execute().get('values', [])
        return name, aidi_sotrudnic

    elif "должности" in indec:
        name = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                    range="БД!A2:A").execute().get('values', [])
        aidi_sotrudnic = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                              range="БД!C2:C").execute().get('values', [])

        dolgnost_sotrudnica = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                                   range="БД!G2:G").execute().get('values', [])
        return name, aidi_sotrudnic, dolgnost_sotrudnica

    elif "хештег" in indec:
        name_hg = service2.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                    range="БД!A2:B").execute().get('values', [])
        return name_hg

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


def find_name_by_id(combined_list, id_sotrudnica):
    for item in combined_list:
        if item[1] == id_sotrudnica:
            return item[0]
    return "ID не найден"


def proverka_id_v_selom(id_sotrudnica):
    global otvet_proverci

    indec = "проверка"
    list_bd = del_dob(indec)

    for item in list_bd:
        if item[0] == id_sotrudnica:
            return 'Да'

    return 'Нет'


def find_dol_by_id(combined_list, id_sotrudnica):
    for item in combined_list:
        if item[1] == id_sotrudnica:
            return item[2]
    return "ID не найден"


def proverka_id(id_sotrudnica):

    otvet_proverci = proverka_id_v_selom(id_sotrudnica)

    indec = "должности"
    list_data_dolgnost = del_dob(indec)

    combined_list = [[list_data_dolgnost[0][i][0], list_data_dolgnost[1][i][0], list_data_dolgnost[2][i][0]] for i
                     in range(len(list_data_dolgnost[0]))]
    dol_sotr = find_dol_by_id(combined_list, id_sotrudnica)

    if otvet_proverci == 'Да' and dol_sotr in list_dol:
        indec = "идентификация"
        list_data_sotrudnica = del_dob(indec)

        combined_list = [[list_data_sotrudnica[0][i][0], int(list_data_sotrudnica[1][i][0])] for i in
                         range(len(list_data_sotrudnica[0]))]
        name_sotrudnica = find_name_by_id(combined_list, int(id_sotrudnica))

        return name_sotrudnica

    elif otvet_proverci == 'Да' and dol_sotr not in list_dol:
        name_sotrudnica = "Должность не соответствует, критериям"
        return name_sotrudnica

    else:
        name_sotrudnica = "Пользователь не зарегистрирован в системе"
        return name_sotrudnica

from dataclasses import dataclass
from lib.excel_application import ExcelApplication

@dataclass
class KeyInfo:
    id: int = 0
    target_type: str = ''
    do: str = ''
    do_date: str = ''
    chk: str = ''
    chk_date: str = ''
# main
year_list = ['2019', '2020', '2021']
year_info = {}
for year in year_list:
    key_dict = {}
    for index in range(15):
        ids_dir = str(index * 100 + 1).zfill(4)
        excel_file = f'../ヒヤリハット_{year}_{ids_dir}.xlsm'
        print(excel_file)
        app = ExcelApplication(__file__)
        app.open(excel_file)
        app.select_work_sheet('Analysis Sheet')
        target_type_list = app.get_row_value_list('C', '対象区分')
        for (row, target_type) in target_type_list:
            key_tmp = KeyInfo()
            key_tmp.id = app.get_value(row, 'A')
            key_tmp.target_type = target_type
            key_tmp.do = app.get_value(row, 'AC')
            key_tmp.do_date = app.get_value(row, 'AD')
            key_tmp.chk = app.get_value(row, 'AE')
            key_tmp.chk_date = app.get_value(row, 'AF')
            key_dict[key_tmp.id] = key_tmp
        app.close()
    year_info[year] = key_dict
year_info2 = {}
for year in year_list:
    excel_file2 = f'../Final deliverable dataset v2({year}).xlsx'
    app2 = ExcelApplication(__file__)
    app2.open(excel_file2)
    app2.select_work_sheet('Final deliverable v2')
    id_list = app2.get_row_value_list('A', 'ID')
    key_list = []
    for (row, id) in id_list:
        key_tmp = KeyInfo()
        key_tmp.id = id
        key_tmp.do = app2.get_value(row, 'B')
        key_tmp.do_date = app2.get_value(row, 'C')
        key_tmp.chk = app2.get_value(row, 'D')
        key_tmp.chk_date = app2.get_value(row, 'E')
        key_list += [key_tmp]
    app2.close()
    year_info2[year] = key_list
for year, key_list2 in year_info2.items():
    print(f'[{year}]')
    for key2 in key_list2:
        key = year_info[year].get(key2.id)
        if key is None:
            print(f'★一覧あり＆解析なし★ {key2}') if key2.do != 'None' else 'pass'
            continue
        if key.target_type == '対象外':
            print(f'★対象外で一覧あり★ {key}') if key2.do != 'None' else 'pass'
            continue
        stat_do = key2.do == key.do
        stat_do_date = key2.do_date == key.do_date
        stat_chk = key2.chk == key.chk
        stat_chk_date = key2.chk_date == key.chk_date
        if stat_do and stat_do_date and stat_chk and stat_chk_date:
            continue
        print(f'★担当者不一致★ id:{key.id},do:({key.do},{key2.do})') if not stat_do else 'pass'
        print(f'★担当者日付不一致★ id:{key.id},do_date:({key.do_date},{key2.do_date}),do:{key2.do}') if not stat_do_date else 'pass'
        print(f'★ダブル不一致★ id:{key.id},chk:({key.chk},{key2.chk})') if not stat_chk else 'pass'
        print(f'★ダブル日付不一致★ id:{key.id},chk_date:({key.chk_date},{key2.chk_date}),chk:{key2.chk}') if not stat_chk_date else 'pass'

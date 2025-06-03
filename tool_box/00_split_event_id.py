# (仕様)
# ・ヒヤリハット_2019_0001.txtを作成
# ・No.とevent_idのリスト(100件分)
# ・2019～2021 and 0001～1401
import os
import pyperclip
from lib.common import get_list, put_list, copy_file

def get_event_id_from_clip():
    # get text from cripboad
    text_import = pyperclip.paste()
    text_list = text_import.split('\n')
    text_list = [s.replace('\r', '') for s in text_list]
    # anal clipboard info
    event_id = text_list[0]
    event_id = event_id if len(event_id) in [6, 7] and event_id.isnumeric() else None
    return event_id
def create_year_id_dict():
    # event info from event_id
    path_event_id = '../event_id'
    print(os.listdir(path_event_id))
    event_id_files = os.listdir(path_event_id)
    event_id_files = [f for f in event_id_files if os.path.isfile(os.path.join(path_event_id, f))]
    event_id_dict = {}
    for file in event_id_files:
        if 'idx' not in file:
            continue
        year = file.split('_')[2]
        event_id_list = get_list(os.path.join(path_event_id, file))
        dict_tmp = {f'{year}_{x.split()[0]}': x.split()[1] for x in event_id_list}
        event_id_dict = {**event_id_dict, **dict_tmp}
    return event_id_dict
def get_id_parent(id):
    id_int = int(id)
    count = (id_int - 1)//100
    count *= 100
    count += 1
    ids_dir = str(count).zfill(4)
    return ids_dir
# event info from event_id
year_id_dict = create_year_id_dict()
print(year_id_dict)
id_parent_dict = {}
for year_id, event_id in year_id_dict.items():
    tmp = year_id.split('_')
    year = tmp[0]
    id = tmp[1]
    id_parent = get_id_parent(id)
    if id_parent_dict.get(f'{year}_{id_parent}') == None:
        id_parent_dict[f'{year}_{id_parent}'] = [f'{id}\t{event_id}']
    else:
        id_parent_dict[f'{year}_{id_parent}'] += [f'{id}\t{event_id}']
print(id_parent_dict)
for id_parent, event_is_list in id_parent_dict.items():
    list_file = f'../ヒヤリハット_{id_parent}.txt'
    print(list_file)
    print(event_is_list)
    put_list(list_file, event_is_list)
    year = id_parent.split('_')[0]
    src_excel_file = f'../_ヒヤリハット_{year}_nnnn.xlsm'
    dst_excel_file = f'../ヒヤリハット_{id_parent}.xlsm'
    copy_file(src_excel_file, dst_excel_file) if not os.path.exists(dst_excel_file) else 'pass'

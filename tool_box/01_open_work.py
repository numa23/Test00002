import os
import pyperclip
from lib.common import *

# get text from cripboad
text_import = pyperclip.paste()
text_list = text_import.split('\n')
text_list = [s.replace('\r', '') for s in text_list]
# anal clipboard info
event_id = text_list[0]
if len(event_id) != 6 or event_id.isnumeric() != True:
    print('error:not event_id text!!')
    exit()
# event info from event_id
path_event_id = '../event_id'
print(os.listdir(path_event_id))
event_id_files = os.listdir(path_event_id)
event_id_files = [f for f in event_id_files if os.path.isfile(os.path.join(path_event_id, f))]
event_id_dict = {}
for file in event_id_files:
    year = file.split('_')[2]
    event_id_list = get_list(os.path.join(path_event_id, file))
    dict_tmp = {x.split()[1]: f'{year}_{x.split()[0]}' for x in event_id_list}
    event_id_dict = {**event_id_dict, **dict_tmp}
event_info = event_id_dict.get(event_id)
if event_info is None:
    print(f'error:事象ID({event_id})はevent_id_listに存在しません!!')
    exit()
print(event_info)
# creat target folder
year = event_info.split('_')
id = year[1]
year = year[0]
id_int = int(id)
count = (id_int - 1)//100
count *= 100
count += 1
ids_dir = str(count).zfill(4)
print(f'year:{year},ids_dir:{ids_dir},id:{id}')
target_path = f'..\work\{year}\{ids_dir}'
mkdir(target_path)

exec(f'explorer {target_path}')
exec(f'start ../ヒヤリハット_{year}_{ids_dir}.xlsm')

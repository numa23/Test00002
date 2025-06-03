import sys
import os
import pyperclip
from tkinter import messagebox
from dataclasses import dataclass
from lib.excel_application import ExcelApplication
from lib.common import put_list, copy_file, mkdir, copy_dir

@dataclass
class KeyInfo:
    row: int = 0
    id: int = 0
    event_id: int = 0
    update: str = ''
del_ret = lambda x: x.replace('\n', '')
del_none = lambda x: x.replace('None', '')
del_key = lambda x, key: x.replace(key, '')
trim = lambda x: str.strip(x)
split_bar = lambda x: x.split('_')[0]
chg_ids_dir = lambda id: ((int(id) - 1) // 100) * 100 + 1
rounded = lambda x, y: int((x * 10 ** y) + 0.5) / 10 ** y
isnumeric = lambda x: str(x).replace('.', '').isnumeric()
def get_svn_path():
    svn_path = ''
    try:
        svn_path = app.get_yaml_info('path', 'svn_path')
    except:
        clip_text = pyperclip.paste()
        clip_list = clip_text.split(': ')
        if clip_list[0] != 'svn_path' or len(clip_list) != 2:
            print(f'clip_list:{clip_list}')
        else:
            svn_path = trim(clip_list[1])
            yaml_list = ['path:', f"  svn_path: '{svn_path}'"]
            put_list('svn_path.yaml', yaml_list)
    return svn_path
def get_range_value(sec_range, value, unit):
    _sec_range = {key: trim(_range.replace(unit, '')) for key, _range in sec_range.items()}
    _sec_range = {key: _range.replace('<', '-9999.0') for key, _range in _sec_range.items()}
    _sec_range = {key: (float(_range.split('-')[0]), float(_range.split('-')[1])) for key, _range in _sec_range.items()}
    print(f'_sec_range:{_sec_range}')
    if value == 'not applicable':
        return value
    index = [key for key, (st, ed) in _sec_range.items() if st <= float(value) <= ed][0]
    return sec_range[index]
def anal_arg():
    is_demo = False
    if len(sys.argv) == 2 and sys.argv[1] == 'demo':
        is_demo = True
        excel_file = '../ヒヤリハット_2020_0001.xlsm'
        excel_file2 = '../Final deliverable dataset v2(2020).xlsx'
    else:
        if len(sys.argv) < 3:
            print('引数にYEAR(2020)とID(xxxx)を指定して！')
            exit()
        year = sys.argv[1]
        id = sys.argv[2]
        if not year.isnumeric() or not id.isnumeric():
            print('error:引数に数字文字列を指定して！')
            exit()
        if len(year) != 4 or len(id) > 4:
            print('error:引数に指定文字列長を指定して！')
            exit()
        ids_dir = chg_ids_dir(id)
        ids_dir = str(ids_dir).zfill(4)
        excel_file = f'../ヒヤリハット_{year}_{ids_dir}.xlsm'
        excel_file2 = f'Final deliverable dataset v2({year}).xlsx'
    return excel_file, excel_file2, is_demo, year, ids_dir
# main
excel_file, excel_file2, is_demo, year, ids_dir = anal_arg()
app = ExcelApplication(__file__)
if not is_demo:
    svn_path = get_svn_path()
    if svn_path == '':
        msg = 'svn配下の(00_exec_at_svn.py)を実行してね!!'
        print(msg)
        messagebox.showwarning('警告', msg)
        exit()
    print(f'svn_path:{svn_path}')
    excel_file2 = os.path.join(svn_path, excel_file2)
print(f'excel_file:{excel_file}')
if not os.path.exists(excel_file):
    print(f'error:excel_file not exist!! {excel_file}')
    exit()
print(f'excel_file2:{excel_file2}')
if not os.path.exists(excel_file2):
    print(f'error:excel_file2 not exist!! {excel_file2}')
    exit()
yaml_dict = app.get_yaml_all()
print(yaml_dict)
app.open(excel_file)
app.select_work_sheet('Analysis Sheet')
header_dict = app.get_column_value_dict(3)
col_name_dict = {value: key for key, value in header_dict.items() if value != ''}
print(col_name_dict)
create_list = app.get_row_value_list('AA', '追加')
print(create_list)
key_list = []
for index, (row, value) in enumerate(create_list):
    key_tmp = KeyInfo()
    key_tmp.row = row
    key_tmp.id = app.get_value(row, 'A')
    key_tmp.event_id = app.get_value(row, 'B')
    update = app.get_value(row, col_name_dict['更新'])
    key_tmp.update = value if update == 'None' else update
    key_list += [key_tmp]
print(f'key_list:{key_list}')

app2 = ExcelApplication(__file__)
app2.open(excel_file2)
app2.select_work_sheet('Final deliverable v2')
header_dict2 = app2.get_column_value_dict(1)
col_name_dict2 = {value: key for key, value in header_dict2.items() if value != ''}
print(col_name_dict2)
id_list = app2.get_row_value_list('A', 'ID')
id2row_dict = {id: row for row, id in id_list}
is_update = False
update_list = []
for key_info in key_list:
    src_row = key_info.row
    tgt_row = id2row_dict.get(key_info.id)
    update = del_none(app2.get_value(tgt_row, col_name_dict2['update']))
    print(f'update:{update},key_info.update:{key_info.update}')
    if update == '' or update < key_info.update:
        update_list += [key_info.id.zfill(4)]
        is_update = True
        print(f'update id:{key_info.id},event_id:{key_info.event_id},update:{key_info.update}')
        app2.get_cell(tgt_row, col_name_dict2['update']).value = key_info.update
        for col_name, tgt_col in col_name_dict2.items():
            item = yaml_dict['convert_table'][col_name]
            if item['type'] == 'pass':
                continue
            src_col_name = item['src']
            if src_col_name[0] == '$':
                key = yaml_dict['double_input'][src_col_name]
                print(f"key:{key}")
                for name in key.split(','):
                    src_col = col_name_dict[name]
                    value = del_none(del_ret(app.get_value(src_row, src_col)))
                    print(f"valuevalue:{value}")
                    if value in ['―', 'ー']:
                        continue
                    src_col_name = name
            src_col = col_name_dict[src_col_name]
            value = del_none(del_ret(app.get_value(src_row, src_col)))
            if item['type'] == 'copy':
                app2.get_cell(tgt_row, tgt_col).value = value
            elif item['type'] == 'round':
                value = '{:.2f}'.format(rounded(float(value), 2)) if isnumeric(value) else value
                app2.get_cell(tgt_row, tgt_col).value = value
            elif item['type'] == 'code':
                app2.get_cell(tgt_row, tgt_col).value = value.split(':')[0]
            elif item['type'] == 'value':
                print(f'value:{value}')
                app2.get_cell(tgt_row, tgt_col).value = trim(value.split(':')[1])
            elif item['type'] == 'sec_range':
                print(f'value:{value}')
                app2.get_cell(tgt_row, tgt_col).value = get_range_value(yaml_dict['sec_range'], value, 'sec')
            elif item['type'] == 'speed_range':
                print(f'value:{value}')
                app2.get_cell(tgt_row, tgt_col).value = get_range_value(yaml_dict['speed_range'], value, 'km/h')
app2.save() if is_update else 'pass'
print('not update!!') if not is_update else 'pass'
app2.close()
app.close()
# submit excel_work_sheet and work_folder
if is_update and not is_demo:
    base_dir = f'work/{year}/{ids_dir}'
    src_dir = os.path.join('../', base_dir)
    dst_dir = os.path.join(svn_path, base_dir)
    mkdir(dst_dir)
    file_list = os.listdir(src_dir)
    file_list = [f for f in file_list if os.path.isfile(os.path.join(src_dir, f))]
    print(f'update_list:{update_list}')
    print(f'file_list:{file_list}')
    for file in file_list:
        if split_bar(file) not in update_list:
            continue
        copy_file(os.path.join(src_dir, file), dst_dir)
    excel_file_dst = os.path.join(svn_path, del_key(excel_file, '../'))
    copy_file(excel_file, excel_file_dst)

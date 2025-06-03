import os
import pyperclip
from lib.common import *
from lib.yaml_loader import YamlLoader

def change_color(ws, row, color):
    if color is None:
        return
    from openpyxl.styles import PatternFill
    #fill = PatternFill(start_color='FF0000', fill_type = 'solid')
    fill = PatternFill(start_color=color, fill_type = 'solid')
    #ws['A'][index].fill = fill
    #ws['B'][index].fill = fill
    ws.cell(row=row, column=1).fill = fill
    ws.cell(row=row, column=2).fill = fill
def font_bold(ws, row, column=1):
    from openpyxl.styles import Font
    font = Font(bold=True)
    ws.cell(row=row, column=column).font = font
def font_bold_color(ws, row, column, color):
    from openpyxl.styles import Font
    font = Font(bold=True, color=color)
    ws.cell(row=row, column=column).font = font
def draw_frame_0(ws, row):
    from openpyxl.styles.borders import Border, Side
    side = Side(style='thin', color='000000')
    border = Border(top=side, right=side, left=side)
    ws.cell(row=row, column=1).border = border
    ws.cell(row=row, column=2).border = border
def draw_frame_1(ws, row):
    from openpyxl.styles.borders import Border, Side
    side = Side(style='thin', color='000000')
    border = Border(right=side, left=side)
    ws.cell(row=row, column=1).border = border
    border = Border(top=side, right=side, left=side)
    ws.cell(row=row, column=2).border = border
def draw_frame_2(ws, row):
    from openpyxl.styles.borders import Border, Side
    side = Side(style='thin', color='000000')
    border = Border(top=side)
    ws.cell(row=row, column=1).border = border
    ws.cell(row=row, column=2).border = border

def change_cell_color(ws, row, column, color):
    if color is None:
        return
    from openpyxl.styles import PatternFill
    fill = PatternFill(start_color=color, fill_type = 'solid')
    ws.cell(row=row, column=column).fill = fill
def draw_cell_frame(ws, row, column):
    from openpyxl.styles.borders import Border, Side
    side = Side(style='thin', color='000000')
    border = Border(top=side, bottom=side, right=side, left=side)
    ws.cell(row=row, column=column).border = border
def get_column_from_string(column_str):
    return openpyxl.utils.column_index_from_string(column_str)
def get_row_item_posi(matrix_info):
    row_item_posi = {}
    for _, info in matrix_info.items():
        column_str = str(info['column'])
        column = get_column_from_string(column_str)
        row_items = info['row_items']
        if row_items != None:
            for item in row_items:
                if row_item_posi.get(item) == None:
                    row_item_posi[item] = [column]
                else:
                    row_item_posi[item] += [column]
    return row_item_posi
def put_text_and_color(ws, row, columns, text, color):
    if len(columns) == 0:
        return
    for column in columns:
        ws.cell(row=row, column=column).value = text
        change_cell_color(ws, row, column, color)

# get text from cripboad
text_import = pyperclip.paste()
text_list = text_import.split('\n')
text_list = [s.replace('\r', '') for s in text_list]
# anal clipboard info
event_id = ''
event_year = ''
if len(text_list) > 10 and '事象ID' in text_list[0] and 'ヒヤリハット' in text_list[6]:
    out_type = 'tag_list'
    event_id = text_list[0].split('\t')[1]
    print(f'tag list!! event_id:{event_id}')
elif len(text_list) > 10 and 'IncidentID' in text_list[2]:
    out_type = 'export_csv'
    event_id = text_list[2].split(',')[1]
    print(f'export csv!! event_id:{event_id}')
else:
    print('error:not valid text!!')
    print('copy text from tag_list.txt or export.csv!!')
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
# create target file
if out_type == 'tag_list':
    out_file_name = f'{id}_tag_{event_id}.xlsx'
elif out_type == 'export_csv':
    out_file_name = f'{id}_DRMeasurePlugIn_{event_id}.csv'
else:
    print('error:想定外の動作!!')
    exit()
out_file_name = os.path.join(target_path, out_file_name)
if out_type == 'tag_list':
    yaml = YamlLoader('01_import.yaml')
    bg_color_info = yaml.get_yaml_dict('bg_color')
    palette_info = yaml.get_yaml_dict('palette')
    matrix_info = yaml.get_yaml_dict('matrix')
    import openpyxl
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = 'tag_list'
    len_list_a = []
    len_list_b = []
    #default_color = 'FFFFDD'
    default_color = palette_info['default']
    current_color = default_color
    row_item_posi = get_row_item_posi(matrix_info)
    print(f'row_item_posi:{row_item_posi}')
    cnv_exist_tbl = ['全体コメント', '法令違反項目']
    dict_4th = {}
    for row, tsv_info in enumerate(text_list, start=1):
        item_list = tsv_info.split('\t')
        if item_list[0] == '交通参加者番号':
            if item_list[1] == '1':
                item_list[0] += ' (自車)'
            elif item_list[1] == '2':
                item_list[0] += ' (相手)'
            else:
                print(f'item_list[0]:{item_list[0]},item_list[1]:{item_list[1]}')
        for column, item_info in enumerate(item_list, start=1):
            sheet.cell(row=row, column=column).value = item_info
        if len(item_list) == 2:
            if item_list[0] != '':
                color = bg_color_info.get(item_list[0])
                if color is None:
                    current_color = default_color
                else:
                    current_color = palette_info[color]
            len_list_a += [len(item_list[0])]
            len_list_b += [len(item_list[1])]
            if item_list[0] != '' or item_list[1] != '':
                if item_list[0] != '':
                    draw_frame_0(sheet, row)
                else:
                    draw_frame_1(sheet, row)
                change_color(sheet, row, current_color)
                columns = row_item_posi.get(item_list[0])
                if columns is not None:
                    for column in columns:
                        if dict_4th.get(column) is None:
                            dict_4th[column] = [[item_list[0], item_list[1], current_color]]
                        else:
                            dict_4th[column] += [[item_list[0], item_list[1], current_color]]
                    if item_list[0] in cnv_exist_tbl:
                        item_list[1] = '〇' if item_list[1].replace(' ', '') != '' else '―'
                    put_text_and_color(sheet, row, columns, item_list[1], current_color)
                if '交通参加者番号' in item_list[0]:
                    font_bold(sheet, row)
            else:
                draw_frame_2(sheet, row)
    draw_frame_2(sheet, row)
    max_row = row
    adjusted_width = 30
    sheet.column_dimensions['A'].width = max(len_list_a) * 2.07
    sheet.column_dimensions['B'].width = max(len_list_b) * 2.07
    print(f'matrix_info:{matrix_info}')
    for key, info in matrix_info.items():
        column_str = str(info['column'])
        column = get_column_from_string(column_str)
        color = info['color']
        if color is None:
            _color = default_color
        else:
            _color = palette_info[color]
        print(f'column:{column},info:{info}')
        sheet.cell(row=1, column=column).value = key
        draw_cell_frame(sheet, row=1, column=column)
        change_cell_color(sheet, row=1, column=column, color=_color)
        key = key + '  ' if key == '天候' else key
        sheet.column_dimensions[column_str].width = (len(key) + 1) * 2.0
        if info.get('help_text') != None:
            sheet.cell(row=2, column=column).value = info['help_text']
            change_cell_color(sheet, row=2, column=column, color=palette_info['check_movie'])
    print(f'dict_4th:{dict_4th}')
    row = max_row + 4
    for key, info in matrix_info.items():
        column_str = str(info['column'])
        column = get_column_from_string(column_str)
        color = info['color']
        current_color = palette_info[color]
        put_text_and_color(sheet, row, [1], key, current_color)
        font_bold(sheet, row)
        draw_cell_frame(sheet, row=row, column=1)
        help_text = info.get('help_text')
        if help_text is not None:
            sheet.cell(row=row, column=2).value = f' ※{help_text}'
            font_bold(sheet, row, 2)
            font_bold_color(sheet, row, 2, 'FF0000')
        row += 1
        items = dict_4th.get(column)
        if items is not None:
            for item in items:
                put_text_and_color(sheet, row, [1], item[0], item[2])
                put_text_and_color(sheet, row, [2], item[1], item[2])
                row += 1
        row += 1
    sheet.freeze_panes = 'C2'
    wb.save(out_file_name)
elif out_type == 'export_csv':
    put_list(out_file_name, text_list)
print(f'({out_file_name})を生成しました!!')
# 距離、速度、THW、TTC 計算
if out_type == 'export_csv':
    import csv
    import math
    start_index = 0
    event_begin = 0
    xs = []
    ys = []
    ts = []
    vs = []
    with open(out_file_name, encoding='utf-8') as f:
        rows = csv.reader(f)
        for index, row in enumerate(rows):
            if len(row) == 0:
                continue
            if 'A_X[m]' in row:
                start_index = index + 1
            if start_index > 0:
                if row[10] == '0':
                    event_begin = index
            if event_begin > 0:
                xs += [row[1]]
                ys += [row[2]]
                ts += [row[10]]
                vs += [row[11]]
    if xs[0] == '':
        print('error:時間0での距離(x,y)が存在しない!!')
        exit()
    ls = [math.sqrt(float(x)**2 + float(y)**2) for x, y in zip(xs, ys) if x != '']
    ls_min = min(ls)
    event_begin = 0
    event_end = [index for index, l in enumerate(ls) if l == ls_min][0]
    print(f'min(ls):{ls_min}, event_end:{event_end}, time:{ts[event_end]}')
    t_event_end = float(ts[event_end])
    if t_event_end <= 4.3:
        fix_t = 0
        fix_index = 0
    else:
        fix_t = t_event_end - 4.3
        #fix_index = [index for index, t in enumerate(ts) if float(t) > fix_t][-1] # NG code
        for index, t in enumerate(ts):
            if float(t) > fix_t:
                fix_index = index
                break
    print(f'fix_t:{fix_t},fix_index:{fix_index}')
    header = f'p,x,y,t,l,dl,dt,v,dv,thw,ttc'
    print(header)
    tsv_list = [header.replace(',' ,'\t')]
    for index, l in enumerate(ls):
        x, y, t, l, v = float(xs[index]), float(ys[index]), float(ts[index]), float(ls[index]), float(vs[index])
        if index + 1 == len(ls):
            #x2, y2, t2 = x, y, float(ts[index + 1])
            x2, y2, t2 = x, y, t
        else:
            x2, y2, t2 = float(xs[index + 1]), float(ys[index + 1]), float(ts[index + 1])
        #l = math.sqrt(x**2 + y**2)
        dl = math.sqrt((x - x2)**2 + (y - y2)**2)
        dt = t2 - t
        # dx / dt = 相対速度(dv)、 x / v = THW、x / dv = TTC
        not_zero = lambda x: x if x > 0 else 1e-10
        dv = dl / not_zero(dt) * 3.6
        thw = l / not_zero(v / 3.6)
        ttc = l / not_zero(dv / 3.6)
        body = f'{"o" if index==fix_index else "*" if index==event_end else "-"},{x},{y},{t},{l},{dl},{dt},{v},{dv},{thw},{ttc}'
        if index==fix_index:
            l_fix, v_fix, dv_fix, thw_fix, ttc_fix = l, v, dv, thw, ttc
        print(body)
        tsv_list += [body.replace(',' ,'\t')]
        if index + 1 == len(ls):
            break
    thw_fix = thw_fix if v_fix > 0.0 else 'not applicable'
    ttc_fix = ttc_fix if dv_fix > 0.0 else 'not applicable'
    tsv_list += []
    tsv_list += ['距離\t速度\t相対速度\tTHW\tTTC']
    tsv_list += [f'{l_fix}\t{v_fix}\t{dv_fix}\t{thw_fix}\t{ttc_fix}']
    out_file_name = f'{id}_calc_sheet_{event_id}.tsv'
    out_file_name = os.path.join(target_path, out_file_name)
    put_list(out_file_name, tsv_list)
    print(f'({out_file_name})を生成しました!!')
exec(f'explorer {target_path}')
excel_worksheet = f'ヒヤリハット_{year}_{ids_dir}.xlsm'
local_excel = os.path.join('../', excel_worksheet)
if not os.path.exists(local_excel):
    yaml = YamlLoader('svn_path.yaml')
    svn_excel = os.path.join(yaml.get_yaml_info('path', 'svn_path'), excel_worksheet)
    copy_file(svn_excel, local_excel)
exec(f'start {local_excel}')

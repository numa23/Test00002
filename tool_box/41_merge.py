import datetime
import os
from lib.common import remove_file, copy_file, move_file
from lib.excel_application import ExcelApplication

del_none = lambda x: x.replace('None', '')
trim = lambda x: str.strip(x)
get_date_str = lambda : datetime.datetime.now().strftime('%Y%m%d')
date_str = get_date_str()
excel_file_tmpl = '../YYYYMMDD Final deliverable dataset v2(nnnn).xlsx'
excel_file_final = excel_file_tmpl.replace('YYYYMMDD', date_str)
excel_file_final = excel_file_final.replace('.xlsx', '_jp.xlsx')
print(f'excel_file_final:{excel_file_final}')
if os.path.exists(excel_file_final):
    remove_file(excel_file_final)
copy_file(excel_file_tmpl, excel_file_final)
app = ExcelApplication(__file__)
app.open(excel_file_final)
app.select_work_sheet('YYYYMMDD Final deliverable v2')
app.rename_work_sheet('YYYYMMDD Final deliverable v2'.replace('YYYYMMDD', date_str))
header_dict = app.get_column_value_dict(1)
col_name_dict = {value: key for key, value in header_dict.items() if value != ''}
print(f'col_name_dict:{col_name_dict}')
target_row_start = 2
target_row = target_row_start
counter = {'2019': [0,0,0], '2020': [0,0,0], '2021': [0,0,0]}
for year in ['2019', '2020', '2021']:
    excel_file2 = f'../Final deliverable dataset v2({year}).xlsx'
    app2 = ExcelApplication(__file__)
    app2.open(excel_file2)
    app2.select_work_sheet('Final deliverable v2')
    header_dict2 = app2.get_column_value_dict(1)
    col_name_dict2 = {value: key for key, value in header_dict2.items() if value != ''}
    #print(col_name_dict2)
    event_id_col = col_name_dict2['AMP_Case']
    id_list = app2.get_row_value_list('A', 'ID')
    for row, id in id_list:
        if app2.get_value(row, event_id_col) in ['', 'None']:
            continue
        print(f'{year},{id},{app2.get_value(row, event_id_col)}')
        counter[year][0] += 1
        counter[year][1] += 1 if app2.get_value(row, col_name_dict2['完了日']) not in ['', 'None'] else 0
        counter[year][2] += 1 if app2.get_value(row, col_name_dict2['チェック完了日']) not in ['', 'None'] else 0
        for name, target_col in col_name_dict.items():
            app.get_cell(target_row, target_col).value = del_none(app2.get_value(row, col_name_dict2[name]))
        target_row += 1
    app2.close()
app.save()
app.close()
total_count = target_row - target_row_start
excel_file_final_cnt = excel_file_final.replace('nnnn', str(total_count))
remove_file(excel_file_final_cnt)
move_file(excel_file_final, excel_file_final_cnt)
# convert jp to us
excel_file_final_cnt_us = excel_file_final_cnt.replace('_jp', '')
copy_file(excel_file_final_cnt, excel_file_final_cnt_us)
app3 = ExcelApplication(__file__)
yaml_dict = app.get_yaml_all()
item_list = [key for key in yaml_dict.keys()]
print(f'item_list:{item_list}')
app3.open(excel_file_final_cnt_us)
app3.select_work_sheet('YYYYMMDD Final deliverable v2'.replace('YYYYMMDD', date_str))
for name, col in col_name_dict.items():
    if name not in item_list:
        print(f'name:{name}')
        continue
    for row, _ in enumerate(range(total_count), start=2):
        value = trim(app3.get_value(row, col))
        print(f'row:{row},name:{name},value:{value}')
        app3.get_cell(row, col).value = yaml_dict[name][value]
app3.save()
app3.close()
print(f'col_name_dict:{col_name_dict}')
print(f'counter:{counter}')
sum = [0,0,0]
with open(f'../{date_str}_集計情報.txt', 'w', encoding='utf-8') as f:
    f.writelines(f'year\tbe\tdo\tchk\n')
    for year, values in counter.items():
        f.writelines(f'{year}\t{values[0]}\t{values[1]}\t{values[2]}\n')
        sum[0] += values[0]
        sum[1] += values[1]
        sum[2] += values[2]
    f.writelines(f'total\t{sum[0]}\t{sum[1]}\t{sum[2]}\n')

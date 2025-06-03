import os
import sys

if len(sys.argv) < 2:
    print('引数に複数の事象IDリストを指定して！')
    exit()
list_files = sys.argv[1:]
print(list_files)
list_cat = []
for list_file_in in list_files:
    with open(list_file_in, encoding='utf-8') as f:
        list_tmp = [s.rstrip() for s in f.readlines()]
        list_cat += list_tmp
#print(list_cat)
list_mul = list(set(list_cat))
#print(list_mul)
is_overlapping = len(list_cat) != len(list_mul)
if is_overlapping:
    def inc_count(dict, x):
        dict[x] += 1
    print('重複検出!!')
    id_count_dict = {x: 0 for x in list_cat}
    id_count_dict = {x: 0 for x in list_cat}
    [inc_count(id_count_dict, x) for x in list_cat]
    for key, count in id_count_dict.items():
        if count > 1:
            print(f'event_id:{key},count:{count}')
else:
    print('重複なし!!')

import os
import sys

if len(sys.argv) == 1:
    print('引数に事象IDリストを指定して！')
    exit()
max_len = 1200
list_file_in = sys.argv[1]
print(list_file_in)
with open(list_file_in, encoding='utf-8') as f:
    list_all = [s.rstrip() for s in f.readlines()]
print(list_all)
list_file_o = os.path.splitext(list_file_in)
list_file_o = f'{list_file_o[0]}_idx{list_file_o[1]}'
with open(list_file_o, mode='w', encoding='utf-8') as f:
    f.writelines([f'{str(idx).zfill(4)} {s}\n' for idx, s in enumerate(list_all, start=1)])

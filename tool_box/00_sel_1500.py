import os
import sys
import random

if len(sys.argv) == 1:
    print('引数に事象IDリストを指定して！')
    exit()
max_len = 1500
list_file_in = sys.argv[1]
print(list_file_in)
with open(list_file_in, encoding='utf-8') as f:
    list_all = [s.rstrip() for s in f.readlines()]
print(list_all)
sel_list = random.sample(list_all, max_len)
#list_1100.sort()
print(f'len:{len(sel_list)}')
print(sel_list)
list_file_o = os.path.splitext(list_file_in)
list_file_o = f'{list_file_o[0]}_{max_len}{list_file_o[1]}'
with open(list_file_o, mode='w', encoding='utf-8') as f:
    f.writelines([f'{s}\n' for s in sel_list])

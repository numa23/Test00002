def setup_input(template, replace_dic, output):
  with open(template) as f:
    s = f.read()
  for key, value in replace_dic.items():
    s = s.replace(key, value)
  with open(output, mode='w') as f:
    f.write(s)

from sys import argv

if 3 > len(argv):
  print('[usage]')
  print('python3 cnv_tsv2sna.py risk_estimator 999')
  print('')
  print('[argument]')
  print('risk_estimator 999 :: create sn_risk_estimator_999_001.yaml from tc_risk_estimator_999.tsv')
  print('')
  print('[tsv desc]')
  print('tc_risk_estimator_999.tsv :: tsv[0]:P001,tsv[1]:desc,tsv[2]:data_start_posi,tsv[3]-:data_area')
  print('')
  print('[explanation]')
  print('prepare template file sn_risk_estimator_tmp.yaml')
  print('$VALUE_01$ in template file is replaced with tsv[3].')
  exit()

#--------
# config
#--------
target = argv[1]                        # risk_estimator       #sn_risk_estimator_tmp.yaml
main = argv[2]                          # 001


import os

target_path = f'{target}/scenario/' if os.path.exists(f'{target}') else ''
fmt_path = target_path + ('fmt/' if os.path.exists(target_path + 'fmt') else '')
tsv_path = target_path + ('tsv/' if os.path.exists(target_path + 'tsv') else '')

print('target_path:', target_path)
print('fmt_path:', fmt_path)
print('tsv_path:', tsv_path)

test_case = tsv_path + f'tc_{target}_{main}.tsv'   # tc_risk_estimator_999.tsv

print(f'{test_case} {target} {main}')
#exit()

import csv

case = 0
fmt = 'fmt'
scenario = target
with open(test_case, newline='') as f:
  csv_list = csv.reader(f, delimiter='\t')
  for csv in csv_list:
    if len(csv) == 0:
      continue
    if csv[0][0] == '#':
      continue
    if csv[0] == 'fmt':
      fmt = csv[1]
      continue
    if csv[0] == 'scenario':
      scenario = csv[1]
      continue
    #print(csv)
    value_dic = {}
    value_dic['$CASE$'] = f'{csv[0]}'
    value_dic['$DESC$'] = f'{csv[1]}'
    index = 0
    posi_st = csv[2] if csv[2] != '' else '3'
    posi_ed = len(csv)
    #for item in csv[7:19]:
    for item in csv[int(posi_st):int(posi_ed)]:
      index += 1
      value_dic['$VALUE_{:02}$'.format(index)] = item.replace("'", '')
    #print(value_dic)
    case += 1
    case_no = '{:03}'.format(case)
    setup_input(fmt_path + f'sn_{scenario}_{fmt}.yaml', value_dic, target_path + f'sn_{target}_{main}_{case_no}_00.yaml')
    #print(f'sn_{target}_tmp.yaml')
    print(f'{csv[0]} : ' + f'sn_{target}_{main}_{case_no}_00.yaml')


import yaml
from sys import argv
import subprocess
import time
import os
import datetime

#---------
# version
#---------
ver_major = 0
ver_minor = 0
ver_sub = 0

version = f'{ver_major}.{ver_minor}.{ver_sub}'

'''
0.0.0	in production	ctrl_unit_test.py provisional release (unversioned)
'''

################################################################################
# parts functions

'''
def exec0(cmd_line):
    print('exec:' + cmd_line)
    ps = subprocess.run(cmd_line, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text=True)
    #ps = subprocess.run(cmd_line, shell = True)
    return ps
'''
def exec(cmd_line, dsp_flag=True):
    #print('exec:' + cmd_line)
    pipe = None if dsp_flag else subprocess.PIPE
    #ps = subprocess.run(cmd_line, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text=True)
    ps = subprocess.run(cmd_line, shell = True, stdout = pipe, stderr = pipe, text=True)
    return ps
def exec1(cmd_line):
    print('exec1:' + cmd_line)
    ps = subprocess.run(cmd_line, shell = True, text=True)
    return ps
def exec2(cmd_line):
    print('exec2:' + cmd_line)
    ps = subprocess.Popen(cmd_line, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    return ps
# do nothing func
def do_nothing():
    pass
def create_node_list():
    path = '.'
    files = os.listdir(path)
    dir_list = [d for d in files if os.path.isdir(os.path.join(path, d))]
    node_list = [d for d in dir_list if os.path.exists(os.path.join(d, 'scenario'))]
    node_list.sort()
    return node_list
def create_template_file(fmt_name, template):
    with open(fmt_name, 'w') as f:
        f.write(template)
def replace_key_on_file(file_name, dic):
    text_all = ''
    with open(file_name, 'r') as f:
        text_all = f.read()
    for key,value in dic.items():
        text_all = text_all.replace(key, value)
    with open(file_name, 'w') as f:
        f.write(text_all)
def chk_all_same(list):
    for item in list:
        if item != list[0]:
            return False
    return True
def check_serial_number(number_list):
    unmatch_count = 0
    index = int(number_list[0])
    for number in number_list:
        if index != int(number):
            if index < int(number):
                index += (int(number) - index)
            else:
                unmatch_count += 1
        index += 1
    return unmatch_count
def check_fix_length(check_list):
    if check_list == []:
        return []
    top_len = len(check_list[0])
    result_list = [True if len(x) == top_len else False for x in check_list]
    return result_list

# 'sn_xxxx_xxxx_001_001_00.yaml' & next -> [['001', '001', '00'], ['001', '002', '00']]
def get_case_pattern_list(node_name):
    node_name_path = f'{node_name}/'
    scenario_path = f'{node_name_path}scenario'
    files = os.listdir(scenario_path)
    file_list = [f for f in files if os.path.isfile(os.path.join(scenario_path, f))]
    case_pattern_list = [file.replace(f'sn_{node_name}_', '').replace('.yaml', '') for file in file_list]
    case_pattern_list.sort()
    return [case_pattern.split('_') for case_pattern in case_pattern_list]
# 'tc_xxxx_xxxx_001.tsv' & next -> ['001', '002', '003', '004', '005', '006']
def get_case_list(node_name):
    node_name_path = f'{node_name}/'
    tsv_path = f'{node_name}/scenario/tsv'
    files = os.listdir(tsv_path)
    case_list = [file.replace(f'tc_{node_name}_', '').replace('.tsv', '') for file in files]
    case_list.sort()
    return case_list
# [002-004,006] -> ['002','003','004','006']
def chg_range_info(range_info):
    range_info_new = []
    for range_item in range_info:
        if '-' in range_item:
            items = range_item.split('-')
            range_info_new += ['{:03}'.format(x) for x in range(int(items[0]), int(items[1]) + 1)]
        else:
            range_info_new += ['{:03}'.format(int(range_item))]
    return sorted(range_info_new)
def get_fmt_file(node_yaml_name):
    sepa_list = os.path.split(node_yaml_name)
    if not os.path.exists(sepa_list[0] + '/fmt'):
        return node_yaml_name + '_fmt.yaml'
    return sepa_list[0] + '/fmt/' + sepa_list[1] + '_fmt.yaml'
# func for report mode  to get items from dsp_xxxx_xxxx_001_010_00.log
def get_dsp_item(node_name, case, pat, sub):
    dsp_info_map = {}
    with open(f'{node_name}/log/dsp_{node_name}_{case}_{pat}_{sub}.log') as f:
        for line in f:
            if ':' not in line:
                continue;
            line = line.replace('\n', '')
            items = line.split(':', 1)
            dsp_info_map[items[0]] = items[1]
            if 'date_time' in line:
                break
    return dsp_info_map
# func for report mode to control print and write file
def report(text, mode='a', is_disp=True):
    print(text) if is_disp else do_nothing()
    global report_path_name
    with open(report_path_name, mode) as f:
        print(text, file=f)
# func for zip mode to get time stamp string
def get_zip_time_stamp(node_name):
    dsp_info_map = {}
    rpt_file = f'{node_name}/report/rpt_{node_name}_all.txt'
    if os.path.exists(rpt_file):
        with open(rpt_file) as f:
            for line in f:
                if ':' not in line:
                    continue;
                line = line.replace('\n', '')
                items = line.split(':', 1)
                dsp_info_map[items[0]] = items[1]
                if 'date_time' in line:
                    break
    time_stamp = dsp_info_map.get('date_time', '')
    if time_stamp == '':
        time_stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    else:
        time_stamp = datetime.datetime.strptime(time_stamp, '%Y/%m/%d %H:%M:%S').strftime('%Y%m%d_%H%M%S')
    return time_stamp
def get_unuse_variable(text):
    count = text.count('$')
    if count % 2 != 0:
        return [f'error! count:{count}']
    unuse_list = []
    posi_e = -1
    for index in range(count // 2):
        posi_s = text.index('$', posi_e + 1)
        posi_e = text.index('$', posi_s + 1)
        unuse_list += [text[posi_s:posi_e + 1]]
    return unuse_list
def check_next_same_string(string_list):
    err_list = []
    prv_string = ''
    for string in string_list:
        if string == prv_string:
            err_list += [string]
        prv_string = string
    return err_list

################################################################################
# template functions

def get_template_target(node_name):
    template = ''
    template += f"rosparam:(ret)  param_01: 'load param/$param_yaml_name_01$ $param_name_01$'(ret)(ret)"
    template += f"rosrun:(ret)  rosrun_01: '$project_name_01$ {node_name}_node.py'(ret)(ret)"
    template += f"rostopic:(ret)  echo_01: '$echo_msg_name_01$'(ret)  pub_01: '$pub_msg_name_01$ $pub_msg_class_01$'"
    return template.replace('(ret)', '\n')
def get_template_scenario(node_name):
    template = ''
    template += f"comand:(ret)  pub select: $VALUE_01$(ret)  pub sleep: $VALUE_02$(ret)  disp result: $VALUE_03$(ret)"
    template += f"info:(ret)  case: $CASE$(ret)  desc: $DESC$(ret)"
    template += f"result_tobe:(ret)  $RESULT_ITEM$: '$VALUE_04$'(ret)"
    template += f"yaml_name:(ret)  - param/param_file(ret)  - input/in_{node_name}_01  # msg name(ret)"
    template += f"param/param_file:(ret)  $PARAM_ITEM$: '$VALUE_05$'(ret)"
    template += f"input/in_{node_name}_01:(ret)  $TOPIC_ITEM$: '$VALUE_06$'"
    return template.replace('(ret)', '\n')
def get_template_test_data(node_name):
    template = ''
    template += f'P001(tab)sample test pattern (p001)(tab)(tab)["01"](tab)3.0(tab)False(tab)result_001(tab)param_001(tab)topic_001(ret)'
    template += f'P002(tab)sample test pattern (p002)(tab)(tab)["01"](tab)3.0(tab)False(tab)result_002(tab)param_002(tab)topic_002(ret)'
    return template.replace('(ret)', '\n').replace('(tab)', '\t')
def get_template_input(node_name):
    template = ''
    template += f"header:(ret)  seq: 2(ret)  stamp:(ret)    secs: 0(ret)    nsecs: 0(ret)  frame_id: ''(ret)topic_item: $TOPIC_ITEM$(ret)"
    return template.replace('(ret)', '\n')
def get_template_param(node_name):
    template = ''
    template += f"dummy_item: True(ret)"
    template += f"param_item: $PARAM_ITEM$(ret)"
    return template.replace('(ret)', '\n')
def get_template_output(node_name):
    template = ''
    template += f"items: (ret)    - (ret)    result_item: $RESULT_ITEM$(ret)"
    return template.replace('(ret)', '\n')


################################################################################
# application helper function

#'    nsecs: 100000000(tab)*     nsecs: 99999904' -> '    nsecs: 100000000(tab)      nsecs: 99999904'
def float_comparison_fix_error(result_item):
    ok_count = 0
    for index, x in enumerate(result_item['result_detail']):
        #if 'nsecs:' in x and '(tab)*' in x:
        if 'nsecs:' in x and '*' in x:
            y = x.strip()
            #ndrcs_list = y.split('(tab)*     ')
            ndrcs_list = y.split('    *     ')
            ndrcs_list = [z.replace('nsecs: ', '') for z in ndrcs_list]
            import math
            if eval(f'math.isclose(0.{ndrcs_list[0].zfill(9)}, 0.{ndrcs_list[1].zfill(9)}, abs_tol=0.01)'):
                ok_count += 1
                result_item['result_detail'][index] = x.replace('*', ' ')
    result_item['unmatch'] -= ok_count
    if result_item['unmatch'] == 0:
        result_item['judge'] = '(o)'

# func for report mode to get file text
def get_file_text(file_name):
    with open(file_name, encoding='utf8', newline='') as f:
        file_text = f.readlines()
    file_text = [x.replace('\n', '') for x in file_text]
    return file_text

# func for report mode to get diff result
def get_diff_result(diff_file_01, diff_file_02):
    #print(f'({diff_file_01})')
    text_list_01 = get_file_text(diff_file_01)
    #print(text_list_01)
    #print(f'({diff_file_02})')
    text_list_02 = get_file_text(diff_file_02)
    #print(text_list_02)
    max_len = max(len(text_list_01), len(text_list_02))
    get_text = lambda text_list, index: str(text_list[index]) if len(text_list) > index else ''
    comp_text = lambda text_01, text_02: '*' if text_01 != text_02 else ' '
    ng_count = 0
    diff_result = []
    for index in range(max_len):
        text_01 = get_text(text_list_01, index)
        text_02 = get_text(text_list_02, index)
        judge = comp_text(text_01, text_02)
        ng_count += 1 if judge == '*' else 0
        #print(f'{text_01.ljust(62)}{judge} {text_02}')
        diff_result += [f'{text_01.ljust(62)}{judge} {text_02}']
    return ng_count, diff_result

# func for report mode to create result_item map
def create_result_info(node_name, case_pattern_list):
    case_pattern_list = get_case_pattern_list(node_name) if case_pattern_list == None else case_pattern_list
    result_info = {}
    for case_pattern in case_pattern_list:
        result_item = {}
        case = case_pattern[0]
        pat = case_pattern[1]
        sub = case_pattern[2]
        diff_file_01 = f'{node_name}/report/analysis/out_{node_name}_{case}_{pat}_{sub}_tobe.yaml'
        diff_file_02 = f'{node_name}/report/analysis/out_{node_name}_{case}_{pat}_{sub}_asis.yaml'
        ng_count, diff_result = get_diff_result(diff_file_01, diff_file_02)
        '''
        diff_file = f'{node_name}/report/analysis/out_{node_name}_{case}_{pat}_{sub}_tobe.yaml '
        diff_file += f'{node_name}/report/analysis/out_{node_name}_{case}_{pat}_{sub}_asis.yaml'
        diff_result = exec('diff -u ' + diff_file, False).stdout.splitlines()
        ng_count_bai = 0
        for x in diff_result:
            ng_count_bai += 1 if x[0] in ('-', '+') and x[2] not in ('-', '+') else 0
       '''
        #result_item['judge'] = '(o)' if ng_count_bai == 0 else '(x)'
        result_item['judge'] = '(o)' if ng_count == 0 else '(x)'
        result_item['case'] = case
        result_item['pat'] = pat
        result_item['sub'] = sub
        #result_item['unmatch'] = ng_count_bai//2
        result_item['unmatch'] = ng_count
        dsp_info_map = get_dsp_item(node_name, case, pat, sub)
        result_item['time'] = dsp_info_map["date_time"]
        result_item['desc'] = [dsp_info_map[x] for x in dsp_info_map if 'P' in x][0]
        result_item['version'] = dsp_info_map.get('version', '0.0.0')
        #diff_result = exec('diff -y ' + diff_file, False).stdout.splitlines()
        #result_item['result_detail'] = [x.replace('      |\t','* ').replace('\t','(tab)', 1).replace('\t','') for x in diff_result]
        result_item['result_detail'] = diff_result
        result_info[f'{case} {pat} {sub}'] = result_item
        float_comparison_fix_error(result_item)
    return result_info

################################################################################
# application functions

#-----------------
# create node dir 
#-----------------
def create_node_dir(node_name, istemplate=True):
    node_list = create_node_list()
    if node_name in node_list:
        print('already exist:', node_name)
    else:
        node_name_path = f'{node_name}/'
        template = ['input', 'log', 'output', 'param', 'report', 'scenario', 'target']
        template += ['input/fmt', 'param/fmt', 'report/fmt', 'scenario/fmt', 'scenario/tsv']
        for dir in template:
            os.makedirs(f'{node_name_path}{dir}', exist_ok=True)
        if istemplate:
            create_template_file(f'{node_name_path}target/ros_{node_name}.yaml', get_template_target(node_name))
            create_template_file(f'{node_name_path}scenario/fmt/sn_{node_name}_fmt.yaml', get_template_scenario(node_name))
            create_template_file(f'{node_name_path}scenario/tsv/tc_{node_name}_001.tsv', get_template_test_data(node_name))
            create_template_file(f'{node_name_path}input/fmt/in_{node_name}_01_fmt.yaml', get_template_input(node_name))
            create_template_file(f'{node_name_path}param/fmt/param_file_fmt.yaml', get_template_param(node_name))
            create_template_file(f'{node_name_path}report/fmt/out_{node_name}_fmt.yaml', get_template_output(node_name))

#--------------------
# clear created file 
#--------------------
def clear_created_file(node_name, isall=False):
    node_list = create_node_list()
    if node_name in node_list:
        node_name_path = f'{node_name}/'
        template = ['input', 'log', 'output', 'param', 'report', 'report/analysis'] + (['scenario'] if isall else [])
        for dir in template:
            path = f'{node_name_path}{dir}'
            files = os.listdir(path)
            file_list = [f for f in files if os.path.isfile(os.path.join(path, f))]
            for file in file_list:
                os.remove(os.path.join(path, file))
                #print(os.path.join(path, file))
        print(f'clear {node_name} project!')
    else:
        print('not exist:', node_name)

#---------------------------
# copy node to another node 
#---------------------------
def copy_node_node(node_name, node_name2):
    node_list = create_node_list()
    if node_name not in node_list:
        print('not exist:', node_name)
        return
    if node_name2 in node_list:
        print('already exist:', node_name2)
        return
    import shutil
    create_node_dir(node_name2, istemplate=False)
    template = ['input/fmt', 'param/fmt', 'report/fmt', 'scenario', 'scenario/fmt', 'scenario/tsv', 'target']
    for dir in template:
        path = f'{node_name}/{dir}'
        path2 = f'{node_name2}/{dir}'
        files = os.listdir(path)
        file_list = [f for f in files if os.path.isfile(os.path.join(path, f))]
        for file in file_list:
            if dir in ['param/fmt']:
                shutil.copy(os.path.join(path, file), os.path.join(path2, file))
            else:
                file2 = file.replace(f'{node_name}', f'{node_name2}')
                shutil.copy(os.path.join(path, file), os.path.join(path2, file2))
            if dir in ['scenario','scenario/fmt']:
                dic = {f'input/in_{node_name}': f'input/in_{node_name2}'}
                replace_key_on_file(os.path.join(path2, file2), dic)

#------------------
# exec cnv_tsv2sna
#------------------
def exec_cnv_tsv2sna(node_name, range_info):
    node_list = create_node_list()
    if node_name in node_list:
        range_info = chg_range_info(range_info)
        case_list = get_case_list(node_name)
        if range_info != []:
            case_list = [x for x in case_list if x in range_info]
        for case in case_list:
            #print(f'python3 cnv_tsv2sna.py {node_name} {case}')
            exec(f'python3 cnv_tsv2sna.py {node_name} {case}')
    else:
        print('not exist:', node_name)

#-----------------------
# get scenario tsv info
#-----------------------
def get_scenario_tsv_info(node_name):
    path = f'{node_name}/scenario/tsv'
    files = os.listdir(path)
    file_list = [f for f in files if os.path.isfile(os.path.join(path, f))]
    tsv_file_info = {}
    import csv as csvobj
    for file in file_list:
        tsv_info = {}
        tsv_list = []
        with open(f'{path}/{file}', newline='') as f:
            tsv_reader = csvobj.reader(f, delimiter='\t')
            for index, tsv in enumerate(tsv_reader):
                if len(tsv) == 0:
                    continue
                if tsv[0][0] == '#':
                    continue
                if tsv[0] == 'fmt':
                    tsv_info['fmt'] = tsv[1]
                    continue
                if tsv[0] == 'scenario':
                    tsv_info['scenario'] = tsv[1]
                    continue
                tsv_list.append(tsv)
        tsv_info['tsv'] = tsv_list
        len_list = [len(tsv) for tsv in tsv_list]
        tsv_info['all_same'] = chk_all_same(len_list)
        tsv_info['len'] = len_list[0]
        tsv_file_info[file] = tsv_info
    tsv_file_list = sorted(tsv_file_info.items())
    return dict(tsv_file_list)

#---------------------
# check yaml scenario
#---------------------
def check_yaml_scenario(node_name, scenario_name):
    yml_info = {}
    true_key_list = ['comand', 'info', 'result_tobe', 'yaml_name']
    with open(f'{node_name}/scenario/fmt/{scenario_name}', 'r') as yml:
        scenario_yml = yaml.safe_load(yml)
    key_list = [key for key, item in scenario_yml.items()]
    if 'yaml_name' in key_list:
        true_key_list += [x for x in scenario_yml['yaml_name']]
    ng_list = []
    for true_key in true_key_list:
        if true_key not in key_list:
            ng_list += [true_key]
    yml_info['ng_list'] = ng_list
    yml_info['yml_obj'] = scenario_yml
    return yml_info

#-----------------------
# get scenario fmt info
#-----------------------
def get_scenario_fmt_info(node_name, sn_fmt_list):
    #val_list = []
    line_list = []
    tsv_file_info = {}
    for sn_fmt in sn_fmt_list:
        tsv_info = {}
        tsv_list = []
        with open(f'{node_name}/scenario/fmt/{sn_fmt}') as f:
            line_list = f.readlines()
        val_list = [line.replace(' ','').replace('\n','').replace("'",'') for line in line_list if '$VALUE_' in line]
        val_list = [x.split(':') for x in val_list]
        val_list = [x[1] for x in val_list]
        number_list = [x.replace('$VALUE_','').replace('$','') for x in val_list]
        tsv_info['number_list'] = number_list
        tsv_info['serial'] = check_serial_number(number_list)
        tsv_info['fix'] = check_fix_length(number_list)
        yml_info = check_yaml_scenario(node_name, sn_fmt)
        tsv_info['ng_list'] = yml_info['ng_list']
        tsv_info['yml_obj'] = yml_info['yml_obj']
        tsv_file_info[sn_fmt] = tsv_info
    tsv_file_list = sorted(tsv_file_info.items())
    return dict(tsv_file_list)

#--------------------
# get input fmt info
#--------------------
def get_input_fmt_info(node_name, scenario_obj, dir_name):
    input_fmt_info = {}
    key_list = [key for key, item in scenario_obj.items() if dir_name in key]
    for key in key_list:
        item_list = [x for x, y in scenario_obj.get(key).items()]
        key_fmt = key.replace(dir_name, f'{dir_name}/fmt')
        input_fmt = f"{node_name}/{key_fmt}_fmt.yaml"
        with open(input_fmt) as f:
            input_all = f.read()
        all_variable = get_unuse_variable(input_all)
        same_string = check_next_same_string(all_variable)
        ok_count = 0
        ng_count = 0
        err_info = ''
        for item in item_list:
            if item in input_all:
                ok_count += 1
                input_all = input_all.replace(item, 'dummy_value')
            else:
                ng_count += 1
                err_info += f'\t(?){item} is not in input file!'
        unuse_variable = get_unuse_variable(input_all)
        err_info +=  f'\t(?)unused variables!:{unuse_variable}' if unuse_variable != [] else ''
        err_info +=  f'\t(?)same string next to!:{same_string}' if same_string != [] else ''
        input_fmt_info[key] = err_info
    return input_fmt_info

#---------------------------
# get output(tobe) fmt info
#---------------------------
def get_output_fmt_info(node_name, scenario_obj, dir_name):
    output_fmt_info = {}
    '''
    key_list = [key for key, item in scenario_obj.items() if 'result_tobe' in key]
    print(key_list)
    for key in key_list:
    '''
    item_list = [x for x, y in scenario_obj.get('result_tobe').items()]
    #key_fmt = key.replace(dir_name, f'{dir_name}/fmt')
    output_fmt = f"{node_name}/report/fmt/out_{node_name}_fmt.yaml"
    with open(output_fmt) as f:
        input_all = f.read()
    all_variable = get_unuse_variable(input_all)
    same_string = check_next_same_string(all_variable)
    ok_count = 0
    ng_count = 0
    err_info = ''
    for item in item_list:
        if item in input_all:
            ok_count += 1
            input_all = input_all.replace(item, 'dummy_value')
        else:
            ng_count += 1
            err_info += f'\t(?){item} is not in input file!'
    unuse_variable = get_unuse_variable(input_all)
    err_info +=  f'\t(?)unused variables!:{unuse_variable}' if unuse_variable != [] else ''
    err_info +=  f'\t(?)same string next to!:{same_string}' if same_string != [] else ''
    output_fmt_info[f"report/out_{node_name}_fmt.yaml"] = err_info
    return output_fmt_info

#----------------
# check fmt file
#----------------
def check_fmt_file(node_name):
    template = ['scenario/tsv','scenario/fmt','scenario','input/fmt','param/fmt','report/fmt']
    print('--------------------')
    print(' check scenario tsv')
    print('--------------------')
    print('[check number of columns in tsv]')
    tsv_file_info = get_scenario_tsv_info(node_name)
    for key, info in tsv_file_info.items():
        #print(f"{key}:{tsv_info['all_same']}:{tsv_info['len']},{tsv_info.get('fmt')},{tsv_info.get('scenario')}")
        print('{} {}'.format('(o)' if info['all_same'] else '(x)', key))
    print('')
    print('--------------------')
    print(' check scenario fmt')
    print('--------------------')
    print('[check for fixed numeric length of variables]')
    sn_fmt_list = [y.get('scenario') if y.get('scenario') != None else node_name for x, y in tsv_file_info.items()]
    sn_fmt_list = list(set(sn_fmt_list))
    sn_fmt_list = [f'sn_{x}_fmt.yaml' for x in sn_fmt_list]
    scenario_fmt_info = get_scenario_fmt_info(node_name, sn_fmt_list)
    for key, info in scenario_fmt_info.items():
        print('{} {}'.format('(o)' if len(set(info['fix'])) == 1 else '(x)', key))
    print('')
    print('[sequential check of variables in scenario]')
    for key, info in scenario_fmt_info.items():
        print('{} {}'.format('(o)' if info['serial'] == 0 else '(x)', key))
    print('')
    print('[duplicate check for variables in scenarios]')
    for key, info in scenario_fmt_info.items():
        print('{} {}'.format('(o)' if len(set(info['number_list'])) == len(info['number_list']) else '(x)', key))
    print('')
    print('[yaml item name check in scenario]')
    for key, info in scenario_fmt_info.items():
        err_info = f"\tnot exist key:{info['ng_list']}" if info['ng_list'] != [] else ''
        print('{} {}{}'.format('(o)' if info['ng_list'] == [] else '(x)', key, err_info))
    print('')
    print('-----------------')
    print(' check input fmt')
    print('-----------------')
    print('[check input fmt file]')
    for key, info in scenario_fmt_info.items():
        sn_fmt = key
        input_fmt_info = get_input_fmt_info(node_name, info['yml_obj'], 'input')
        for input_fmt, error_info in input_fmt_info.items():
            print(('(o)' if error_info == '' else '(x)') + f'{sn_fmt} + {input_fmt}{error_info}')
    print('')
    print('-----------------')
    print(' check param fmt')
    print('-----------------')
    print('[check param fmt file]')
    for key, info in scenario_fmt_info.items():
        sn_fmt = key
        param_fmt_info = get_input_fmt_info(node_name, info['yml_obj'], 'param')
        for param_fmt, error_info in param_fmt_info.items():
            print(('(o)' if error_info == '' else '(x)') + f'{sn_fmt} + {param_fmt}{error_info}')
    print('')
    print('------------------------')
    print(' check output(tobe) fmt')
    print('------------------------')
    print('[check output(tobe) fmt file]')
    for key, info in scenario_fmt_info.items():
        sn_fmt = key
        output_fmt_info = get_output_fmt_info(node_name, info['yml_obj'], 'report')
        for output_fmt, error_info in output_fmt_info.items():
            print(('(o)' if error_info == '' else '(x)') + f'{sn_fmt} + {output_fmt}{error_info}')


'''
　・tsv - scenario
　・scenario - input
　・scenario - param
　・scenario - output
'''



#------------------------------
# make report from result data
#------------------------------
def make_report_from_result_data(node_name, case_pattern_list=None, title_on=True):
    global report_path_name
    node_list = create_node_list()
    if node_name in node_list:
        fmt_file = get_fmt_file(f'{node_name}/report/out_{node_name}')
        if os.path.isfile(fmt_file):
            result_info = create_result_info(node_name, case_pattern_list)
            all_or_sel = 'all' if case_pattern_list == None else 'sel'
            report_path_name = f'{node_name}/report/rpt_{node_name}_{all_or_sel}.txt'
            title = f'Unit test execution result report ({node_name})'
            report('=' * (len(title) + 2), mode='w') if title_on else do_nothing()
            report(f' {title}') if title_on else do_nothing()
            report('=' * (len(title) + 2)) if title_on else do_nothing()
            report('date_time:' + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")) if title_on else do_nothing()
            report('') if title_on else report('', mode='w')
            report('---------------------')
            report(' pass / fail summary ')
            report('---------------------')
            total_count = len(result_info)
            ok_count = len([key for key, item in result_info.items() if item['judge'] == '(o)'])
            report(f'(ok / ng / total) = ({ok_count} / {total_count - ok_count} / {total_count})')
            report('')
            report('-------------')
            report(' result list ')
            report('-------------')
            for key, item in result_info.items():
                result_simple = f"{item['judge']}:{key}, unmatch:{item['unmatch']},"
                result_simple += f" version:{item['version']}, exec:{item['time']}, desc:{item['desc']}"
                report(result_simple)
                item['result_simple'] = result_simple
            is_disp = True if total_count <= 10 else False
            report('', is_disp=is_disp)
            report('---------------', is_disp=is_disp)
            report(' result detail ', is_disp=is_disp)
            report('---------------', is_disp=is_disp)
            report('Expected result on the left, execution result on the right.', is_disp=is_disp)
            report("Mark '*' for unmatch items.", is_disp=is_disp)
            report('', is_disp=is_disp)
            for key, item in result_info.items():
                report(f"[{item['result_simple']}]", is_disp=is_disp)
                for line in item['result_detail']:
                    #tobe_asis = line.split('(tab)')
                    #line = tobe_asis[0] + ' ' * (64 - len(tobe_asis[0])) + tobe_asis[1]
                    #line = line.replace('  *','*')
                    report(line, is_disp=is_disp)
                report('', is_disp=is_disp)
    else:
        print('not exist:', node_name)

#---------------
# exec all test 
#---------------
def exec_all_test(node_name, range_info, option=''):
    node_list = create_node_list()
    if node_name in node_list:
        range_info = chg_range_info(range_info)
        case_pattern_list = get_case_pattern_list(node_name)
        if range_info != []:
            case_pattern_list = [x for x in case_pattern_list if x[0] in range_info]
        #print(case_pattern_list)
        for case_pattern in case_pattern_list:
            exec(f'python3 exec_unit_test.py {node_name} {case_pattern[0]} {case_pattern[1]} {case_pattern[2]}{option}')
            #print(f'python3 exec_unit_test.py {node_name} {case_pattern[0]} {case_pattern[1]} {case_pattern[2]}{option}')
        if not ('-se' in option and '-sa' in option):
            case_pattern_list = None if range_info == [] else case_pattern_list
            make_report_from_result_data(node_name, case_pattern_list=case_pattern_list, title_on=False)
        #print(f'exec all test {node_name} project!')
    else:
        print('not exist:', node_name)

#---------------
# exec sel test 
#---------------
def exec_sel_test(node_name, sel_info_list):
    node_list = create_node_list()
    if node_name in node_list:
        #print(sel_info_list)
        sel_info_map = {}
        for sel_info in sel_info_list:
            if ':' not in sel_info:
                print('invalid arg:', sel_info_list)
                return
            case_pattern = sel_info.split(':')
            sel_info_map['{:03}'.format(int(case_pattern[0]))] = chg_range_info(case_pattern[1].split(','))
        case_pattern_list = get_case_pattern_list(node_name)
        case_pattern_list = [x for x in case_pattern_list if x[0] in sel_info_map.keys() and x[1] in sel_info_map[x[0]]]
        for case_pattern in case_pattern_list:
            exec(f'python3 exec_unit_test.py {node_name} {case_pattern[0]} {case_pattern[1]} {case_pattern[2]}')
            #print(f'python3 exec_unit_test.py {node_name} {case_pattern[0]} {case_pattern[1]} {case_pattern[2]}')
        make_report_from_result_data(node_name, case_pattern_list=case_pattern_list, title_on=False)
        #print(f'exec all test {node_name} project!')
    else:
        print('not exist:', node_name)

#------------------------
# zip target node folder
#------------------------
def zip_target_node_folder(node_name):
    node_list = create_node_list()
    if node_name in node_list:
        time_stamp = get_zip_time_stamp(node_name)
        exec(f'zip -r {node_name}_{time_stamp} {node_name}')
    else:
        print('not exist:', node_name)

################################################################################
# main flow

#-------
# usage
#-------
'''
if 4 > len(argv):
    print('[usage]')
    print('python3 exec_unit_test.py target 000 000')
    exit()
'''

'''
□実行中表示・非表示切り替え
□all シーケンス情報取得
　□all 実行
□sel：選択実行
　□ctrl_unit_test 001 001
　□ctrl_unit_test 001 
　□ctrl_unit_test 001 003-004
□init：フォルダ展開、テンプレ展開
□clear：成果物クリア(output、log、tobe/asis)
□diff -y による report 作成
　□合否判定
　□double桁落ちどうする？
□あと付け、todo/asis 生成
'''
#-----------
# arguments
#-----------
'''
node_name = argv[1]
case = argv[2]
pat = argv[3]
sub = argv[4] if 5 <= len(argv) else '00'
'''




print(argv)
print(len(argv))

#-------------------
# disp command list
#-------------------
if len(argv) ==1:
    command_list = ['list','create','clear','scenario','input','all','sel','analysis','report','zip']
    print('[command list]')
    for command in command_list:
        print(command)
    exit()

#--------------------------
# disp exist node dir list
#--------------------------
# python3 ctrl_unit_test.py list
if argv[1] == 'list':
    node_list = create_node_list()
    for node in node_list:
        print(node)
    exit()

#-----------------
# create node dir 
#-----------------
# python3 ctrl_unit_test.py create xxxx_xxxx
if argv[1] == 'create':
    if len(argv) > 2:
        node_name = argv[2]
        create_node_dir(node_name)
    else:
        print('python3 ctrl_unit_test.py create xxxx_xxxx')
    exit()

#--------------------
# clear created file 
#--------------------
# python3 ctrl_unit_test.py clear xxxx_xxxx [all]
if argv[1] == 'clear':
    if len(argv) > 2:
        node_name = argv[2]
        isall = False
        if len(argv) > 3:
            isall = True if argv[3] == 'all' else False
        clear_created_file(node_name, isall)
    else:
        print('python3 ctrl_unit_test.py clear xxxx_xxxx [all]')
    exit()

#-------------------
# copy node to node 
#-------------------
# python3 ctrl_unit_test.py copy xxxx_xxxx xxxx_xxxx2
if argv[1] == 'copy':
    if len(argv) > 3:
        node_name = argv[2]
        node_name2 = argv[3]
        copy_node_node(node_name, node_name2)
    else:
        print('python3 ctrl_unit_test.py copy xxxx_xxxx xxxx_xxxx2')
    exit()

#---------------------
# exec cnv_tsv2sna.py 
#---------------------
# python3 ctrl_unit_test.py scenario xxxx_xxxx [all / 001,003-005,007]
if argv[1] == 'scenario':
    if len(argv) > 2:
        node_name = argv[2]
        range_info = argv[3].split(',') if len(argv) > 3 else []
        exec_cnv_tsv2sna(node_name, range_info)
    else:
        print('python3 ctrl_unit_test.py create xxxx_xxxx 001,003-005,007(or all)')
    exit()

#-----------------------
# create input from fmt
#-----------------------
# python3 ctrl_unit_test.py analysis xxxx_xxxx [1,3-5,7]
if argv[1] == 'input':
    if len(argv) > 2:
        node_name = argv[2]
        range_info = argv[3].split(',') if len(argv) > 3 else []
        option = ' -se -sa'
        exec_all_test(node_name, range_info, option=option)
    else:
        print('python3 ctrl_unit_test.py analysis xxxx_xxxx [1,3-5,7]')
    exit()

#----------------
# check fmt file
#----------------
# python3 ctrl_unit_test.py check xxxx_xxxx
if argv[1] == 'check':
    if len(argv) > 2:
        node_name = argv[2]
        check_fmt_file(node_name)
    else:
        print('python3 ctrl_unit_test.py check xxxx_xxxx')
    exit()

#---------------
# exec all test 
#---------------
# python3 ctrl_unit_test.py all xxxx_xxxx 001,003-005,007
if argv[1] == 'all':
    if len(argv) > 2:
        node_name = argv[2]
        range_info = argv[3].split(',') if len(argv) > 3 else []
        exec_all_test(node_name, range_info)
    else:
        print('python3 ctrl_unit_test.py all xxxx_xxxx [001,003-005,007]')
    exit()

#---------------
# exec sel test 
#---------------
# python3 ctrl_unit_test.py sel xxxx_xxxx 003:002-004,007 005:007,008
if argv[1] == 'sel':
    if len(argv) > 3:
        node_name = argv[2]
        sel_info_list = argv[3:]
        exec_sel_test(node_name, sel_info_list)
    else:
        print('python3 ctrl_unit_test.py sel xxxx_xxxx 003:002-004,007 005:007,008')
    exit()

#---------------------------
# create analysis tobe/asis
#---------------------------
# python3 ctrl_unit_test.py analysis xxxx_xxxx [1,3-5,7]
if argv[1] == 'analysis':
    if len(argv) > 2:
        node_name = argv[2]
        range_info = argv[3].split(',') if len(argv) > 3 else []
        option = ' -si -se'
        exec_all_test(node_name, range_info, option=option)
    else:
        print('python3 ctrl_unit_test.py analysis xxxx_xxxx [1,3-5,7]')
    exit()

#------------------------------
# make report from result data
#------------------------------
if argv[1] == 'report':
    if len(argv) > 2:
        node_name = argv[2]
        make_report_from_result_data(node_name)
    else:
        print('python3 ctrl_unit_test.py create xxxx_xxxx')
    exit()

#-------------------------
# target node to zip file
#-------------------------
# python3 ctrl_unit_test.py zip xxxx_xxxx
if argv[1] == 'zip':
    if len(argv) > 2:
        node_name = argv[2]
        zip_target_node_folder(node_name)
    else:
        print('python3 ctrl_unit_test.py zip xxxx_xxxx')
    exit()

print(f'not applicable command!! {argv[1]}')
command_list = ['list','create','clear','scenario','input','all','sel','analysis','report','zip']
print('[command list]')
for command in command_list:
    print(command)
exit()

for index in range(1, 2):
    #cmd_line = 'python3 exec_unit_test.py python_listener 001 ' + '{:03}'.format(index)
    cmd_line = 'python3 exec_unit_test.py alert_filter 001 ' + '{:03}'.format(index)
    exec(cmd_line, False)
    time.sleep(1.0)




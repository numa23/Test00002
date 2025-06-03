import yaml
from sys import argv
import subprocess
import time
import os
import datetime

#---------
# version
#---------
ver_major = 1
ver_minor = 0
ver_sub = 0

version = f'{ver_major}.{ver_minor}.{ver_sub}'

'''
1.0.0	Create New	exec_unit_test.py Initial release
'''

#-------
# funcs
#-------
def setup_input(template, replace_dic, output):
    with open(template) as f:
        s = f.read()
    for key, value in replace_dic.items():
        s = s.replace(key, value)
    with open(output, mode='w') as f:
        f.write(s)
def get_fmt_file(node_yaml_name):
    sepa_list = os.path.split(node_yaml_name)
    if not os.path.exists(sepa_list[0] + '/fmt'):
        return node_yaml_name + '_fmt.yaml'
    return sepa_list[0] + '/fmt/' + sepa_list[1] + '_fmt.yaml'
def get_fix_num_list(target, roscommand, argument):
    list = []
    if target[roscommand] == None:
        return []
    for index in range(1, 100):
        if target[roscommand].get(f'{argument}' + '_{:02}'.format(index)) == None:
            break;
        list.append('{:02}'.format(index))
    return list
def get_command_value(scenario, command, default):
    cmd_value = None
    cmd_obj = scenario.get('comand')
    cmd_obj = scenario.get('command') if cmd_obj == None else cmd_obj
    if cmd_obj != None:
        cmd_value = cmd_obj.get(command)
    return  cmd_value if cmd_value != None else default
log_path_name = ''
def printx(log_text, mode='a'):
    print(log_text)
    global log_path_name
    with open(log_path_name, mode) as f:
        print(log_text, file=f)
def do_nothing():
    pass
def exec(cmd_line, quiet=False):
    printx('exec:' + cmd_line) if quiet == False else do_nothing()
    ps = subprocess.run(cmd_line, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text=True)
    return ps
def exec2(cmd_line, quiet=False):
    printx('exec2:' + cmd_line) if quiet == False else do_nothing()
    ps = subprocess.Popen(cmd_line, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    return ps
def wait_start_ps(ps_list):
    for ps in ps_list:
        ps_wait = exec(f'pgrep -l {ps}')
        if ps not in ps_wait.stdout:
            return False
    return True
def analysis_yml(obj, obj2):
    if type(obj) == dict:
        print(f'obj:{obj}、obj2:{obj2}')
        for key, value in obj.items():
            value = analysis_yml(value, obj2[key])
            if value != None:
                obj[key] = value
    elif type(obj) == list:
        print(f'obj:{obj}、obj2:{obj2}')
        for index, data in enumerate(obj):
            analysis_yml(data, obj2[index])
    else:
        return obj2
    return None

#-------
# usage
#-------
if 4 > len(argv):
    print('[usage]')
    print('python3 exec_unit_test.py target 000 000')
    exit()

#-----------
# arguments
#-----------
node_name = argv[1]
case = argv[2]
pat = argv[3]
sub = argv[4] if 5 <= len(argv) else '00'

skip_input = False
skip_exec = False
skip_anal = False
if 5 <= len(argv):
    skip_input = True if '-si' in argv[4:] else False
    skip_exec = True if '-se' in argv[4:] else False
    skip_anal = True if '-sa' in argv[4:] else False
    sub = argv[4] if argv[4].isdigit() else '00'

#---------------
# get path info
#---------------
node_name_path = f'{node_name}/' if os.path.exists(f'{node_name}') else ''
log_path_name = node_name_path + 'log/'

#-------------------
# get scenario info
#-------------------
with open(f'{node_name_path}scenario/sn_{node_name}_{case}_{pat}_{sub}.yaml', 'r') as yml:
    scenario = yaml.safe_load(yml)
info = scenario['info']
title = f" {info['case']}({case}_{pat}_{sub}):{info['desc']}"
log_path_name += f'dsp_{node_name}_{case}_{pat}_{sub}.log'
printx('-' * len(title), 'w')
printx(title)
printx('-' * len(title))
printx(f'version:{version}')
printx('md5sum:' + exec('md5sum ' + argv[0], quiet=True).stdout.split()[0])
now = datetime.datetime.now()
printx('date_time:' + now.strftime("%Y/%m/%d %H:%M:%S"))

#--------------------------
# setup param & input data
#--------------------------
if not skip_input:
    param_fmt = get_command_value(scenario, 'param fmt', {})
    yaml_name_list = scenario['yaml_name']
    for yaml_name in yaml_name_list:
        node_yaml_name = f'{node_name_path}{yaml_name}'
        fmt_file = get_fmt_file(node_yaml_name)
        dir_file = yaml_name.split('/')
        if dir_file[0] == 'param':
            fmt_new = param_fmt.get(dir_file[1])
            if fmt_new != None:
                fmt_file = fmt_file.replace(dir_file[1] + '_fmt', fmt_new + '_fmt')
        printx(fmt_file)
        setup_input(fmt_file, scenario[yaml_name], f'{node_yaml_name}.yaml')
        exec2(f'cp {node_yaml_name}.yaml {node_yaml_name}_{case}_{pat}_{sub}.yaml')
    printx('input:' + str(scenario[yaml_name_list[0]]))
    time.sleep(1.0)

#-----------------
# get target info
#-----------------
with open(f'{node_name_path}target/ros_{node_name}.yaml', 'r') as yml:
    target = yaml.safe_load(yml)
time.sleep(2.0)

#-----------------
# create num list
#-----------------
param_num_list = get_fix_num_list(target, 'rosparam', 'param')
run_num_list = get_fix_num_list(target, 'rosrun', 'rosrun')
echo_num_list = get_fix_num_list(target, 'rostopic', 'echo')
pub_num_list = get_fix_num_list(target, 'rostopic', 'pub')

#------------------
# get command info
#------------------
pub_num_list = get_command_value(scenario, 'pub select', pub_num_list)
pub_sleep =  get_command_value(scenario, 'pub sleep', 1.0)
pub_sleep_list = pub_sleep if type(pub_sleep) == list else [pub_sleep] * (len(pub_num_list) - 1) + [0.0]
disp_result = get_command_value(scenario, 'disp result', False)
result_fmt = get_command_value(scenario, 'result_fmt', '')

#---------
# roscore
#---------
if not skip_exec:
    node_list = exec('rosnode list').stdout.splitlines()
    for node in node_list:
        exec(f'rosnode kill {node}')
    exec2('pkill ros')
    time.sleep(3.0)
    ps_roscore = exec2('roscore &')
    while not wait_start_ps(['roscore', 'rosmaster', 'rosout']):
        time.sleep(0.5)
    time.sleep(1.0)

#----------
# rosparam
#----------
if not skip_exec:
    for fix_num in param_num_list:
        rosparam = target['rosparam'][f'param_{fix_num}']
        if node_name_path != '' and not node_name_path in rosparam:
            rosparam = rosparam.replace('load ', 'load ' + node_name_path)
        exec2('rosparam ' + rosparam)
    time.sleep(2.0)

#--------
# rosrun
#--------
if not skip_exec:
    for index, fix_num in enumerate(run_num_list):
        end_fix_num = f'_{fix_num}' if index > 0 else ''
        rosrun = target['rosrun'][f'rosrun_{fix_num}']
        rosrun += f' > {node_name_path}log/run_{node_name}_{case}_{pat}_{sub}{end_fix_num}.log 2>&1'
        exec2('rosrun ' + rosrun)
    time.sleep(3.0)

#---------------
# rostopic echo
#---------------
if not skip_exec:
    for index, fix_num in enumerate(echo_num_list):
        end_fix_num = f'_{fix_num}' if index > 0 else ''
        rosecho = target['rostopic'][f'echo_{fix_num}']
        rosecho += f' > {node_name_path}output/out_{node_name}_{case}_{pat}_{sub}{end_fix_num}.txt'
        exec2('rostopic echo ' + rosecho)
    time.sleep(2.0)

#--------------
# rostopic pub
#--------------
if not skip_exec:
    import rostopic
    for index, fix_num in enumerate(pub_num_list):
        filename = f'{node_name_path}input/in_{node_name}_{fix_num}_{case}_{pat}_{sub}.yaml'
        printx('exec3:rostopic pub ' + target['rostopic'][f'pub_{fix_num}'] + f' -1 -f {filename}')
        target_items = target['rostopic'][f'pub_{fix_num}'].split()
        pub, msg_class = rostopic.create_publisher(target_items[0], target_items[1], True)
        rostopic.stdin_publish(pub, msg_class, None, True, filename, False)
        time.sleep(pub_sleep_list[index])
        printx(f'sleep:{pub_sleep_list[index]}(sec)') if index < len(pub_num_list) - 1 else do_nothing()
    time.sleep(10.0)

#--------------------
# create tobe result
#--------------------
if not skip_anal:
    fmt_file = get_fmt_file(f'{node_name_path}report/out_{node_name}')
    if result_fmt != '':
        fmt_file = fmt_file.replace('_fmt', f'{result_fmt}_fmt')
        print(f'{fmt_file}:{os.path.isfile(fmt_file)}')
    if os.path.isfile(fmt_file):
        os.makedirs(f'{node_name_path}report/analysis', exist_ok=True)
        result_tobe = f'{node_name_path}report/analysis/out_{node_name}_{case}_{pat}_{sub}_tobe.yaml'
        setup_input(fmt_file, scenario['result_tobe'], result_tobe)
        with open(result_tobe, 'r') as yf:
            result_yaml = yaml.safe_load(yf)
        with open(result_tobe, 'w') as yf:
            yaml.dump(result_yaml, yf, default_flow_style=False)
        #    yaml.safe_dump(result_yaml, yf, sort_keys=False)

#--------------------
# create asis result
#--------------------
if not skip_anal:
    if os.path.isfile(fmt_file):
        output_yaml_list = exec('cat ' + f'{node_name_path}output/out_{node_name}_{case}_{pat}_{sub}.txt').stdout.split('---')
        if len(output_yaml_list) >= 2:
            print(len(output_yaml_list))
            print(output_yaml_list)
            result_yaml2 = yaml.safe_load(output_yaml_list[-2])
            analysis_yml(result_yaml, result_yaml2)
            with open(f'{node_name_path}report/analysis/out_{node_name}_{case}_{pat}_{sub}_asis.yaml', 'w') as yf:
                yaml.dump(result_yaml, yf, default_flow_style=False)
                #yaml.safe_dump(result_yaml, yf, sort_keys=False)

#-------------
# disp result
#-------------
if not skip_anal and disp_result == True:
    if os.path.isfile(fmt_file):
        diff_file = f'{node_name_path}report/analysis/out_{node_name}_{case}_{pat}_{sub}_tobe.yaml '
        diff_file += f'{node_name_path}report/analysis/out_{node_name}_{case}_{pat}_{sub}_asis.yaml'
        diff_result = exec('diff -u ' + diff_file).stdout.splitlines()
        printx('result:start')
        def printxx(x):
            global index
            index += 1
            printx(x)
        index = 0
        for x in diff_result:
            printxx(x) if x[0] in ('-', '+') and x[2] not in ('-', '+') else do_nothing()
        printx('result:end')
        printx('judge:' + ('(o)' if index == 0 else '(x)') + f' {node_name} {case} {pat} {sub}')

do_nothing() if not skip_exec else exit()

#----------
# kill ros
#----------
node_list = exec('rosnode list').stdout.splitlines()
print(node_list)
for node in node_list:
    exec(f'rosnode kill {node}')
exec2('pkill ros')
time.sleep(5.0)


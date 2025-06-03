import os
import sys
import datetime as dt
import time
import yaml
import subprocess
from lib import Cloud

funcs = []

def get_funcs_ros():
    return funcs
'''

def exec(cmd_line):
    ps = subprocess.run(cmd_line, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text=True)
    return ps

def exec2(cmd_line):
    #printx('exec2:' + cmd_line) if quiet == False else do_nothing()
    ps = subprocess.Popen(cmd_line, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    return ps

def wait_start_ps(ps_list):     # for ubuntu
    for ps in ps_list:
        ps_wait = exec(f'pgrep -l {ps}')
        if ps not in ps_wait.stdout:
            return False
    return True
'''

funcs += ['get_file_text']
# func for report mode to get file text
def get_file_text(file_name):
    with open(file_name, encoding='utf8', newline='') as f:
        file_text = f.readlines()
    file_text = [x.replace('\n', '') for x in file_text]
    file_text = [x.replace('\r', '') for x in file_text]
    return file_text

def comp_text(text_01, text_02):
    cloud = Cloud()
    skip_list = cloud.dict.get('skip_comp')
    #skip_list = [' nsec:', ' sec:']
    if skip_list != None:
        for skip_item in skip_list:
            if skip_item in text_01:
                return '-'
    return '*' if text_01 != text_02 else ' '

funcs += ['get_diff_result']
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
    #comp_text = lambda text_01, text_02: '*' if text_01 != text_02 else ' '
    ng_count = 0
    diff_result = []
    for index in range(max_len):
        text_01 = get_text(text_list_01, index)
        text_02 = get_text(text_list_02, index)
        judge = comp_text(text_01, text_02)
        ng_count += 1 if judge == '*' else 0
        #print(f'{text_01.ljust(62)}{judge} {text_02}')
        diff_result += [f'{text_01.ljust(62)}{judge} {text_02}']
    cloud = Cloud()
    cloud.dict['ng_count'] = ng_count
    return diff_result

funcs += ['get_ng_count']
def get_ng_count():
    cloud = Cloud()
    return cloud.dict.get('ng_count')

funcs += ['disp_list']
def disp_list(item_list):
    for item in item_list:
        print(item)

funcs += ['write_list']
def write_list(file, item_list):
    with open(file, 'w', encoding='utf-8') as f:
        for item in item_list:
            print(item, file=f)

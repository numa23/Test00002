import os
import sys
import datetime as dt
import time
import yaml
import subprocess
from lib import Cloud

funcs = []

def get_funcs_ros_py():
    return funcs

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

funcs += ['roscore']
def roscore():
    print(f'{sys._getframe().f_code.co_name}')
    node_list = exec('rosnode list').stdout.splitlines()
    for node in node_list:
        exec('rosnode kill ' + node)
    exec2('pkill ros')
    time.sleep(3.0)
    ps_roscore = exec2('roscore &')
    retry = 0
    while not wait_start_ps(['roscore', 'rosmaster', 'rosout']):
        time.sleep(0.5)
        if retry > 20:
            return False
        retry += 1
    time.sleep(1.0)
    return True

funcs += ['rosparam_load']
def rosparam_load(param, namespace):
    #print(f'{sys._getframe().f_code.co_name}')
    print(f'rosparam load {param} {namespace}')
    exec2(f'rosparam load {param} {namespace}')

funcs += ['rosrun']
def rosrun(pkg_node):
    #print(f'{sys._getframe().f_code.co_name}')
    print('rosrun csa_and_csa_intersection ' + f'{pkg_node}_node.py')
    exec2('rosrun csa_and_csa_intersection ' + f'{pkg_node}_node.py')

funcs += ['rostopic_echo']
def rostopic_echo(topic_name, filename):
    #print(f'{sys._getframe().f_code.co_name}')
    print('rostopic echo ' + topic_name + ' > ' + filename)
    exec2('rostopic echo ' + topic_name + ' > ' + filename)

funcs += ['rostopic_pub']
def rostopic_pub(topic_name, topic_type, filename):
    #print(f'{sys._getframe().f_code.co_name}')
    print(f'rostopic pub {topic_name} {topic_type} -1 -f {filename}')
    import rostopic
    pub, msg_class = rostopic.create_publisher(topic_name, topic_type, True)
    rostopic.stdin_publish(pub, msg_class, None, True, filename, False)
    #time.sleep(pub_sleep_list[index])
    time.sleep(1)
    #printx(f'sleep:{pub_sleep_list[index]}(sec)') if index < len(pub_num_list) - 1 else do_nothing()
    #time.sleep(10.0)

funcs += ['roskill']
def roskill():
    print(f'{sys._getframe().f_code.co_name}')
    node_list = exec('rosnode list').stdout.splitlines()
    print(node_list)
    retry = 0
    for node in node_list:
        exec(f'rosnode kill {node}')
        if retry > 20:
            break
        retry += 1
    exec2('pkill ros')
    time.sleep(5.0)

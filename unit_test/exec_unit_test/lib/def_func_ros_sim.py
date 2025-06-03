import os
import sys
import datetime as dt
import time
import yaml
import subprocess
from lib import Cloud
from CSAonMATLAB.MATLAB import cd
from CSAonMATLAB.ROS import rostopic_stdin_publish, rostopic_echo, rosrun, rosnode_kill

funcs = []

def get_funcs_ros_sim():
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

funcs += ['ros_cd_sim']
def ros_cd_sim(my_path):
    cd(my_path)

funcs += ['ros_node_run_sim']
def ros_node_run_sim(node_name):
    rosrun(node_name)

funcs += ['ros_node_kill_sim']
def ros_node_kill_sim(node_name):
    rosnode_kill(node_name)

funcs += ['ros_topic_publish_sim']
def ros_topic_publish_sim(topic_name, msg_type, yaml_file_path):
    rostopic_stdin_publish(topic_name, msg_type, yaml_file_path)

funcs += ['ros_topic_echo_sim']
def ros_topic_echo_sim(topic_name, yaml_file_path):
    rostopic_echo(topic_name, yaml_file_path)

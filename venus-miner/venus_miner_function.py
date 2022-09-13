import psutil
import os
import json
#获取进程是否存在函数,返回1表示存在，0表示不存在
def process_check(process_name):
    '''
    用于检查进程是否存在
    参数填写进程名称
    返回1表示该进程存在，0表示进程不存在
    '''
    for i in psutil.pids():
        if psutil.Process(i).name()==f"{process_name}":
            print(f"{process_name}进程正在运行,进程号为:%s" % i)
            return 1
        else:
            continue
    return 0

#获取进程创建的时间
def process_alive(process_name,process_cmd):
    '''
    用于获取进程创建的时间
    :param process_name: 进程名称
    :param process_cmd: 进程启动带的第一个参数
    :return:
    '''
    process_pid = [pid for pid in psutil.pids() if psutil.Process(pid).name() == f"{process_name}" and f'{process_cmd}' in psutil.Process(pid).cmdline()]
    process_create_time=psutil.Process(process_pid[0]).create_time()
    return process_create_time

def venus_miner_list():
    '''
    用于获取venus-miner矿工地址
    以列表的形式返回矿工信息
    '''
    miner_list_info=os.popen("/root/venus-miner address list").read()
    info_json=json.loads(miner_list_info)
    return info_json
def venus_miner_state(miner_addr):
    '''
    用于获取venus-miner矿工状态
    True表示已开启挖矿，False表示不在挖矿
    '''
    miner_state_info=os.popen(f"/root/venus-miner address state").read()
    info_json=json.loads(miner_state_info)
    for i in range(0,len(info_json)):
        if miner_addr == info_json[i]["Addr"]:
            state=info_json[i]['IsMining']
    return state

def venus_auth_test_user():
    venus_auth_user = 'auto-test-1234'
    return venus_auth_user
def venus_auth_test_miner():
    venus_auth_miner='f01000'
    return venus_auth_miner
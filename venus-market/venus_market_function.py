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

def venus_market_list_miner():
    miner_list=os.popen("/root/venus-market actor list | grep ^t0 |awk '{print $1}'").readlines()
    return miner_list

def venus_market_list_pieces():
    '''
    用于获取venus-market piece信息
    以列表的形式返回每个piece信息
    '''
    market_list_pieces=os.popen("/root/venus-market pieces list-pieces|grep -v venusmarket").readlines()
    return market_list_pieces

def venus_market_list_deals():
    '''
    用于获取venus-market deal信息
    以列表的形式返回每个deal信息
    '''
    market_list_deals=os.popen(f"/root/venus-market storage-deals list --verbose | egrep -v 'venusmarket|ProposalCid'").readlines()
    return market_list_deals

def market_client_data_local():
    '''
    获取
    :return:
    '''
    client_data_info=os.popen("/root/market-client data local").readlines()
    return client_data_info


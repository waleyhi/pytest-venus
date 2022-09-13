import psutil
import os
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
    用于获取venus-miner钱包地址信息
    以列表的形式返回钱包地址
    '''
    miner_list_info=os.popen(f"/root/venus-miner list").readlines()
    return miner_list_info


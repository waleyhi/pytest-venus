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
            break
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
    process_pid = [pid for pid in psutil.pids() if psutil.Process(pid).name() == f"{process_name}" and psutil.Process(pid).cmdline()[1] == f"{process_cmd}"]
    process_create_time=psutil.Process(process_pid[0]).create_time()
    return process_create_time
#venus-message获取各种类型消息id用于自动化测试,如果没有查询到消息id，则返回0
def venus_messager_id_get(list_type):
    '''
    用于获取消息id
    可选参数为list，list-fail或者list-blocked
    '''
    messager_msg_info = os.popen(f"/root/venus-messager msg {list_type} --verbose| grep '^baf'").readlines()
    if len(messager_msg_info)==0:
        print ("无可供测试的消息")
        return 0
    else:
        messager_msg_id=messager_msg_info[0].split()[0]
        return messager_msg_id
def venus_messager_address_get():
    '''
    用于获取venus-messager中address地址
    :return:
    '''
    messager_address_info = os.popen(f"/root/venus-messager address list").readlines()
    if len(messager_address_info)==0:
        print("无可供测试的地址信息")
        return 0
    else:
        messager_address_addr=messager_address_info[3].split('"')[3]
        return messager_address_addr
def venus_messager_address_state(address):
    messager_address_info = os.popen(f"/root/venus-messager address search {address}").readlines()
    if len(messager_address_info) > 2:
        messager_address_state = messager_address_info[6].split()[1]
        return messager_address_state
    else:
        print("无法找到对应钱包地址信息，请检查钱包地址信息是否正常")
        return 0


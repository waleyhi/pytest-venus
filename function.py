import psutil
#检查进程是否存在函数,返回1表示存在，0表示不存在
def process_check(process_name):
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
    process_pid = [pid for pid in psutil.pids() if psutil.Process(pid).name() == f"{process_name}" and psutil.Process(pid).cmdline()[1] == f"{process_cmd}"]
    process_create_time=psutil.Process(process_pid[0]).create_time()
    return process_create_time


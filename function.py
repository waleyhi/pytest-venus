import psutil
#检查进程是否存在函数,返回1表示存在，0表示不存在
def process_check(process_name):
    for i in psutil.pids():
        if psutil.Process(i).name()==f"{process_name}":
            return 1
            break
        else:
            continue
        return 0

#检查进程是否能运行超过3分钟，返回1表示正常，返回0表示失败
#def process_alive(process_name):



import allure
import datetime
import os
import psutil
import pytest
import re
import time
import func_timeout

@allure.feature("venus主程序测试")
class Test_program_status():
    @allure.story("测试venus程序是否能启动")
    def test_venus_start(self):
        for i in psutil.pids():
            if psutil.Process(i).name()=="venus":
                print ("venus进程正在运行,进程号为:%s" % i)
                a=1
                break
            else:
                a=0
        assert a==1,"venus 进程不存在"
    @allure.story("测试venus程序是否能稳定运行3分钟不崩溃")
    def test_venus_alive(self):
        time.sleep(180)
        venus_pid=[pid for i in psutil.pids() if psutil.Process(i).name()=="venus"]
        a=psutil.Process(venus_pid).create_time()
        b=time.time()
        c=b-a
        print ("venus 进程已稳定运行%f秒" % c)
        assert c > 180,"venus 运行时间不足3分钟"
    @allure.story("测试venus高度是否能同步到最新")
    def test_venus_height(self):
        height=os.popen("/root/venus chain ls").readlines()[-1]
        height_time=re.split('\(|\)',height)[1]
        time1=datetime.datetime.strptime(height_time,'%Y-%m-%d %H:%M:%S')
        time2=time1.timestamp()
        time3=time.time()
        print ("当前区块时间为%s,实际时间为%s" % time1,datetime.datetime.now())
        assert time3-time2 < 60,"高度同步异常，venus已超过60秒没更新高度"
@allure.feature("venus state 各命令测试")
class Teststate():
    @allure.story("venus state power 命令测试")
    def test_state_power(self):
        power_info=os.popen("/root/venus state power t01000").readlines()[0]
        print ("命令执行结果为%s" % power_info)
        power=re.split('\(',power_info)[0]
        assert int(power)==2516582400,"venus state power命令异常"
    @allure.story("venus state sectors 命令测试")
    def test_state_sectors(self):
        sectors_info=os.popen("/root/venus state sectors t01000").readlines()[0]
        print ("命令执行结果为%s" % sectors_info)
        sectors=re.split(':',sectors_info)[0]
        assert int(sectors)==0,"venus state sectors 命令异常"
    @allure.story("venus state actor-cids 命令测试")
    def test_state_actor_cids(self):
        actor_cids=os.popen("/root/venus state actor-cids").readlines()
        print ("命令执行结果为%s" % actor_cids)
        for i in range(1,20):
            if actor_cids[i]=='storagepower      bafk2bzaceb45l6zhgc34n6clz7xnvd7ek55bhw46q25umuje34t6kroix6hh6  \n':
                a=1
                break
            else:
                a=0
        assert a==1,"venus actor版本不对，请检查actor-cids"
@allure.feature("venus chain 各命令测试")
class Testchain():
    @allure.story("测试venus高度导出为car文件是否正常")
    def test_chain_export(self):
        os.system("/root/venus chain export /tmp/test.car")
        car_path='/tmp/test.car'
        car_size=os.path.getsize(car_path)/1024/1024
        print ("高度car文件已导出，路径为%s,大小为%s MB" % car_path,car_size)
        assert os.path.isfile(car_path),"导出链失败，请检查chain export命令"
@allure.feature("venus wallet 各命令测试")
class Testwallet():
    @allure.story("venus wallet ls命令是否正常")
    def test_wallet_ls(self):
        print("命令执行结果为%s" % os.system("/root/venus wallet ls"))
        assert os.system("/root/venus wallet ls")==0,"wallet ls失败，请检查命令"

if __name__ == '__main__':
    pytest.main()

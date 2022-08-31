import allure
import datetime
import os
import psutil
import pytest
import re
import time
import pexpect
#venus 主程序测试
@allure.epic("venus测试")
@allure.feature("venus主程序测试")
class Test_venus_status():
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
        #time.sleep(180)
        venus_pid=[pid for pid in psutil.pids() if psutil.Process(pid).name()=="venus" and psutil.Process(pid).cmdline()[1]=="daemon"]
        a=psutil.Process(venus_pid[0]).create_time()
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
        print ("当前区块时间为%s,实际时间为%s" % (time1,datetime.datetime.now()))
        assert time3-time2 < 60,"高度同步异常，venus已超过60秒没更新高度"

#venus state 命令模块测试
@allure.epic("venus测试")
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

#venus chain 命令模块测试
@allure.epic("venus测试")
@allure.feature("venus chain 各命令测试")
class Testchain():
    @allure.story("测试venus高度导出为car文件是否正常")
    def test_chain_export(self):
        os.system("/root/venus chain export /tmp/test.car")
        car_path='/tmp/test.car'
        car_size=os.path.getsize(car_path)/1024/1024
        print ("高度car文件已导出，路径为%s,大小为%s MB" % (car_path,car_size))
        assert os.path.isfile(car_path),"导出链失败，请检查chain export命令"

#venus wallet 命令模块测试
@allure.epic("venus测试")
@allure.feature("venus wallet 各命令测试")
class Test_venus_wallet():
    @allure.story("venus wallet ls命令是否正常")
    def test_wallet_ls(self):
        print("命令执行结果为%s" % os.system("/root/venus wallet ls"))
        assert os.system("/root/venus wallet ls")==0,"wallet ls失败，请检查命令"
    @allure.story("venus wallet balance命令是否正常")
    def test_wallet_balance(self):
        balance_info = os.popen(
            "/root/venus wallet balance t3rugtczeric5kypbgnt7643omyxia6mkrevryrggrksqx73zfbqthgj7eumxbeap6hoctj45dc6k6ylyfm57a").readlines()[
            0]
        print ("t3rugtczeric5kypbgnt7643omyxia6mkrevryrggrksqx73zfbqthgj7eumxbeap6hoctj45dc6k6ylyfm57a地址余额为：",balance_info)
        assert os.system("/root/venus wallet balance t3rugtczeric5kypbgnt7643omyxia6mkrevryrggrksqx73zfbqthgj7eumxbeap6hoctj45dc6k6ylyfm57a")==0,"wallet balance失败，请检查命令"
    @allure.story("venus wallet set-password命令是否正常")
    @pytest.mark.run(order=1)
    def test_wallet_set_password(self):
        try:
            set_password_process=pexpect.spawn("/root/venus wallet set-password")
            expect_list = ['Password:',pexpect.EOF,pexpect.TIMEOUT,]
            index=set_password_process.expect(expect_list)
            if index==0:
                set_password_process.sendline("admin123")
                expect_list = ['Enter Password again:',pexpect.EOF,pexpect.TIMEOUT,]
                index=set_password_process.expect(expect_list)
                if index==0:
                    set_password_process.sendline("admin123")
                    a=1
                    print("密码设置成功，新密码为admin123")
                    process.interact()
                else:
                    print("命令执行未出现again字样")
                    a=0
                    print('EOF or TIMEOUT')
            else:
                print ("命令执行未出现password字样")
                print('EOF or TIMEOUT')
        except Exception as e:
            a=0
            print ("密码设置失败，报错信息为：",e)
        assert a==1,"密码设置失败，请检查venus wallet set-password命令"
    @allure.story("测试wallet new/new bls是否能生成t3地址")
    @pytest.mark.run(order=2)
    def test_wallet_new_t3(self):
        try:
            wallet_new_info_t3=os.popen("/root/venus wallet new").readlines()[0]
            print ("命令执行成功，新建t3地址为：",wallet_new_info_t3)
            a=1
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1
    @allure.story("测试venes wallet是否能生成t1地址")
    @pytest.mark.run(order=2)
    def test_wallet_new_t1(self):
        try:
            wallet_new_info_t1 = os.popen("/root/venus wallet new --type=secp256k1").readlines()[0]
            print ("命令执行成功，新建t1地址为：",wallet_new_info_t1)
            a=1
        except Exception as e:
            print("命令报错，错误信息为：",e)
            a=0
        assert a==1
    @allure.story("测试venus wallet ls是否能输出钱包信息")
    def test_wallet_ls(self):
        try:
            wallet_ls_info = os.popen("/root/venus wallet ls ").readlines()
            print ("命令执行成功，wallet信息为：",wallet_ls_info)
            a=1
        except Exception as e:
            print ("命令报错，报错信息为：",e)
            a=0
        assert a==1
    @allure.story("测试venus wallet set-default是否能设置默认钱包地址")
    @pytest.mark.run(order=2)
    def test_wallet_set_default(self):
        wallet_ls_info=os.popen("/root/venus wallet ls").readlines()
        not_default_wallet=[i for i in wallet_ls_info if 'X' not in i][-1]
        print ("需要设置为默认钱包地址的t3地址信息为：",not_default_wallet)
        not_default_wallet_address=not_default_wallet.split()[0]
        try:
            set_default_wallet_info=os.popen(f'/root/venus wallet set-default {not_default_wallet_address}').readlines()
            print ("已将%s设置为默认钱包地址" % set_default_wallet_info[0])
            a=1
        except Exception as e:
            print ("设置钱包地址报错，报错信息为：",e)
            a=0
        assert a==1,"venus 节点设置钱包地址报错"
    @allure.story("测试venus wallet lock功能是否正常")
    @pytest.mark.run(order=2)
    def test_wallet_lock(self):
        wallet_lock = os.popen("/root/venus wallet lock").readlines()
        print ("命令执行结果为：",wallet_lock)
        if 'success' in wallet_lock[0]:
            a=1
        elif 'already locked' in wallet_lock[0]:
            a=1
        else:
            a=0
        assert a==1,"venus wallet lock命令执行失败"
    @allure.story("测试 venus wallet unlock功能是否正常")
    @pytest.mark.run(order=3)
    def test_wallet_unlock(self):
        wallet_unlock_info = os.popen("echo 'admin123' | /root/venus wallet unlock").readlines()
        print("命令执行结果为：", wallet_unlock_info)
        if 'unlocked success' in wallet_unlock_info[0]:
            a=1
        elif 'already unlocked' in wallet_unlock_info[0]:
            a=1
        else:
            a=0
        assert a==1,"venus wallet unlock命令执行失败"
    @allure.story("测试venus wallet import是否能导入钱包地址")
    @pytest.mark.run(order=4)
    def test_wallet_import(self):
        private_key='7b2254797065223a22626c73222c22507269766174654b6579223a225039715136684d414c74695162623955754c48624371586a4d555161576346346774466c6c4759434b52553d227d'
        t3_addr='t3waqhfglxquvmdeqko7jb3qkd6vrpsdaduhnlsbvotu6zajf2dbp4uk5pip3mbjbq6dj4iun7tqzkkh3nrtla'
        wallet_import_info = os.popen(f"echo '{private_key}'|/root/venus wallet import").readlines()
        print ("命令执行结果为：",wallet_import_info)
        if f'{t3_addr}' in wallet_import_info[0]:
            a=1
        else:
            a=0
        assert a==1,"venus wallet import导入钱包地址失败"
    @allure.story("测试venus wallet export是否能导出钱包地址")
    @pytest.mark.run(order=4)
    def test_wallet_export(self):
        private_key='7b2254797065223a22626c73222c22507269766174654b6579223a225039715136684d414c74695162623955754c48624371586a4d555161576346346774466c6c4759434b52553d227d'
        t3_addr = 't3waqhfglxquvmdeqko7jb3qkd6vrpsdaduhnlsbvotu6zajf2dbp4uk5pip3mbjbq6dj4iun7tqzkkh3nrtla'
        wallet_export_info=os.popen(f"echo 'admin123' | /root/venus wallet export {t3_addr}").readlines()
        print ("命令执行结果为：",wallet_export_info)
        if {private_key} in wallet_export_info[0]:
            a=1
        else:
            a=0
        assert a==1,"venus wallet export导出钱包地址失败"

if __name__ == '__main__':
    pytest.main()
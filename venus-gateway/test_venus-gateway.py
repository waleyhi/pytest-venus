import os
import allure
import time
import psutil
import pytest
#获取venus-gateway程序运行目录
@pytest.fixture(scope='function',autouse=True)
def get_venus_gateway_run_path():
    venus_gateway_path=os.popen("ps -ef | grep venus-gateway|grep run| grep -v grep| awk '{print $2}'| xargs pwdx | awk '{print $NF}'").read().strip()
    return venus_gateway_path
@allure.epic("venus-gateway测试")
@allure.feature("venus-gateway主程序测试")
class Test_venus_gateway_status():
    @allure.story("测试venus-gateway程序是否能启动")
    def test_venus_gateway_start(self):
        for i in psutil.pids():
            if psutil.Process(i).name()=="venus-gateway":
                print ("venus-gateway进程正在运行,进程号为:%s" % i)
                a=1
                break
            else:
                a=0
        assert a==1,"venus-gateway 进程不存在"
    @allure.story("测试venus-gateway程序是否能稳定运行3分钟不崩溃")
    def test_venus_gateway_alive(self):
        #time.sleep(180)
        venus_gateway_pid=[pid for pid in psutil.pids() if psutil.Process(pid).name()=="venus-gateway" and "run" in str(psutil.Process(pid).cmdline())]
        a=psutil.Process(venus_gateway_pid[0]).create_time()
        b=time.time()
        c=b-a
        print ("venus-gateway 进程已稳定运行%f秒" % c)
        assert c > 180,"venus-gateway 运行时间不足3分钟"

@allure.epic("venus-gateway测试")
@allure.feature("venus-gateway miner各命令测试")
class Test_venus_gateway_miner():
    @allure.story("测试venus-gateway miner list 查看矿工信息是否成功")
    def test_venus_gateway_miner_list(self,get_venus_gateway_run_path):
        try:
            gateway_miner_list = os.popen(f"{get_venus_gateway_run_path}/venus-gateway miner list").readlines()
            print ("gateway miner list命令结果为：",gateway_miner_list)
            if len(gateway_miner_list)==0:
                a=0
            else:
                a=1
        except Exception as e:
            print ("gateway miner list查看矿工信息失败，报错信息为：",e)
            a=0
        assert a==1,"gateway miner list查看矿工信息失败"
    @allure.story("测试venus-gateway miner state 查看矿工状态是否成功")
    def test_venus_gateway_miner_state(self,get_venus_gateway_run_path):
        gateway_miner_list = os.popen(f"{get_venus_gateway_run_path}/venus-gateway miner list").readlines()[0]
        try:
            gateway_miner_state = os.popen(f"{get_venus_gateway_run_path}/venus-gateway miner state {gateway_miner_list}").readlines()
            print("gateway miner state命令结果为：", gateway_miner_state)
            if len(gateway_miner_state) == 0:
                a = 0
            else:
                a = 1
        except Exception as e:
            print("gateway miner state查看矿工状态失败，报错信息为：", e)
            a = 0
        assert a == 1,"gateway miner state查看矿工状态失败"
    @allure.story("测试venus-gateway wallet list 查看钱包地址信息是否成功")
    def test_venus_gateway_wallet_list(self,get_venus_gateway_run_path):
        try:
            gateway_wallet_list = os.popen(f"{get_venus_gateway_run_path}/venus-gateway wallet list").readlines()
            print("gateway wallet list命令结果为：", gateway_wallet_list)
            if len(gateway_wallet_list) == 0:
                a = 0
            else:
                a = 1
        except Exception as e:
            print("gateway wallet list查看钱包信息失败，报错信息为：", e)
            a = 0
        assert a == 1, "gateway wallet list查看钱包信息失败"
    @allure.story("测试venus-gateway wallet state 查看钱包状态是否成功")
    def test_venus_gateway_wallet_state(self,get_venus_gateway_run_path):
        gateway_wallet_list = os.popen(f"{get_venus_gateway_run_path}/venus-gateway wallet list").readlines()
        wallet_for_state=gateway_wallet_list[2].split('"')[3]
        try:
            gateway_wallet_state = os.popen(f"{get_venus_gateway_run_path}/venus-gateway wallet state {wallet_for_state}").readlines()
            print("gateway wallet state命令结果为：",gateway_wallet_state)
            if len(gateway_wallet_state) == 0:
                a = 0
            else:
                a = 1
        except Exception as e:
            print("gateway wallet state查看钱包状态失败，报错信息为：", e)
            a = 0
        assert a == 1, "gateway wallet state查看钱包状态失败"
if __name__ == '__main__':
    pytest.main()
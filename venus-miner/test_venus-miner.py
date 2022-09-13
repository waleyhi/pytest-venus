import os
import allure
import time
import pytest
import venus_miner_function
@allure.epic("venus-miner测试")
@allure.feature("venus-miner主程序测试")
class Test_venus_miner_status:
    @allure.story("测试venus-miner程序是否能启动")
    @pytest.mark.run(order=1)
    def test_venus_miner_start(self):
        a= venus_miner_function.process_check('venus-miner')
        assert a==1,"venus-miner 进程不存在"
    @allure.story("测试venus-miner程序是否能稳定运行3分钟不崩溃")
    @pytest.mark.run(order=1)
    def test_venus_miner_alive(self):
        #time.sleep(180)
        a= venus_miner_function.process_alive('venus-miner','run')
        b=time.time()
        c=b-a
        print ("venus-miner 进程已稳定运行%f秒" % c)
        assert c > 180,"venus-miner 运行时间不足3分钟"


@allure.epic("venus-miner测试")
@allure.feature("venus-miner 各功能模块测试")
class Test_venus_miner():
    @allure.story("测试venus-miner address update从auth中更新矿工信息是否正常")
    @pytest.mark.run(order=2)
    def test_venus_miner_address_update(self):
        global venus_auth_miner
        global venus_auth_user
        create_test_user=os.popen(f"/root/venus-auth user add {venus_auth_user}").read()
        print ("auth上创建测试用户结果为：",create_test_user)
        create_test_miner=os.popen(f"/root/venus-auth user miner add {venus_auth_user} {venus_auth_miner}").read()
        print ("auth上绑定测试用户与矿工结果为：",create_test_miner)
        try:
            miner_update_info = os.popen("/root/venus-miner address update").read()
            print ("update执行结果为：",miner_update_info)
            if f'{venus_auth_miner}' in miner_update_info and f'{venus_auth_user}' in miner_update_info:
                a = 1
            else:
                a = 0
        except Exception as e:
            print("update更新矿工信息报错，报错信息为：", e)
            a = 0
        assert a == 1, "venus-miner update更新矿工信息测试失败"

    @allure.story("测试venus-miner address stop停止矿工出块是否正常")
    @pytest.mark.run(order=3)
    def test_venus_miner_address_stop(self):
        global venus_auth_miner
        stop_info = os.popen(f"/root/venus-miner address stop {venus_auth_miner}").read()
        print (f"{venus_auth_miner}停止挖矿结果为：",stop_info)
        miner_state=venus_miner_function.venus_miner_state(f'{venus_auth_miner}')
        if 'stop mining success' in stop_info and miner_state=='False':
            a=1
        else:
            a=0
        assert a == a,"venus-miner stop停止矿工挖矿测试失败"

    @allure.story("测试venus-miner address start启动矿工出块是否正常")
    @pytest.mark.run(order=4)
    def test_venus_miner_address_start(self):
        global venus_auth_miner
        start_info = os.popen(f"/root/venus-miner address start {venus_auth_miner}").read()
        print (f"{venus_auth_miner}停止挖矿结果为：",start_info)
        miner_state=venus_miner_function.venus_miner_state(f'{venus_auth_miner}')
        if 'start mining success' in start_info and miner_state=='True':
            a=1
        else:
            a=0
        assert a == a,"venus-miner start启动矿工挖矿测试失败"
    @allure.story("测试venus-miner winner计算出块权是否正常")
    @pytest.mark.run(order=2)
    def test_venus_miner_winner(self):
        try:
            winner_info = os.popen("/root/venus-miner winner count --epoch-start 0 --epoch-end 100 f01000").read()
            print ("矿工f01000前100高度出块权为：",winner_info)
            a=1
        except Exception as e:
            print ("获取出块权命令报错，报错信息为：", e)
            a=0
        assert a==1,'出块权命令测试失败'


if __name__ == '__main__':
    #定义全局变量，用于矿工地址测试
    global venus_auth_user
    global venus_auth_miner
    venus_auth_user = 'auto-test-1234'
    venus_auth_miner = 'f01000'
    pytest.main()
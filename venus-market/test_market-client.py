import os
import allure
import time
import pytest
import venus_market_function
@allure.epic("venus-market测试")
@allure.feature("venus-market主程序测试")
class Test_venus_market_status:
    @allure.story("测试venus-market程序是否能启动")
    @pytest.mark.run(order=1)
    def test_venus_market_start(self):
        a= venus_market_function.process_check('venus-market')
        assert a==1,"venus-market 进程不存在"
    @allure.story("测试venus-market程序是否能稳定运行3分钟不崩溃")
    @pytest.mark.run(order=1)
    def test_venus_market_alive(self):
        #time.sleep(180)
        a= venus_market_function.process_alive('venus-market','pool-run')
        b=time.time()
        c=b-a
        print ("venus-market 进程已稳定运行%f秒" % c)
        assert c > 180,"venus-market 运行时间不足3分钟"

@allure.epic("venus-market测试")
@allure.feature("venus-market pieces功能模块测试")
class Test_venus_market_piece:
    @allure.story("测试venus-market pieces list-pieces查看pieces信息是否正常")
    @pytest.mark.run(order=2)
    def test_venus_market_pieces_list_pieces(self):
        try:
            list_pieces=os.popen("/root/venus-market pieces list-pieces").readlines()
            print ("list-pieces执行结果为：",list_pieces)
            a=1
        except Exception as e:
            print("list-pieces执行报错，报错信息为：", e)
            a = 0
        assert a == 1, "list-pieces查看pieces信息测试失败"

    @allure.story("测试venus-market address stop停止矿工出块是否正常")
    @pytest.mark.run(order=3)
    def test_venus_market_address_stop(self):
        venus_auth_market=venus_market_function.venus_auth_test_market()
        stop_info = os.popen(f"/root/venus-market address stop {venus_auth_market}").read()
        print (f"{venus_auth_market}停止挖矿结果为：",stop_info)
        market_state=venus_market_function.venus_market_state(f'{venus_auth_market}')
        if 'stop mining success' in stop_info and market_state=='False':
            a=1
        else:
            a=0
        assert a == 1,"venus-market stop停止矿工挖矿测试失败"


if __name__ == '__main__':
    pytest.main()
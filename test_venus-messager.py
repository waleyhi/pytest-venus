import os
import allure
import time
import psutil
import pytest
import function
@allure.epic("venus-messager测试")
@allure.feature("venus-messager主程序测试")
class Test_venus_messager_status():
    @allure.story("测试venus-messager程序是否能启动")
    def test_venus_messager_start(self):
        a=function.process_check(venus-messager)
        assert a==1,"venus-messager 进程不存在"
    @allure.story("测试venus-messager程序是否能稳定运行3分钟不崩溃")
    def test_venus_messager_alive(self):
        #time.sleep(180)
        a=function.process_alive(venus-messager,run)
        b=time.time()
        c=b-a
        print ("venus-messager 进程已稳定运行%f秒" % c)
        assert c > 180,"venus-messager 运行时间不足3分钟"

if __name__ == '__main__':
    global user_name
    global user_rm
    global token_rm
    pytest.main()
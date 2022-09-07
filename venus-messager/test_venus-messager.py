import os
import allure
import time
import pytest
import venus_messager_function
@allure.epic("venus-messager测试")
@allure.feature("venus-messager主程序测试")
class Test_venus_messager_status():
    @allure.story("测试venus-messager程序是否能启动")
    @pytest.mark.run(order=1)
    def test_venus_messager_start(self):
        a= venus_messager_function.process_check('venus-messager')
        assert a==1,"venus-messager 进程不存在"
    @allure.story("测试venus-messager程序是否能稳定运行3分钟不崩溃")
    @pytest.mark.run(order=1)
    def test_venus_messager_alive(self):
        #time.sleep(180)
        a= venus_messager_function.process_alive('venus_messager', 'run')
        b=time.time()
        c=b-a
        print ("venus-messager 进程已稳定运行%f秒" % c)
        assert c > 180,"venus-messager 运行时间不足3分钟"

@allure.epic("venus-messager测试")
@allure.feature("venus-messager msg功能模块测试")
class Test_venus_messager_msg():
    @allure.story("测试venus-messager msg list查看消息是否正常")
    @pytest.mark.run(order=2)
    def test_venus_messager_msg_list(self):
        try:
            messager_msg_list = os.popen("/root/venus-messager msg list").readlines()
            print ("messager msg list执行结果为：",messager_msg_list)
            a=1
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,"messager msg list 执行报错"
    @allure.story("测试venus-messager msg list-fail查看失败消息是否正常")
    @pytest.mark.run(order=2)
    def test_venus_messager_msg_list_fail(self):
        try:
            messager_msg_list_fail = os.popen("/root/venus-messager msg list-fail").readlines()
            print ("messager msg list-fail执行结果为：",messager_msg_list_fail)
            a=1
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,"messager msg list-fail 执行报错"
    @allure.story("测试venus-messager msg list-blocked查看消息是否正常")
    @pytest.mark.run(order=2)
    def test_venus_messager_msg_list_blocked(self):
        try:
            messager_msg_list_blocked = os.popen("/root/venus-messager msg list-blocked").readlines()
            print ("messager msg list执行结果为：",messager_msg_list_blocked)
            a=1
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,"messager msg list-blocked 执行报错"
    @allure.story("测试venus-messager msg search搜索指定消息是否正常")
    @pytest.mark.run(order=3)
    def test_venus_messager_msg_search_id(self):
        msg_id= venus_messager_function.venus_messager_id_get('list')
        try:
            messager_msg_search_id_info = os.popen(f"/root/venus-messager msg search --id {msg_id}").readlines()
            print ("命令执行结果为：",messager_msg_search_id_info)
            if 'record not found' in messager_msg_search_id_info[0]:
                print ("查询消息失败")
                a=0
            else:
                a=1
        except Exception as e:
            print ("msg search 信息报错，报错信息为：",e)
            a=0
        assert a==1,"venus-messager msg search --id测试失败"
@allure.epic("venus-messager测试")
@allure.feature("venus-messager address功能模块测试")
class Test_venus_messager_address():
    @allure.story("测试venus-messager address list查看地址信息是否正常")
    @pytest.mark.run(order=1)
    def test_venus_messager_address_list(self):
        try:
            messager_address_list = os.popen("/root/venus-messager address list").readlines()
            print ("messager address list执行结果为：",messager_address_list)
            a=1
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,"messager address list 执行报错"
    @allure.story("测试venus-messager address search搜索指定地址信息是否正常")
    @pytest.mark.run(order=2)
    def test_venus_messager_address_search(self):
        global address_addr
        address_addr= venus_messager_function.venus_messager_address_get()
        try:
            messager_address_search = os.popen(f"/root/venus-messager address search {address_addr}").readlines()
            print ("命令执行结果为：",messager_address_search)
            if 'invalid address checksum' in messager_address_search[0]:
                print ("搜索地址失败")
                a=0
            else:
                a=1
        except Exception as e:
            print ("address search 信息报错，报错信息为：",e)
            a=0
        assert a==1,"venus-messager address search 测试失败"
    @allure.story("测试venus-messager address forbidden禁用地址是否正常")
    @pytest.mark.run(order=3)
    def test_venus_messager_address_forbidden(self):
        global address_addr
        try:
            messager_address_forbidden = os.popen(f"/root/venus-messager address forbidden {address_addr}").readlines()
            print("命令执行结果为：", messager_address_forbidden)
            address_status= venus_messager_function.venus_messager_address_state(f'{address_addr}')
            if address_status=='4,' and 'forbidden address success!' == messager_address_forbidden[0]:
                a = 1
            else:
                a = 0
        except Exception as e:
            print("address forbidden 信息报错，报错信息为：", e)
            a = 0
        assert a == 1, "venus-messager address forbidden 测试失败"
    @allure.story("测试venus-messager address active 激活地址是否正常")
    @pytest.mark.run(order=4)
    def test_venus_messager_address_active(self):
        global address_addr
        try:
            messager_address_active = os.popen(f"/root/venus-messager address active {address_addr}").readlines()
            print("命令执行结果为：", messager_address_active)
            address_status = venus_messager_function.venus_messager_address_state(f'{address_addr}')
            if address_status == '1,' and 'active address success!'==messager_address_active[0]:
                a = 1
            else:
                a = 0
        except Exception as e:
            print("address forbidden 信息报错，报错信息为：", e)
            a = 0
        assert a == 1, "venus-messager address active 测试失败"
    @allure.story("测试venus-messager address del 删除地址是否正常")
    @pytest.mark.run(order=5)
    def test_venus_messager_address_del(self):
        global address_addr
        try:
            messager_address_del = os.popen(f"/root/venus-messager address del {address_addr}").readlines()
            print("命令执行结果为：", messager_address_del)
            #获取删除地址状态
            address_status = venus_messager_function.venus_messager_address_state(f'{address_addr}')
            #如果地址状态为0，则说明已经无法搜索到该地址，删除正常
            if address_status == 0:
                a = 1
            else:
                a = 0
        except Exception as e:
            print("address forbidden 信息报错，报错信息为：", e)
            a = 0
        assert a == 1, "venus-messager address del 测试失败"
if __name__ == '__main__':
    #定义全局变量address_addr，用于forbidden、active、del测试
    global address_addr
    pytest.main()
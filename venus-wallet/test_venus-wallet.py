import os
import allure
import time
import pytest
import venus_wallet_function
@allure.epic("venus-wallet测试")
@allure.feature("venus-wallet主程序测试")
class Test_venus_wallet_status():
    @allure.story("测试venus-wallet程序是否能启动")
    @pytest.mark.run(order=1)
    def test_venus_wallet_start(self):
        a= venus_wallet_function.process_check('venus-wallet')
        assert a==1,"venus-wallet 进程不存在"
    @allure.story("测试venus-wallet程序是否能稳定运行3分钟不崩溃")
    @pytest.mark.run(order=1)
    def test_venus_wallet_alive(self):
        #time.sleep(180)
        a= venus_wallet_function.process_alive('venus-wallet', 'run')
        b=time.time()
        c=b-a
        print ("venus-wallet 进程已稳定运行%f秒" % c)
        assert c > 180,"venus-wallet 运行时间不足3分钟"


@allure.epic("venus-wallet测试")
@allure.feature("venus-wallet msg功能模块测试")
class Test_venus_wallet_msg():
    @allure.story("测试venus-wallet msg list查看消息是否正常")
    @pytest.mark.run(order=2)
    def test_venus_wallet_msg_list(self):
        try:
            wallet_msg_list = os.popen("/root/venus-wallet msg list").readlines()
            print ("wallet msg list执行结果为：",wallet_msg_list)
            a=1
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,"wallet msg list 执行报错"
    @allure.story("测试venus-wallet msg list-fail查看失败消息是否正常")
    @pytest.mark.run(order=2)
    def test_venus_wallet_msg_list_fail(self):
        try:
            wallet_msg_list_fail = os.popen("/root/venus-wallet msg list-fail").readlines()
            print ("wallet msg list-fail执行结果为：",wallet_msg_list_fail)
            a=1
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,"wallet msg list-fail 执行报错"
    @allure.story("测试venus-wallet msg list-blocked查看消息是否正常")
    @pytest.mark.run(order=2)
    def test_venus_wallet_msg_list_blocked(self):
        try:
            wallet_msg_list_blocked = os.popen("/root/venus-wallet msg list-blocked").readlines()
            print ("wallet msg list执行结果为：",wallet_msg_list_blocked)
            a=1
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,"wallet msg list-blocked 执行报错"
    @allure.story("测试venus-wallet msg search搜索指定消息是否正常")
    @pytest.mark.run(order=3)
    def test_venus_wallet_msg_search_id(self):
        msg_id= venus_wallet_function.venus_wallet_id_get('list')
        try:
            wallet_msg_search_id_info = os.popen(f"/root/venus-wallet msg search --id {msg_id}").readlines()
            print ("命令执行结果为：",wallet_msg_search_id_info)
            if 'record not found' in wallet_msg_search_id_info[0]:
                print ("查询消息失败")
                a=0
            else:
                a=1
        except Exception as e:
            print ("msg search 信息报错，报错信息为：",e)
            a=0
        assert a==1,"venus-wallet msg search --id测试失败"


@allure.epic("venus-wallet测试")
@allure.feature("venus-wallet address功能模块测试")
class Test_venus_wallet_address():
    @allure.story("测试venus-wallet address list查看地址信息是否正常")
    @pytest.mark.run(order=1)
    def test_venus_wallet_address_list(self):
        try:
            wallet_address_list = os.popen("/root/venus-wallet address list").read()
            print ("wallet address list执行结果为：",wallet_address_list)
            a=1
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,"wallet address list 执行报错"
    @allure.story("测试venus-wallet address search搜索指定地址信息是否正常")
    @pytest.mark.run(order=2)
    def test_venus_wallet_address_search(self):
        global address_addr
        address_addr= venus_wallet_function.venus_wallet_address_get()
        try:
            wallet_address_search = os.popen(f"/root/venus-wallet address search {address_addr}").readlines()
            print ("命令执行结果为：",wallet_address_search)
            if 'invalid address checksum' in wallet_address_search[0]:
                print ("搜索地址失败")
                a=0
            else:
                a=1
        except Exception as e:
            print ("address search 信息报错，报错信息为：",e)
            a=0
        assert a==1,"venus-wallet address search 测试失败"
    @allure.story("测试venus-wallet address set-sel-msg-num指定地址设置消息推送数量是否正常")
    @pytest.mark.run(order=3)
    def test_venus_wallet_address_set_sel_msg_num(self):
        global address_addr
        try:
            os.popen(f"/root/venus-wallet address set-sel-msg-num --num=1234 {address_addr}")
            wallet_address_list = os.popen(f"/root/venus-wallet address search {address_addr}").read()
            address_info_dict=eval(wallet_address_list)
            if address_info_dict['selMsgNum'] == 1234:
                a=1
            else:
                a=0
        except Exception as e:
            print ("命令执行报错，报错信息为：",e)
            a=0
        assert a==1,"address set-sel-msg-num测试失败"
    @allure.story("测试venus-wallet address set-fee-params指定地址设置消息gas参数是否正常")
    @pytest.mark.run(order=3)
    def test_venus_wallet_address_set_fee_params(self):
        global address_addr
        try:
            os.popen(f"/root/venus-wallet address set-fee-params --gas-overestimation=1.6 --max-feecap=7 --max-fee=7 {address_addr}")
            wallet_address_list = os.popen(f"/root/venus-wallet address search {address_addr}").read()
            address_info_dict = eval(wallet_address_list)
            if address_info_dict['gasOverEstimation'] == 1.6 and address_info_dict['maxFee']=='7' and address_info_dict['maxFeeCap']=='7':
                a = 1
            else:
                a = 0
        except Exception as e:
            print("命令执行报错，报错信息为：", e)
            a = 0
        assert a == 1, "address set-fee-params测试失败"
    @allure.story("测试venus-wallet address forbidden禁用地址是否正常")
    @pytest.mark.run(order=3)
    def test_venus_wallet_address_forbidden(self):
        global address_addr
        try:
            wallet_address_forbidden = os.popen(f"/root/venus-wallet address forbidden {address_addr}").readlines()
            print("命令执行结果为：", wallet_address_forbidden)
            address_status= venus_wallet_function.venus_wallet_address_state(f'{address_addr}')
            if address_status=='4,' and 'forbidden address success!' in wallet_address_forbidden[0]:
                a = 1
            else:
                a = 0
        except Exception as e:
            print("address forbidden 信息报错，报错信息为：", e)
            a = 0
        assert a == 1, "venus-wallet address forbidden 测试失败"
    @allure.story("测试venus-wallet address active 激活地址是否正常")
    @pytest.mark.run(order=4)
    def test_venus_wallet_address_active(self):
        global address_addr
        try:
            wallet_address_active = os.popen(f"/root/venus-wallet address active {address_addr}").readlines()
            print("命令执行结果为：", wallet_address_active)
            address_status = venus_wallet_function.venus_wallet_address_state(f'{address_addr}')
            if address_status == '1,' and 'active address success!' in wallet_address_active[0]:
                a = 1
            else:
                a = 0
        except Exception as e:
            print("address forbidden 信息报错，报错信息为：", e)
            a = 0
        assert a == 1, "venus-wallet address active 测试失败"
    @allure.story("测试venus-wallet address del 删除地址是否正常")
    @pytest.mark.run(order=5)
    def test_venus_wallet_address_del(self):
        global address_addr
        try:
            wallet_address_del = os.popen(f"/root/venus-wallet address del {address_addr}").readlines()
            print("命令执行结果为：", wallet_address_del)
            #获取删除地址状态
            address_status = venus_wallet_function.venus_wallet_address_state(f'{address_addr}')
            #如果地址状态为0，则说明已经无法搜索到该地址，删除正常
            if address_status == 0:
                a = 1
            else:
                a = 0
        except Exception as e:
            print("address forbidden 信息报错，报错信息为：", e)
            a = 0
        assert a == 1, "venus-wallet address del 测试失败"


@allure.epic("venus-wallet测试")
@allure.feature("venus-wallet share-params功能模块测试")
class Test_venus_wallet_share_params():
    @allure.story("测试venus-wallet share-params 查看当前消息推送参数是否正常")
    @pytest.mark.run(order=1)
    def test_venus_wallet_share_params_get(self):
        try:
            share_params_get=venus_wallet_function.venus_wallet_share_params_get()
            print ("wallet share-params get执行结果为：",share_params_get)
            if 'gasOverEstimation' in share_params_get:
                a=1
            else:
                a=0
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,"wallet share-params get 测试报错"
    @allure.story("测试venus-wallet share-params set修改消息推送参数是否正常")
    @pytest.mark.run(order=1)
    def test_venus_wallet_share_params_set(self):
        try:
            wallet_share_params_set = os.popen("/root/venus-wallet share-params set --gas-over-estimation=1.5 --max-fee=7 --max-feecap=7000000000 --sel-msg-num=1").read()
            share_params_get=venus_wallet_function.venus_wallet_share_params_get()
            #转化为字典
            params_dict=eval(share_params_get)
            if params_dict['gasOverEstimation']==1.5 and params_dict['maxFee']=='7' and params_dict['maxFeeCap']=='7000000000' and params_dict['selMsgNum']==1:
                a=1
            else:
                a=0
        except Exception as e:
            print ("命令报错，报错信息为：",e)
            a=0
        assert a==1,"wallet share-params set测试失败"
if __name__ == '__main__':
    #定义全局变量address_addr，在search测试模块中赋值，用于forbidden、active、del测试
    global address_addr
    pytest.main()
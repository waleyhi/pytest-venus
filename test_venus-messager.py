import os
import allure
import time
import psutil
import pytest
@allure.epic("venus-messager测试")
@allure.feature("venus-messager主程序测试")
class Test_venus_messager_status():
    @allure.story("测试venus-messager程序是否能启动")
    def test_venus_messager_start(self):
        for i in psutil.pids():
            if psutil.Process(i).name()=="venus-messager":
                print ("venus-messager进程正在运行,进程号为:%s" % i)
                a=1
                break
            else:
                a=0
        assert a==1,"venus-messager 进程不存在"
    @allure.story("测试venus-messager程序是否能稳定运行3分钟不崩溃")
    def test_venus_messager_alive(self):
        #time.sleep(180)
        venus_messager_pid=[pid for pid in psutil.pids() if psutil.Process(pid).name()=="venus-messager" and psutil.Process(pid).cmdline()[1]=="run"]
        a=psutil.Process(venus_messager_pid[0]).create_time()
        b=time.time()
        c=b-a
        print ("venus-messager 进程已稳定运行%f秒" % c)
        assert c > 180,"venus-messager 运行时间不足3分钟"

@allure.epic("venus-messager测试")
@allure.feature("venus-messager token各命令测试")
class Test_venus_messager_token():
    @allure.story("测试venus-messager token gen生成token是否成功")
    @pytest.mark.run(order=1)
    def test_venus_messager_token_gen(self):
        token_type=['read','write','sign','admin']
        for i in token_type:
            try:
                messager_gen_info = os.popen(f"/root/venus-messager token gen --perm={i} auto-test-{i}").readlines()[0]
                print (f"messager创建{i}权限token命令结果为：",messager_gen_info)
                if 'generate token success' in messager_gen_info:
                    a=1
                else:
                    a=0
                    break
            except Exception as e:
                print (f"messager创建{i}权限token报错，报错信息为：",e)
                a=0
        assert a==1,f"messager创建{i}权限token失败"
    @allure.story("测试venus-messager token get查询token是否成功")
    @pytest.mark.run(order=2)
    def test_venus_messager_token_get(self):
        venus_token_list = os.popen("/root/venus-messager token list").readlines()
        auto_token=[token for token in venus_token_list if 'auto-test' in token]
        try:
            messager_token_get_name = os.popen(f"/root/venus-messager token get --name={auto_token[0].split()[1]}").readlines()
            messager_token_get_token = os.popen(f"/root/venus-messager token get --token={auto_token[0].split()[5]}").readlines()
            print ("通过name查询token信息结果为：",messager_token_get_name)
            print ("通过token查询token信息结果为：",messager_token_get_token)
            a=1
        except Exception as e:
            a=0
        assert a==1,"通过venus-messager token get查询token信息失败"
    @allure.story("测试venus-messager token list查询全部token是否成功")
    @pytest.mark.run(order=2)
    def test_venus_messager_token_list(self):
        try:
            venus_token_list = os.popen("/root/venus-messager token list").readlines()
            print ("venus-messager token list执行结果为：",venus_token_list)
            a=1
        except Exception as e:
            a=0
        assert a==1,"venus-messager token list查看token信息失败"
    @allure.story("测试venus-messager token rm删除token是否成功")
    @pytest.mark.run(order=3)
    def test_venus_messager_token_rm(self):
        venus_token_list = os.popen("/root/venus-messager token list").readlines()
        #获取token详细信息
        token = [token for token in venus_token_list if 'auto-test' in token]
        #截取token地址
        global token_rm
        token_rm=token[0].split()[5]
        try:
            messager_token_rm = os.popen(f"/root/venus-messager token rm {token_rm}").readlines()
            print ("删除token信息结果为：",messager_token_rm)
            a=1
        except Exception as e:
            print ("报错信息为：",e)
            a=0
        assert a==1,"messager删除token失败"
    @allure.story("测试venus-messager token recover恢复token是否成功")
    @pytest.mark.run(order=4)
    def test_venus_messager_token_recover(self):
        global token_rm
        try:
            messager_token_recover = os.popen(f"/root/venus-messager token recover {token_rm}").readlines()
            print ("已删除token恢复结果为：",messager_token_recover,token_rm)
            a=1
        except Exception as e:
            print ("报错信息为：",e)
            a=0
        assert a==1,"messager恢复token失败"
@allure.epic("venus-messager测试")
@allure.feature("venus-messager user各命令测试")
class Test_venus_messager_user():
    @allure.story("测试venus-messager user add创建用户是否成功")
    @pytest.mark.run(order=1)
    def test_venus_messager_user_add(self):
        try:
            messager_user_add = os.popen(f"/root/venus-messager user add --comment '自动化测试用户' auto-test-{time.time()}").readlines()
            print("messager创建用户信息为：", messager_user_add)
            if 'Add user success' in messager_user_add[0]:
                a=1
            else:
                a=0
        except Exception as e:
            print ("messager user add 命令执行报错，报错信息为：",e)
            a=0
        assert a==1,"messager创建用户报错"
    @allure.story("测试venus-messager user list查看用户是否成功")
    @pytest.mark.run(order=2)
    def test_venus_messager_user_list(self):
        try:
            messager_user_list = os.popen(f"/root/venus-messager user list").readlines()
            print ("messager list用户信息为：",messager_user_list)
            messager_user_list_info=[x for x in messager_user_list if 'auto-test' in x]
            if len(messager_user_list_info) != 0:
                a=1
            else:
                a=0
        except Exception as e:
            print ("messager user list命令执行报错，报错信息为：",e)
            a=0
        assert a==1,"messager list查看用户信息失败"
    @allure.story("测试venus-messager user update更新用户信息是否成功")
    @pytest.mark.run(order=2)
    def test_venus_messager_user_update(self):
        messager_user_list = os.popen(f"/root/venus-messager user list").readlines()
        messager_user_list_info = [x for x in messager_user_list if 'auto-test' in x]
        #获取自动创建的用户
        user_update=messager_user_list_info[0].split()[1]
        try:
            messager_user_update = os.popen(f"/root/venus-messager user update --name={user_update} --comment='自动测试更新user信息' --state=2").readlines()
            print ("messager update用户信息为：",messager_user_update)
            if 'update user success' in messager_user_update[0]:
                a=1
            else:
                a=0
        except Exception as e:
            print ("messager user update命令执行报错，报错信息为：",e)
            a=0
        assert a==1,"messager user update更新用户信息失败"
    @allure.story("测试venus-messager user get搜索用户是否成功")
    @pytest.mark.run(order=2)
    def test_venus_messager_user_get(self):
        messager_user_list = os.popen(f"/root/venus-messager user list").readlines()
        messager_user_list_info = [x for x in messager_user_list if 'auto-test' in x]
        # 获取自动创建的用户
        user_get = messager_user_list_info[0].split()[1]
        try:
            messager_user_get = os.popen(f"/root/venus-messager user get {user_get}").readlines()
            print ("messager get用户信息为：",messager_user_get)
            str_get_info=("".join(messager_user_get))
            if f"{user_get}" in str_get_info:
                a=1
            else:
                a=0
        except Exception as e:
            print ("messager user get命令执行报错，报错信息为：",e)
            a=0
        assert a==1,"messager user get查询用户信息失败"
    @allure.story("测试venus-messager user rm删除用户是否成功")
    @pytest.mark.run(order=3)
    def test_venus_messager_user_rm(self):
        messager_user_list = os.popen(f"/root/venus-messager user list").readlines()
        messager_user_list_info = [x for x in messager_user_list if 'auto-test' in x]
        # 获取自动创建的用户
        global user_rm
        user_rm = messager_user_list_info[0].split()[1]
        try:
            messager_user_rm = os.popen(f"/root/venus-messager user rm {user_rm}").readlines()
            print("messager user rm用户信息为：", messager_user_rm)
            if 'remove user success' in messager_user_rm[0]:
                a = 1
            else:
                a = 0
        except Exception as e:
            print ("messager user rm命令执行报错，报错信息为：",e)
            a=0
        assert a==1,"messager user rm删除用户信息失败"
    @allure.story("测试venus-messager user recover恢复用户是否成功")
    @pytest.mark.run(order=4)
    def test_venus_messager_user_recover(self):
        global user_rm
        try:
            messager_user_recover = os.popen(f"/root/venus-messager user recover {user_rm}").readlines()
            print("messager user recover用户信息为：", messager_user_recover,user_rm)
            if 'recover user success' in messager_user_recover[0]:
                a = 1
            else:
                a = 0
        except Exception as e:
            print("messager user recover命令执行报错，报错信息为：", e)
            a = 0
        assert a==1,"messager user recover恢复用户信息失败"
    @allure.story("测试venus-messager user miner add给用户添加矿工是否成功")
    @pytest.mark.run(order=4)
    def test_venus_messager_user_miner_add(self):
        messager_user_list = os.popen(f"/root/venus-messager user list").readlines()
        messager_user_list_info = [x for x in messager_user_list if 'auto-test' in x]
        global user_name
        user_name = messager_user_list_info[0].split()[1]
        try:
            messager_user_miner_add = os.popen(f"/root/venus-messager user miner add {user_name} t0123456").readlines()
            print ("messager user miner add执行结果为：",messager_user_miner_add)
            if 'success' in messager_user_miner_add[0]:
                a=1
            else:
                a=0
        except Exception as e:
            print ("messager user miner add命令执行报错，报错信息为：",e)
            a=0
        assert a==1,"messager user miner add给用户添加矿工失败"
    @allure.story("测试venus-messager user miner list查看用户矿工信息是否成功")
    @pytest.mark.run(order=5)
    def test_venus_messager_user_miner_list(self):
        global user_name
        try:
            messager_user_miner_list = os.popen(f"/root/venus-messager user miner list {user_name}").readlines()
            print("messager user miner list执行结果为：", messager_user_miner_list)
            if '0123456' in ("".join(messager_user_miner_list)):
                a=1
            else:
                a=0
        except Exception as e:
            print ("messager user miner list命令执行报错，报错信息为：",e)
            a=0
        assert a==1,"messager user miner list查看用户矿工信息失败"
    @allure.story("测试venus-messager user miner rm删除用户矿工是否成功")
    @pytest.mark.run(order=6)
    def test_venus_messager_user_miner_rm(self):
        try:
            messager_user_miner_rm = os.popen(f"/root/venus-messager user miner rm t0123456").readlines()
            print("messager user miner rm执行结果为：", messager_user_miner_rm)
            if 'success' in ("".join(messager_user_miner_rm)):
                a = 1
            else:
                a = 0
        except Exception as e:
            print("messager user miner rm命令执行报错，报错信息为：", e)
            a = 0
        assert a == 1, "messager user miner rm删除用户矿工信息失败"
if __name__ == '__main__':
    global user_name
    global user_rm
    global token_rm
    pytest.main()
import os
import allure
import time
import psutil
import pytest
@allure.epic("venus-auth测试")
@allure.feature("venus-auth主程序测试")
class Test_venus_auth_status():
    @allure.story("测试venus-auth程序是否能启动")
    def test_venus_auth_start(self):
        for i in psutil.pids():
            if psutil.Process(i).name()=="venus-auth":
                print ("venus-auth进程正在运行,进程号为:%s" % i)
                a=1
                break
            else:
                a=0
        assert a==1,"venus-auth 进程不存在"
    @allure.story("测试venus-auth程序是否能稳定运行3分钟不崩溃")
    def test_venus_auth_alive(self):
        #time.sleep(180)
        venus_auth_pid=[pid for pid in psutil.pids() if psutil.Process(pid).name()=="venus-auth" and psutil.Process(pid).cmdline()[1]=="run"]
        a=psutil.Process(venus_auth_pid[0]).create_time()
        b=time.time()
        c=b-a
        print ("venus-auth 进程已稳定运行%f秒" % c)
        assert c > 180,"venus-auth 运行时间不足3分钟"

@allure.epic("venus-auth测试")
@allure.feature("venus-auth token各命令测试")
class Test_venus_auth_token():
    @allure.story("测试venus-auth token gen生成token是否成功")
    @pytest.mark.run(order=1)
    def test_venus_auth_token_gen(self):
        token_type=['read','write','sign','admin']
        for i in token_type:
            try:
                auth_gen_info = os.popen(f"/root/venus-auth token gen --perm={i} auto-test-{i}").readlines()[0]
                print (f"auth创建{i}权限token命令结果为：",auth_gen_info)
                if 'generate token success' in auth_gen_info:
                    a=1
                else:
                    a=0
                    break
            except Exception as e:
                print (f"auth创建{i}权限token报错，报错信息为：",e)
                a=0
        assert a==1,f"auth创建{i}权限token失败"
    @allure.story("测试venus-auth token get查询token是否成功")
    @pytest.mark.run(order=2)
    def test_venus_auth_token_get(self):
        venus_token_list = os.popen("/root/venus-auth token list").readlines()
        auto_token=[token for token in venus_token_list if 'auto-test' in token]
        try:
            auth_token_get_name = os.popen(f"/root/venus-auth token get --name={auto_token[0].split()[1]}").readlines()
            auth_token_get_token = os.popen(f"/root/venus-auth token get --token={auto_token[0].split()[5]}").readlines()
            print ("通过name查询token信息结果为：",auth_token_get_name)
            print ("通过token查询token信息结果为：",auth_token_get_token)
            a=1
        except Exception as e:
            a=0
        assert a==1,"通过venus-auth token get查询token信息失败"
    @allure.story("测试venus-auth token list查询全部token是否成功")
    @pytest.mark.run(order=2)
    def test_venus_auth_token_list(self):
        try:
            venus_token_list = os.popen("/root/venus-auth token list").readlines()
            print ("venus-auth token list执行结果为：",venus_token_list)
            a=1
        except Exception as e:
            a=0
        assert a==1,"venus-auth token list查看token信息失败"
    @allure.story("测试venus-auth token rm删除token是否成功")
    @pytest.mark.run(order=3)
    def test_venus_auth_token_rm(self):
        venus_token_list = os.popen("/root/venus-auth token list").readlines()
        #获取token详细信息
        token = [token for token in venus_token_list if 'auto-test' in token]
        #截取token地址
        global token_rm
        token_rm=token[0].split()[5]
        try:
            auth_token_rm = os.popen(f"/root/venus-auth token rm {token_rm}").readlines()
            print ("删除token信息结果为：",auth_token_rm)
            a=1
        except Exception as e:
            print ("报错信息为：",e)
            a=0
        assert a==1,"auth删除token失败"
    @allure.story("测试venus-auth token recover恢复token是否成功")
    @pytest.mark.run(order=4)
    def test_venus_auth_token_recover(self):
        global token_rm
        try:
            auth_token_recover = os.popen(f"/root/venus-auth token recover {token_rm}").readlines()
            print ("已删除token恢复结果为：",auth_token_recover,token_rm)
            a=1
        except Exception as e:
            print ("报错信息为：",e)
            a=0
        assert a==1,"auth恢复token失败"
@allure.epic("venus-auth测试")
@allure.feature("venus-auth user各命令测试")
class Test_venus_auth_user():
    @allure.story("测试venus-auth user add创建用户是否成功")
    @pytest.mark.run(order=1)
    def test_venus_auth_user_add(self):
        try:
            auth_user_add = os.popen(f"/root/venus-auth user add --comment '自动化测试用户' auto-test-{time.time()}").readlines()
            print("auth创建用户信息为：", auth_user_add)
            if 'Add user success' in auth_user_add[0]:
                a=1
            else:
                a=0
        except Exception as e:
            print ("auth user add 命令执行报错，报错信息为：",e)
            a=0
        assert a==1,"auth创建用户报错"
    @allure.story("测试venus-auth user list查看用户是否成功")
    @pytest.mark.run(order=2)
    def test_venus_auth_user_list(self):
        try:
            auth_user_list = os.popen(f"/root/venus-auth user list").readlines()
            print ("auth list用户信息为：",auth_user_list)
            auth_user_list_info=[x for x in auth_user_list if 'auto-test' in x]
            if len(auth_user_list_info) != 0:
                a=1
            else:
                a=0
        except Exception as e:
            print ("auth user list命令执行报错，报错信息为：",e)
            a=0
        assert a==1,"auth list查看用户信息失败"
    @allure.story("测试venus-auth user update更新用户信息是否成功")
    @pytest.mark.run(order=2)
    def test_venus_auth_user_update(self):
        auth_user_list = os.popen(f"/root/venus-auth user list").readlines()
        auth_user_list_info = [x for x in auth_user_list if 'auto-test' in x]
        #获取自动创建的用户
        user_update=auth_user_list_info[0].split()[1]
        try:
            auth_user_update = os.popen(f"/root/venus-auth user update --name={user_update} --comment='自动测试更新user信息' --state=2").readlines()
            print ("auth update用户信息为：",auth_user_update)
            if 'update user success' in auth_user_update[0]:
                a=1
            else:
                a=0
        except Exception as e:
            print ("auth user update命令执行报错，报错信息为：",e)
            a=0
        assert a==1,"auth user update更新用户信息失败"
    @allure.story("测试venus-auth user get搜索用户是否成功")
    @pytest.mark.run(order=2)
    def test_venus_auth_user_get(self):
        auth_user_list = os.popen(f"/root/venus-auth user list").readlines()
        auth_user_list_info = [x for x in auth_user_list if 'auto-test' in x]
        # 获取自动创建的用户
        user_get = auth_user_list_info[0].split()[1]
        try:
            auth_user_get = os.popen(f"/root/venus-auth user get {user_get}").readlines()
            print ("auth get用户信息为：",auth_user_get)
            str_get_info=("".join(auth_user_get))
            if f"{user_get}" in str_get_info:
                a=1
            else:
                a=0
        except Exception as e:
            print ("auth user get命令执行报错，报错信息为：",e)
            a=0
        assert a==1,"auth user get查询用户信息失败"
    @allure.story("测试venus-auth user rm删除用户是否成功")
    @pytest.mark.run(order=3)
    def test_venus_auth_user_rm(self):
        auth_user_list = os.popen(f"/root/venus-auth user list").readlines()
        auth_user_list_info = [x for x in auth_user_list if 'auto-test' in x]
        # 获取自动创建的用户
        global user_rm
        user_rm = auth_user_list_info[0].split()[1]
        try:
            auth_user_rm = os.popen(f"/root/venus-auth user rm {user_rm}").readlines()
            print("auth user rm用户信息为：", auth_user_rm)
            if 'remove user success' in auth_user_rm[0]:
                a = 1
            else:
                a = 0
        except Exception as e:
            print ("auth user rm命令执行报错，报错信息为：",e)
            a=0
        assert a==1,"auth user rm删除用户信息失败"
    @allure.story("测试venus-auth user recover恢复用户是否成功")
    @pytest.mark.run(order=4)
    def test_venus_auth_user_recover(self):
        global user_rm
        try:
            auth_user_recover = os.popen(f"/root/venus-auth user recover {user_rm}").readlines()
            print("auth user recover用户信息为：", auth_user_recover,user_rm)
            if 'recover user success' in auth_user_recover[0]:
                a = 1
            else:
                a = 0
        except Exception as e:
            print("auth user recover命令执行报错，报错信息为：", e)
            a = 0
        assert a==1,"auth user recover恢复用户信息失败"
    @allure.story("测试venus-auth user miner add给用户添加矿工是否成功")
    @pytest.mark.run(order=4)
    def test_venus_auth_user_miner_add(self):
        auth_user_list = os.popen(f"/root/venus-auth user list").readlines()
        auth_user_list_info = [x for x in auth_user_list if 'auto-test' in x]
        global user_name
        user_name = auth_user_list_info[0].split()[1]
        try:
            auth_user_miner_add = os.popen(f"/root/venus-auth user miner add {user_name} t0123456").readlines()
            print ("auth user miner add执行结果为：",auth_user_miner_add)
            if 'success' in auth_user_miner_add[0]:
                a=1
            else:
                a=0
        except Exception as e:
            print ("auth user miner add命令执行报错，报错信息为：",e)
            a=0
        assert a==1,"auth user miner add给用户添加矿工失败"
    @allure.story("测试venus-auth user miner list查看用户矿工信息是否成功")
    @pytest.mark.run(order=5)
    def test_venus_auth_user_miner_list(self):
        global user_name
        try:
            auth_user_miner_list = os.popen(f"/root/venus-auth user miner list {user_name}").readlines()
            print("auth user miner list执行结果为：", auth_user_miner_list)
            if '0123456' in ("".join(auth_user_miner_list)):
                a=1
            else:
                a=0
        except Exception as e:
            print ("auth user miner list命令执行报错，报错信息为：",e)
            a=0
        assert a==1,"auth user miner list查看用户矿工信息失败"
    @allure.story("测试venus-auth user miner rm删除用户矿工是否成功")
    @pytest.mark.run(order=6)
    def test_venus_auth_user_miner_rm(self):
        try:
            auth_user_miner_rm = os.popen(f"/root/venus-auth user miner rm t0123456").readlines()
            print("auth user miner rm执行结果为：", auth_user_miner_rm)
            if 'success' in ("".join(auth_user_miner_rm)):
                a = 1
            else:
                a = 0
        except Exception as e:
            print("auth user miner rm命令执行报错，报错信息为：", e)
            a = 0
        assert a == 1, "auth user miner rm删除用户矿工信息失败"
if __name__ == '__main__':
    global user_name
    global user_rm
    global token_rm
    pytest.main()
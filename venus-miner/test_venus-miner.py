import os
import allure
import time
import pytest
import venus_miner_function
import uuid
import pexpect
@allure.epic("venus-miner测试")
@allure.feature("venus-miner主程序测试")
class Test_venus_miner_status():
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
class Test_venus_miner_auth():
    @allure.story("测试venus-miner auth create-token查看token信息是否正常")
    @pytest.mark.run(order=1)
    def test_venus_miner_auth_create_token(self):
        token_type = ['read', 'write', 'sign', 'admin']
        for i in token_type:
            try:
                auth_info = os.popen(f"/root/venus-miner auth create-token --perm={i}").read()
                print(f"{i}权限token为：", auth_info)
                if len(auth_info) > 10:
                    a = 1
                else:
                    a = 0
                    break
            except Exception as e:
                print(f"查看{i}权限token报错，报错信息为：", e)
                a = 0
        assert a == 1, f"查看{i}权限token失败"
    @allure.story("测试venus-miner auth api-info查看token/api信息是否正常")
    @pytest.mark.run(order=1)
    def test_venus_miner_auth_api_info(self):
        token_type = ['read', 'write', 'sign', 'admin']
        for i in token_type:
            try:
                auth_info = os.popen(f"/root/venus-miner auth api-info --perm={i}").read()
                print(f"{i}权限token/api为：", auth_info)
                if len(auth_info) > 10:
                    a = 1
                else:
                    a = 0
                    break
            except Exception as e:
                print(f"查看{i}权限token/api报错，报错信息为：", e)
                a = 0
        assert a == 1, f"查看{i}权限token/api失败"
    @allure.story("测试venus-miner set-password设置密码是否正常")
    @pytest.mark.run(order=1)
    def test_miner_set_password(self):
        process=pexpect.spawn("/root/venus-miner set-password",timeout=180)
        expect_list = ['Password:',pexpect.EOF,pexpect.TIMEOUT,]
        index=process.expect(expect_list)
        if index==0:
            print ("正在第一次输入密码")
            process.sendline("admin123")
            expect_list = ['Enter Password again:',pexpect.EOF,pexpect.TIMEOUT,]
            index=process.expect(expect_list)
            if index==0:
                print ("正在输入第二次密码")
                process.sendline("admin123")
                expect_list = ['Password set successfully.*','the password already exists',pexpect.EOF,pexpect.TIMEOUT,]
                index=process.expect(expect_list)
                if index==0:
                    #process.interact()
                    a=1
                    print("密码设置成功，新密码为admin123")
                elif index == 1:
                    #process.interact()
                    a = 1
                    print("密码已设置，无需再次设置，密码为admin123")
                else:
                    print ('1EOF or TIMEOUT')
                    a=0
            else:
                print("命令执行未出现again字样")
                a=0
                print('EOF or TIMEOUT')
        else:
            print ("命令执行未出现password字样")
            a=0
            print('EOF or TIMEOUT')
        assert a==1,"密码设置失败，请检查venus-miner set-password命令"
    @allure.story("测试venus-miner new生成t1钱包地址是否正常")
    @pytest.mark.run(order=2)
    def test_miner_new(self):
        try:
            miner_new_info=os.popen("/root/venus-miner new secp256k1").read()
            print ("新建t1地址为：",miner_new_info)
            if miner_new_info in venus_miner_function.venus_miner_list():
                a=1
            else:
                a=0
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,'venus-miner new测试创建t1新地址失败'
    @allure.story("测试venus-miner new bls生成t3钱包地址是否正常")
    @pytest.mark.run(order=2)
    def test_miner_new_bls(self):
        try:
            miner_new_info=os.popen("/root/venus-miner new bls").read()
            print ("新建t3地址为：",miner_new_info)
            if miner_new_info in venus_miner_function.venus_miner_list():
                a=1
            else:
                a=0
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,'venus-miner new bls测试创建t3新地址失败'
    @allure.story("测试venus-miner import导入钱包地址是否正常")
    @pytest.mark.run(order=3)
    def test_miner_import(self):
        global miner_addr
        global miner_privete_key
        try:
            miner_import_info=os.popen(f"echo '{miner_privete_key}'|/root/venus-miner import").read()
            print ("import地址结果为：",miner_import_info)
            if 'successfully' in miner_import_info and miner_addr in venus_miner_function.venus_miner_list():
                a=1
            else:
                a=0
        except Exception as e:
            a=0
        assert a==1,'venus-miner import地址测试失败'
    @allure.story("测试venus-miner export导出钱包地址是否正常")
    @pytest.mark.run(order=4)
    def test_miner_export(self):
        global miner_addr
        global miner_privete_key
        try:
            miner_export_info = os.popen(f"echo 'admin123' | /root/venus-miner export {miner_addr}").read()
            print("export地址结果为：", miner_export_info)
            if miner_privete_key in miner_export_info:
                a = 1
            else:
                a = 0
        except Exception as e:
            a = 0
        assert a == 1, 'venus-miner export地址测试失败'
    @allure.story("测试venus-miner del删除钱包地址是否正常")
    @pytest.mark.run(order=5)
    def test_miner_del(self):
        global miner_addr
        try:
            miner_del_info = os.popen(f"echo 'admin123' | /root/venus-miner del {miner_addr}").read()
            print("删除钱包地址结果为：", miner_del_info)
            if 'success' in miner_del_info and miner_addr not in venus_miner_function.venus_miner_list():
                a = 1
            else:
                a = 0
        except Exception as e:
            a = 0
        assert a == 1, 'venus-miner 删除钱包地址测试失败'
    @allure.story("测试venus-miner lock锁定钱包地址是否正常")
    @pytest.mark.run(order=6)
    def test_miner_lock(self):
        try:
            miner_lock_info=os.popen("echo 'admin123' | /root/venus-miner lock").read()
            print ("venus-miner lock测试结果为：",miner_lock_info)
            if 'miner lock successfully' in miner_lock_info or 'miner already locked' in miner_lock_info:
                a=1
            else:
                a=0
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,'venus-miner lock测试锁定钱包地址失败'
    @allure.story("测试venus-miner unlock解锁钱包地址是否正常")
    @pytest.mark.run(order=6)
    def test_miner_unlock(self):
        try:
            miner_unlock_info=os.popen("echo 'admin123' | /root/venus-miner unlock").read()
            print ("venus-miner unlock测试结果为：",miner_unlock_info)
            if 'miner unlock successfully' in miner_unlock_info or 'miner already unlocked' in miner_unlock_info:
                a=1
            else:
                a=0
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,'venus-miner unlock测试解锁钱包地址失败'
    @allure.story("测试venus-miner lock-state查看钱包地址锁定状态是否正常")
    @pytest.mark.run(order=7)
    def test_miner_lock_state(self):
        try:
            miner_lock_state_info=os.popen("/root/venus-miner lock-state").read()
            print ("venus-miner lock-state测试结果为：",miner_lock_state_info)
            if 'miner state: unlocked' in miner_lock_state_info or 'miner state: locked' in miner_lock_state_info:
                a=1
            else:
                a=0
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,'venus-miner lock-state测试查看钱包地址状态失败'
    @allure.story("测试venus-miner support添加支持的用户是否正常")
    @pytest.mark.run(order=1)
    def test_miner_support(self):
        account=uuid.uuid1()
        try:
            os.popen(f"/root/venus-miner support {account}")
            file='/root/.venus_miner/config.toml'
            f=open(file,mode='r')
            file_info=f.readlines()
            f.close()
            print ("测试账号为：",account)
            print ("venus-miner配置文件支持账号信息为：",file_info[-1])
            if str(account) in file_info[-1]:
                a=1
            else:
                a=0
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,'venus-miner lock-state测试查看钱包地址状态失败'
if __name__ == '__main__':
    #定义全局变量，用于地址导入、导出、删除测试
    global miner_addr
    global miner_privete_key
    miner_addr='t3waqhfglxquvmdeqko7jb3qkd6vrpsdaduhnlsbvotu6zajf2dbp4uk5pip3mbjbq6dj4iun7tqzkkh3nrtla'
    miner_privete_key='7b2254797065223a22626c73222c22507269766174654b6579223a225039715136684d414c74695162623955754c48624371586a4d555161576346346774466c6c4759434b52553d227d'
    pytest.main()
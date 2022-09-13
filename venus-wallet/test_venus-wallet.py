import os
import allure
import time
import pytest
import venus_wallet_function
import uuid
import pexpect
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
        a= venus_wallet_function.process_alive('venus-wallet','run')
        b=time.time()
        c=b-a
        print ("venus-wallet 进程已稳定运行%f秒" % c)
        assert c > 180,"venus-wallet 运行时间不足3分钟"


@allure.epic("venus-wallet测试")
@allure.feature("venus-wallet 各功能模块测试")
class Test_venus_wallet_auth():
    @allure.story("测试venus-wallet auth create-token查看token信息是否正常")
    @pytest.mark.run(order=1)
    def test_venus_wallet_auth_create_token(self):
        token_type = ['read', 'write', 'sign', 'admin']
        for i in token_type:
            try:
                auth_info = os.popen(f"/root/venus-wallet auth create-token --perm={i}").read()
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
    @allure.story("测试venus-wallet auth api-info查看token/api信息是否正常")
    @pytest.mark.run(order=1)
    def test_venus_wallet_auth_api_info(self):
        token_type = ['read', 'write', 'sign', 'admin']
        for i in token_type:
            try:
                auth_info = os.popen(f"/root/venus-wallet auth api-info --perm={i}").read()
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
    @allure.story("测试venus-wallet set-password设置密码是否正常")
    @pytest.mark.run(order=1)
    def test_wallet_set_password(self):
        process=pexpect.spawn("/root/venus-wallet set-password",timeout=180)
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
        assert a==1,"密码设置失败，请检查venus-wallet set-password命令"
    @allure.story("测试venus-wallet new生成t1钱包地址是否正常")
    @pytest.mark.run(order=2)
    def test_wallet_new(self):
        try:
            wallet_new_info=os.popen("/root/venus-wallet new secp256k1").read()
            print ("新建t1地址为：",wallet_new_info)
            if wallet_new_info in venus_wallet_function.venus_wallet_list():
                a=1
            else:
                a=0
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,'venus-wallet new测试创建t1新地址失败'
    @allure.story("测试venus-wallet new bls生成t3钱包地址是否正常")
    @pytest.mark.run(order=2)
    def test_wallet_new_bls(self):
        try:
            wallet_new_info=os.popen("/root/venus-wallet new bls").read()
            print ("新建t3地址为：",wallet_new_info)
            if wallet_new_info in venus_wallet_function.venus_wallet_list():
                a=1
            else:
                a=0
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,'venus-wallet new bls测试创建t3新地址失败'
    @allure.story("测试venus-wallet import导入钱包地址是否正常")
    @pytest.mark.run(order=3)
    def test_wallet_import(self):
        global wallet_addr
        global wallet_privete_key
        try:
            wallet_import_info=os.popen(f"echo '{wallet_privete_key}'|/root/venus-wallet import").read()
            print ("import地址结果为：",wallet_import_info)
            if 'successfully' in wallet_import_info and wallet_addr in venus_wallet_function.venus_wallet_list():
                a=1
            else:
                a=0
        except Exception as e:
            a=0
        assert a==1,'venus-wallet import地址测试失败'
    @allure.story("测试venus-wallet export导出钱包地址是否正常")
    @pytest.mark.run(order=4)
    def test_wallet_export(self):
        global wallet_addr
        global wallet_privete_key
        try:
            wallet_export_info = os.popen(f"echo 'admin123' | /root/venus-wallet export {wallet_addr}").read()
            print("export地址结果为：", wallet_export_info)
            if wallet_privete_key in wallet_export_info:
                a = 1
            else:
                a = 0
        except Exception as e:
            a = 0
        assert a == 1, 'venus-wallet export地址测试失败'
    @allure.story("测试venus-wallet del删除钱包地址是否正常")
    @pytest.mark.run(order=5)
    def test_wallet_del(self):
        global wallet_addr
        try:
            wallet_del_info = os.popen(f"echo 'admin123' | /root/venus-wallet del {wallet_addr}").read()
            print("删除钱包地址结果为：", wallet_del_info)
            if 'success' in wallet_del_info and wallet_addr not in venus_wallet_function.venus_wallet_list():
                a = 1
            else:
                a = 0
        except Exception as e:
            a = 0
        assert a == 1, 'venus-wallet 删除钱包地址测试失败'
    @allure.story("测试venus-wallet lock锁定钱包地址是否正常")
    @pytest.mark.run(order=6)
    def test_wallet_lock(self):
        try:
            wallet_lock_info=os.popen("echo 'admin123' | /root/venus-wallet lock").read()
            print ("venus-wallet lock测试结果为：",wallet_lock_info)
            if 'wallet lock successfully' in wallet_lock_info or 'wallet already locked' in wallet_lock_info:
                a=1
            else:
                a=0
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,'venus-wallet lock测试锁定钱包地址失败'
    @allure.story("测试venus-wallet unlock解锁钱包地址是否正常")
    @pytest.mark.run(order=6)
    def test_wallet_unlock(self):
        try:
            wallet_unlock_info=os.popen("echo 'admin123' | /root/venus-wallet unlock").read()
            print ("venus-wallet unlock测试结果为：",wallet_unlock_info)
            if 'wallet unlock successfully' in wallet_unlock_info or 'wallet already unlocked' in wallet_unlock_info:
                a=1
            else:
                a=0
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,'venus-wallet unlock测试解锁钱包地址失败'
    @allure.story("测试venus-wallet lock-state查看钱包地址锁定状态是否正常")
    @pytest.mark.run(order=7)
    def test_wallet_lock_state(self):
        try:
            wallet_lock_state_info=os.popen("/root/venus-wallet lock-state").read()
            print ("venus-wallet lock-state测试结果为：",wallet_lock_state_info)
            if 'wallet state: unlocked' in wallet_lock_state_info or 'wallet state: locked' in wallet_lock_state_info:
                a=1
            else:
                a=0
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,'venus-wallet lock-state测试查看钱包地址状态失败'
    @allure.story("测试venus-wallet support添加支持的用户是否正常")
    @pytest.mark.run(order=1)
    def test_wallet_support(self):
        account=uuid.uuid1()
        try:
            os.popen(f"/root/venus-wallet support {account}")
            file='/root/.venus_wallet/config.toml'
            f=open(file,mode='r')
            file_info=f.readlines()
            f.close()
            print ("测试账号为：",account)
            print ("venus-wallet配置文件支持账号信息为：",file_info[-1])
            if str(account) in file_info[-1]:
                a=1
            else:
                a=0
        except Exception as e:
            print("命令报错,错误信息为：",e)
            a=0
        assert a==1,'venus-wallet lock-state测试查看钱包地址状态失败'
if __name__ == '__main__':
    #定义全局变量，用于地址导入、导出、删除测试
    global wallet_addr
    global wallet_privete_key
    wallet_addr='t3waqhfglxquvmdeqko7jb3qkd6vrpsdaduhnlsbvotu6zajf2dbp4uk5pip3mbjbq6dj4iun7tqzkkh3nrtla'
    wallet_privete_key='7b2254797065223a22626c73222c22507269766174654b6579223a225039715136684d414c74695162623955754c48624371586a4d555161576346346774466c6c4759434b52553d227d'
    pytest.main()
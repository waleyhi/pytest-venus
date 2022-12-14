import os
import allure
import time
import pytest
import venus_market_function
import pexpect
#获取market-client程序运行目录
@pytest.fixture(scope='function',autouse=True)
def get_venus_market_client_run_path():
    #由于market-client属于工具，而且一般跟venus-market放一起，故默认将venus-market目录作为client目录
    venus_market_client_path=os.popen("ps -ef | grep venus-market|grep run| grep -v grep| awk '{print $2}'| xargs pwdx | awk '{print $NF}'").read().strip()
    return venus_market_client_path

@allure.epic("market-client测试")
@allure.feature("market-client actor-funds功能模块测试")
class TestMarketClientActorFunds:
    @allure.story("测试market-client actor-funds balances查看指定矿工市场余额是否正常")
    @pytest.mark.run(order=2)
    def test_market_client_actor_funds_balances(self,get_venus_market_client_run_path):
        test_miner = venus_market_function.venus_market_list_miner()[0]
        try:
            actor_balance = os.popen(f"{get_venus_market_client_run_path}/market-client actor-funds balances {test_miner}").read()
            print("测试矿工号：", test_miner)
            print("查询balance执行结果为：", actor_balance)
            if 'Escrowed Funds' in actor_balance:
                a = 1
            else:
                a = 0
                print("查询结果中未包含Escrowed Funds余额，查询测试异常")
        except Exception as e:
            print("查询balance执行报错，报错信息为：", e)
            a = 0
        assert a == 1, "actor-funds balances查看指定矿工市场余额测试失败"

    @allure.story("测试market-client actor-funds add增加指定矿工市场余额是否正常")
    @pytest.mark.run(order=3)
    def test_market_client_actor_funds_add(self,get_venus_market_client_run_path):
        test_miner = venus_market_function.venus_market_list_miner()[0]
        try:
            actor_add = os.popen(
                f"{get_venus_market_client_run_path}/market-client actor-funds add --address {test_miner} --from t3rugtczeric5kypbgnt7643omyxia6mkrevryrggrksqx73zfbqthgj7eumxbeap6hoctj45dc6k6ylyfm57a 100").read()
            print("测试矿工号：", test_miner)
            print("add执行结果为：", actor_add)
            if 'AddBalance message cid' in actor_add:
                a = 1
            else:
                a = 0
                print("add结果中未包含生成消息，add测试异常")
        except Exception as e:
            print("add执行报错，报错信息为：", e)
            a = 0
        assert a == 1, "actor-funds add查看指定矿工市场余额测试失败"


@allure.epic("market-client测试")
@allure.feature("market-client data功能模块测试")
class TestMarketClientData:
    def test_market_client_data_import(self,get_venus_market_client_run_path):
        # 创建测试文件
        os.popen("dd if=/dev/zero of=/tmp/autotest-import-file-test.txt bs=1M count=5")
        cmd_import = os.popen(f"{get_venus_market_client_run_path}/market-client data import /tmp/autotest-import-file-test.txt").read()
        # 获取输出结果中文件的cid
        file_cid = cmd_import.split()[-1]
        print("测试import文件为/tmp/autotest-import-file-test.txt")
        print("import文件结果为：", cmd_import)
        data_info = venus_market_function.market_client_data_local()
        if file_cid in ''.join(data_info):
            a = 1
        else:
            a = 0
        assert a == 1, "data import导入文件测试失败"

    def test_market_client_data_drop(self,get_venus_market_client_run_path):
        # 获取一条测试数据
        data_info01 = venus_market_function.market_client_data_local()[0]
        # 提取测试数据的import id并删除
        id_import = data_info01.split(':')[0]
        os.popen(f"{get_venus_market_client_run_path}/market-client data drop {id_import}")
        # 再次获取data信息
        data_info02 = venus_market_function.market_client_data_local()
        print("删除后data信息为：", data_info02)
        if id_import in ''.join(data_info02):
            a = 0
        else:
            a = 1
        assert a == 1, "data import导入文件测试失败"

    def test_market_client_data_stat(self,get_venus_market_client_run_path):
        # 获取一条测试数据
        data_info01 = venus_market_function.market_client_data_local()[0]
        # 提取测试数据中文件cid值
        file_cid = data_info01.split()[1]
        data_stat = os.popen(f"{get_venus_market_client_run_path}/market-client data stat {file_cid}").read()
        print("文件stat信息为：", data_stat)
        if 'Payload Size' in data_stat:
            a = 1
        else:
            a = 0
        assert a == 1, "data stat查看import文件信息测试失败"

@allure.epic("market-client测试")
@allure.feature("market-client data功能模块测试")
class Test_Market_Client_Storage:
    def test_market_client_storage_asks(self,get_venus_market_client_run_path):
        test_miner = venus_market_function.venus_market_list_miner()[0]
        miner_info = os.popen(f"{get_venus_market_client_run_path}/market-client storage asks query {test_miner}").read()
        print("查询矿工存储市场信息为：", miner_info)
        assert test_miner in miner_info, "storage asks query查看矿工存储市场信息测试失败"

    def test_market_client_storage_deals_list(self,get_venus_market_client_run_path):
        deals_list_info = os.popen(f"{get_venus_market_client_run_path}/market-client storage deals list").read()
        print("查询本地订单信息为：", deals_list_info)
        assert 'DealCid' in deals_list_info, "storage deals list查看订单信息测试失败"

    def test_market_client_storage_deals_stats(self,get_venus_market_client_run_path):
        deals_stats_info = os.popen(f"{get_venus_market_client_run_path}/market-client storage deals stats").read()
        print("查询本地订单状态为：", deals_stats_info)
        assert 'Total' in deals_stats_info, "storage deals stats查看订单状态测试失败"
    def test_market_client_storage_init(self,get_venus_market_client_run_path):
        #获取测试用的文件cid
        data_info = venus_market_function.market_client_data_local()[0]
        # 提取测试数据中文件cid值
        data_cid = data_info.split()[1]
        #获取测试矿工号
        test_miner=venus_market_function.venus_market_list_miner()[0]
        deal_init=pexpect.spawn(f"{get_venus_market_client_run_path}/market-client storage deals init",timeout=180)
        expect_list = ['Data CID.*',pexpect.EOF,pexpect.TIMEOUT,]
        index=deal_init.expect(expect_list)
        if index==0:
            print ("测试data cid为：",data_cid)
            deal_init.sendline(f"{data_cid}")
            expect_list = ['Deal duration.*',pexpect.EOF,pexpect.TIMEOUT,]
            index=deal_init.expect(expect_list)
            if index==0:
                print ("订单过期时间为200天")
                deal_init.sendline("200")
                expect_list = ['Miner Addresses.*',pexpect.EOF,pexpect.TIMEOUT,]
                index=deal_init.expect(expect_list)
                if index==0:
                    deal_init.sendline(f"{test_miner}")
                    print("测试矿工号为",test_miner)
                    expect_list = ['Accept.*', pexpect.EOF, pexpect.TIMEOUT, ]
                    index = deal_init.expect(expect_list)
                    if index==0:
                        deal_init.sendline("yes")
                        print("确认订单信息")
                        expect_list = ['*CID.*', pexpect.EOF, pexpect.TIMEOUT, ]
                        index = deal_init.expect(expect_list)
                        if index==0:
                            a=1
                        elif:
                            a=0
                    else:
                        print('1EOF or TIMEOUT')
                        a = 0
                else:
                    print('1EOF or TIMEOUT')
                    a = 0
            else:
                print('1EOF or TIMEOUT')
                a = 0
        else:
            print('1EOF or TIMEOUT')
            a = 0
        assert a==1,"deal init测试失败"

if __name__ == '__main__':
    pytest.main()

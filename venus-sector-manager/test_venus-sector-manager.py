import os
import allure
import time
import pytest
import uuid
import pexpect
import venus_sector_manager_function as vsm

@allure.epic("venus-sector-manager测试")
@allure.feature("venus-sector-manager主程序测试")
class Test_venus_sector_manager_status():
    @allure.story("测试venus-sector-manager程序是否能启动")
    @pytest.mark.run(order=1)
    def test_venus_sector_manager_start(self):
        a= venus_sector_manager_function.process_check('venus-sector-manager')
        assert a==1,"venus-sector-manager 进程不存在"
    @allure.story("测试venus-sector-manager程序是否能稳定运行3分钟不崩溃")
    @pytest.mark.run(order=1)
    def test_venus_sector_manager_alive(self):
        a= venus_sector_manager_function.process_alive('venus-sector-manager','run')
        b=time.time()
        c=b-a
        print ("venus-sector-manager 进程已稳定运行%f秒" % c)
        assert c > 180,"venus-sector-manager 运行时间不足3分钟"


@allure.epic("venus-sector-manager测试")
@allure.feature("venus-sector-manager 各功能模块测试")
class Test_venus_sector_manager_auth():
    @allure.story("测试venus-sector-manager util chain获取的高度是否正常")
    def test_venus_sector_manager_util_chain_head(self):
        try:
            chain_info = os.popen(f"{vsm.get_venus_sector_manager_run_path()}/venus-sector-manager util chain head").read()
            print("vsm查询高度信息为：", chain_info)
            if 'bafy' in chain_info:
                a=1
            else:
                a=0
        except Exception as e:
            print (f"vsm查询高度信息报错，报错信息为：{e}")
        assert a == 1, "vsm获取高度测试失败"
    @allure.story("测试venus-sector-manager util miner info查看矿工信息是否正常")
    def test_venus_sector_manager_util_miner_info(self):
        try:
            vsm_miner_info = os.popen(
                f"{vsm.get_venus_sector_manager_run_path()}/venus-sector-manager util chain info t01000").read()
            print("vsm查询矿工信息为：", vsm_miner_info)
            if 'f01000' in vsm_miner_info:
                a = 1
            else:
                a = 0
        except Exception as e:
            print(f"vsm查询矿工信息报错，报错信息为：{e}")
        assert a == 1, "vsm查询矿工测试失败"
    @allure.story("测试venus-sector-manager set-password设置密码是否正常")
    def test_wallet_set_password(self,get_venus_sector_manager_run_path):
        try:
            vsm_miner_create_info = os.popen(
                f"{vsm.get_venus_sector_manager_run_path()}/venus-sector-manager util miner create --from t3wknhyskfndkpusfyl5o2uh4724radjxesfortxigrewti3izvjhsoucf5y22wuvq6ag4h2a62nzp42rfnq6q --sector-size 8M").read()
            print("vsm创建矿工信息为：", vsm_miner_create_info)
            if 'miner actor' in vsm_miner_create_info:
                a = 1
            else:
                a = 0
        except Exception as e:
            print(f"vsm创建矿工报错，报错信息为：{e}")
        assert a == 1, "vsm创建矿工测试失败"

if __name__ == '__main__':
    pytest.main()
import psutil,pytest,os,re,time,datetime,allure
@allure.feature("检查venus-gateway进程是否存在")
def test_process_exist():
    for i in psutil.pids():
        if psutil.Process(i).name()=="venus-gateway":
            print ("venus-gateway进程正在运行,进程号为:%s" % i)
            a=1
            break
        else:
            a=0
    assert a==1,"venus-gateway 进程不存在"
@allure.feature("测试venus-gateway中是否已有miner地址")
def test_miner():
    miner_info=os.popen("/root/venus-gateway miner list").readlines()
    if len(miner_info)==0:
        a=0
        print("venus-gateway 中未发现任何矿工")
    else:
        print("venus-gateway中矿工信息如下:",miner_info)
if __name__ == '__main__':
    pytest.main()

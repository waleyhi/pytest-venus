import psutil,pytest,os,re,time,datetime,allure
os.system("rm -f /root/pytest/allure/*")
@allure.feature("检查venus进程是否存在")
def test_process_exist():
    for i in psutil.pids():
        if psutil.Process(i).name()=="venus":
            print ("venus进程正在运行,进程号为:%s" % i)
            a=1
            break
        else:
            a=0
    assert a==1,"venus 进程不存在"
@allure.feature("测试venus高度是否同步到最新")
def test_height():
    height=os.popen("/root/venus chain ls").readlines()[-1]
    height_time=re.split('\(|\)',height)[1]
    time1=datetime.datetime.strptime(height_time,'%Y-%m-%d %H:%M:%S')
    time2=time1.timestamp()
    time3=datetime.datetime.now()
    time4=time3.timestamp()
    assert time4-time2 < 60,"高度同步异常，venus已超过60秒没更新高度"
@allure.feature("venus state 各命令测试")
class Teststate():
    @allure.story("venus state power 命令测试")
    def test_state_power(self):
        power_info=os.popen("/root/venus state power t01000").readlines()[0]
        power=re.split('\(',power_info)[0]
        assert int(power)==2516582400,"venus state power命令异常"
    @allure.story("venus state sectors 命令测试")
    def test_state_sectors(self):
        sectors_info=os.popen("/root/venus state sectors t01000").readlines()[0]
        sectors=re.split(':',sectors_info)[0]
        assert int(sectors)==0,"venus state sectors 命令异常"
    @allure.story("venus state actor-cids 命令测试")
    def test_state_actor_cids(self):
        print("检查venus actor-cids是否符合预期")
        actor_cids=os.popen("/root/venus state actor-cids").readlines()
        for i in range(1,20):
            if actor_cids[i]=='storagepower      bafk2bzaceb45l6zhgc34n6clz7xnvd7ek55bhw46q25umuje34t6kroix6hh6  \n':
                a=1
                break
            else:
                a=0
        assert a==1,"venus actor版本不对，请检查actor-cids"
@allure.feature("venus chain 各命令测试")
class Testchain():
    @allure.story("venus高度导出car文件是否正常")
    def test_chain_export(self):
        print("测试venus节点是否能将高度导出为car文件")
        os.system("/root/venus chain export /tmp/test.car")
        car_path='/tmp/test.car'
        assert os.path.isfile(car_path),"导出链失败，请检查chain export命令"
@allure.feature("venus wallet 各命令测试")
class Testwallet():
    @allure.story("venus wallet ls命令是否正常")
    def test_wallet_ls(self):
        print("测试wallet命令是否正常")
        assert os.system("/root/venus wallet ls")==0,"wallet ls失败，请检查命令"

if __name__ == '__main__':
    pytest.main()

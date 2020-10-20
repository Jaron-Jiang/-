'''
线程为什么要挂起有以下原因：
1. 可以观察浏览器运行到你一个地方了
2. 保证frame等的切换，有可能你写了代码切换的，但因为没有挂起，导致运行错误(我不确定是不是这个原因，但这个问题我出现过，使用了线程挂起这个问题就解决了)
3. 等待视频的播放结束
4. 防止平台检查机制检查出来你是用的刷课程序（正是因为这个原因，因此我挂起的部分时间是随机数，因为停顿时间太规律，也可能被检测到）
5. 等待服务器响应和页面刷新，因为页面没有刷新，那么后面的查找标签就会找不到
'''

from selenium import webdriver
import time
import random

Number = ''   #登录的账号
Password = '' #登录的密码
Course = ''   #要刷的课程名

class Object:

    #构造函数   
    def __init__(self,url):
        self.driver = webdriver.Chrome()#模拟打开chrome浏览器
        self.driver.get(url)#在chrome浏览器中搜索url这个网址

    #登录函数
    def login(self):
        input = self.driver.find_element_by_id('phone')#定位输入账号的标签
        time.sleep(random.random())#线程挂起random.random()秒
        input.send_keys(Number)#在输入账号的标签中模拟输入账号
        input = self.driver.find_element_by_id('pwd')#定位输入密码的标签的句柄
        time.sleep(random.random())#线程挂起random.random()秒
        input.send_keys(Password)#在输入账号的标签中模拟输入密码
        input = self.driver.find_element_by_id('loginBtn')#定位登录的标签的句柄
        time.sleep(random.randint(1,3))#线程挂起random.randint(1,3)秒
        input.click()#模拟鼠标点击登录按钮
        time.sleep(random.randint(1,3))#线程挂起random.randint(1,3)秒
        try:
            self.driver.switch_to.frame(self.driver.find_element_by_id('frame_content'))#切换frame
        except:
            print('登录错误')
            return
        input = self.driver.find_elements_by_class_name('courseName')#定位class为courseName的所有标签的句柄
        flag = True #记录课程是否找到，如果找到，变量为False，反之为Ture
        for i in input:
            if i.text == Course:#如果该标签的文本是我们需要刷的课程，则将该标签的句柄赋给input，并退出遍历
                input = i
                flag = False
                break
        if flag:
            print('没有找到课程: %s' % Course)
            return
        else:
            input.click()#模拟鼠标点击该课程
            self.driver.switch_to.default_content()#返回原来的frame
            windows = self.driver.window_handles#由于打开一个课程会产生一个新的标签，因此获取全部标签的句柄
            self.driver.switch_to.window(windows[-1]) #切换到新产生的标签的句柄
            self.study()#调用study成员函数
        
    #寻找视频      
    def study(self):
        input = self.driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[2]/div[3]/div[1]/div[1]/h3/span[3]/a')#定位课程中的第一个课时
        input.click()#模拟点击该课时
        for i in range(10):#只放前十个课时
            time.sleep(random.randint(1,3))#线程挂起random.randint(1,3)秒
            try:
                self.driver.switch_to.frame(self.driver.find_element_by_id('iframe'))#切换frame
            except:
                print('第一个frame没找到')
                break
            try:
                inputs = self.driver.find_elements_by_css_selector("[class='ans-attach-online ans-insertvideo-online']") #切换frame
            except:
                print('第二个frame没找到')
                break
            try:
                for input in inputs:#对找到的frame进行遍历，并对其中的视频进行播放
                    time.sleep(3)#线程挂起3秒
                    self.play_video(input)#播放当前frame中的视频
                    self.driver.switch_to.parent_frame()#切换frame
                self.driver.switch_to.default_content()#返回最外层的文档
                input = self.driver.find_element_by_xpath('//*[@id="mainid"]/div[1]/div[2]')#寻找下一页这个按钮的标签
                time.sleep(3)#线程挂起3秒
                input.click()#点击下一页这个按钮
            except:
                print('下一页点击失败')
                break

    #播放视频的函数        
    def play_video(self,input):
        try:
            self.driver.switch_to.frame(input)#切换frame
        except:
            print('切换frame句柄失败')
            return
        try:
            inputs = self.driver.find_element_by_id('reader')#寻找当前frame中的视频
        except:
            print('未找到视频')
            return
        inputs.click()#模拟点击该视频，即播放该视频
        time.sleep(2)#线程挂起2秒
        try:
            t = 0#记录视频的时长单位为秒
            while t == 0:
                inputs = self.driver.find_element_by_xpath('//*[@id="video"]/div[5]/div[4]/span[2]')#寻找视频中的时长标签
                inputs = inputs.text#将时长这个字符串返回
                count = 0#记录返回时长的字符串中的‘：’数
                for i in inputs:
                    if i == ':':
                        count = count + 1
                h = '0'#小时
                m = '0'#分
                s = '0'#秒
                #对于不同的时长即是否有小时这个单位进行不同方式的分割
                if count == 1:
                    m , s = inputs.strip().split(':')
                elif count == 2:
                    h , m , s = inputs.strip().split(':')
                t = int(int(h)*3600+int(m)*60+int(s))#计算时长
            print('当前视频 %d 秒' % t)#打印本视频的时长
            time.sleep(t)#线程挂起t秒，因为视频一共有t秒的时长
        except:
            print('播放时长没找到')
            return

    #析构函数
    def __del__(self):
        self.driver.quit() #关闭chromedriver进程   
        
if __name__ == "__main__":
    a = Object('http://i.chaoxing.com')#创建Object对象
    a.login()#运行本刷课程序
    del a#释放对象（不使用这一句，析构函数会出错，原因网上没有说，比较玄学）
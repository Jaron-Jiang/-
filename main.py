from selenium import webdriver
import time
import random

Number = '' #登录的账号
Password = '' #登录的密码
Course = '' #要刷的课程名

class Object:
    def __init__(self,url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
    def login(self):
        input = self.driver.find_element_by_id('phone')#定位输入账号的标签
        time.sleep(random.random())
        input.send_keys(Number)
        input = self.driver.find_element_by_id('pwd')#定位输入密码的标签的句柄
        time.sleep(random.random())
        input.send_keys(Password)
        input = self.driver.find_element_by_id('loginBtn')#定位登录的标签的句柄
        time.sleep(random.randint(1,3))
        input.click()
        time.sleep(random.randint(1,3))
        try:
            self.driver.switch_to.frame(self.driver.find_element_by_id('frame_content'))#切换frame
        except:
            print('登录错误')
        input = self.driver.find_elements_by_class_name('courseName')#定位class为courseName的所有标签的句柄
        flag = True
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
            self.study()
        
            
    def study(self):
        input = self.driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[2]/div[3]/div[1]/div[1]/h3/span[3]/a')
        input.click()
        for i in range(10):
            time.sleep(random.randint(1,3))
            try:
                self.driver.switch_to.frame(self.driver.find_element_by_id('iframe'))
            except:
                print('第一个frame没找到')
                break
            try:
                inputs = self.driver.find_elements_by_css_selector("[class='ans-attach-online ans-insertvideo-online']") 
            except:
                print('第二个frame没找到')
                break
            try:
                for input in inputs:
                    time.sleep(3)
                    self.play_video(input)
                    self.driver.switch_to.parent_frame()
                self.driver.switch_to.default_content()
                input = self.driver.find_element_by_xpath('//*[@id="mainid"]/div[1]/div[2]')
                time.sleep(3)
                input.click()
            except:
                print('下一页点击失败')
                break
                
    def play_video(self,input):
        try:
            self.driver.switch_to.frame(input)
        except:
            print('切换frame句柄失败')
            return
        try:
            inputs = self.driver.find_element_by_id('reader')
        except:
            print('未找到视频')
            return
        inputs.click()
        time.sleep(2)
        try:
            t = 0
            while t == 0:
                inputs = self.driver.find_element_by_xpath('//*[@id="video"]/div[5]/div[4]/span[2]')
                inputs = inputs.text
                count = 0
                for i in inputs:
                    if i == ':':
                        count = count + 1
                h = '0'
                m = '0'
                s = '0'
                if count == 1:
                    m , s = inputs.strip().split(':')
                elif count == 2:
                    h , m , s = inputs.strip().split(':')
                t = int(int(h)*3600+int(m)*60+int(s))
            print('当前视频 %d 秒' % t)
            time.sleep(t)
        except:
            print('播放时长没找到')
            return
    def __del__(self):
        self.driver.quit()    
        
if __name__ == "__main__":
    a = Object('http://i.chaoxing.com')
    a.login()
    del a
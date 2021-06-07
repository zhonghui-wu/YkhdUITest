# encoding: utf-8
import traceback  # 用来打印报错信息
from selenium import webdriver
from time import sleep
from PIL import Image, ImageEnhance
import pytesseract, unittest, time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from config import imgFile, adminHost, teacherHost, studentHost, adminLoginName, adminPassWord
from config import teacherLoginName, teacherPassWord, studentLoginName, studentPassWord
import os, phone
from BeautifulReport import BeautifulReport


class NhyktTest(unittest.TestCase):
    global timelast, courseName, liveCourse, date

    @classmethod
    def setUpClass(cls):
        global date
        date = time.strftime('%Y%m%d')
        isExists = os.path.exists(f'./photo/{date}')
        if not isExists:
            os.mkdir(f'./photo/{date}')
        else:
            pass
        try:
            cls.chrome_options = Options()
            cls.chrome_options.add_argument('--no-sandbox')
            cls.chrome_options.add_argument('--disable-dev-shm-usage')
            cls.chrome_options.add_argument('--headless')
            cls.chrome_options.add_argument('--disable-gpu')
            cls.chrome_options.add_argument('--force-device-scale-factor=1')
            cls.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=cls.chrome_options)
            # cls.driver = webdriver.Chrome(chrome_options=cls.chrome_options)
            cls.driver.get(adminHost)
            cls.driver.set_window_size(1920, 1080)
            cls.driver.implicitly_wait(5)
            ele =cls.driver.find_element_by_css_selector('[class="loginChange"]')
            if ele:
                cls.driver.save_screenshot(f'./photo/{date}/setUpSucceed.png')
        except:
            print('初始化失败')
            cls.driver.save_screenshot(f'./photo/{date}/setUpFail.png')
            traceback.print_exc()  # 打印报错信息
            assert False

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        print("-----------测试结束！结果发送中。。。-----------")

    def GetCode(self, file):  # 获取图片验证码
        global code
        try:
            # 浏览器页面截屏
            self.driver.get_screenshot_as_file(file)

            # 定位验证码位置及大小
            location = self.driver.find_element_by_id('s-canvas').location

            size = self.driver.find_element_by_id('s-canvas').size

            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']

            # 从文件读取截图，截取验证码位置再次保存
            img = Image.open(file).crop((left, top, right, bottom))

            img = img.convert('L')  # 转换模式：L | RGB

            img = ImageEnhance.Contrast(img)  # 增强对比度

            img = img.enhance(2.0)  # 增加饱和度

            img.save(file)

            # 再次读取识别验证码
            img = Image.open(file)

            code = pytesseract.image_to_string(img).replace(' ', '')
        except:
            traceback.print_exc()
            print('获取图片验证码失败')
        return code.strip()

    def save_img(self, img_name):
        self.driver.save_screenshot(f'./img/{img_name}.png')

    @BeautifulReport.add_test_img('NhyktTest_test001AdminLogin')
    def test001AdminLogin(self):  # admin登录
        '''admin登录'''
        try:
            sleep(1)
            self.driver.find_element_by_css_selector('[class="loginChange"]').click()
            self.driver.find_elements_by_css_selector('span > input')[0].send_keys(adminLoginName)
            self.driver.find_elements_by_css_selector('span > input')[1].send_keys(adminPassWord)
            code = self.GetCode(imgFile)
            # 输入验证码
            self.driver.find_elements_by_css_selector('span > input')[2].send_keys(code)
            self.driver.find_element_by_css_selector('span > button').click()

            while True:
                # 判断是否有这个元素
                try:
                    warn = self.driver.find_element_by_css_selector('[class="ant-form-explain"]')
                except:
                    break
                else:
                    if warn:
                        self.driver.find_element_by_id('s-canvas').click()
                        code = self.GetCode(imgFile)
                        inp = self.driver.find_elements_by_css_selector('span > input')[2]
                        # 清除输入框内容
                        inp.send_keys(Keys.CONTROL + 'a')
                        inp.send_keys(Keys.DELETE)
                        # 输入验证码
                        inp.send_keys(code)
                        self.driver.find_element_by_css_selector('span > button').click()

                    else:
                        break

            title = self.driver.find_element_by_css_selector('[title="admin"]')
            self.assertTrue(title)
            if title:
                print('admin登录成功')
                self.driver.save_screenshot(f'./photo/{date}/test001AdminLoginSucceed.png')
            else:
                print('admin登录失败')

        except:
            print('admin登录失败')
            self.save_img('NhyktTest_test001AdminLogin')
            traceback.print_exc()
            assert False
        return

    @BeautifulReport.add_test_img('NhyktTest_test002AddCourse')
    def test002AddCourse(self):  # 新增学科
        '''admin新增学科删除学科'''

        try:
            self.driver.find_element_by_xpath('//*[@id="menu"]/li[5]/div').click()
            self.driver.find_element_by_xpath('//*[@id="menu"]/li[5]/ul/li[1]').click()
            self.driver.find_element_by_css_selector('[class=" ant-tabs-tab"]').click()
            sleep(1)
            # 将屏幕滚动到最下面
            self.driver.execute_script("var q=document.documentElement.scrollTop=10000")
            # 点击输入页数，进入最后一页
            self.driver.find_elements_by_xpath('//*[@class="ant-pagination-options-quick-jumper"]/input')[1].send_keys(
                '100000\n')
            sleep(1)
            n = 0
            all = self.driver.find_elements_by_xpath('//*[@class="subjectManagement"]/div//table/tbody/tr')
            self.assertTrue(all)
            for i in all:
                n += 1
                if "rock测试" in i.text:
                    # 下面是删除学科
                    delete = i.find_elements_by_xpath('//*[@class="subjectManagement"]/div//table/tbody/tr/td/a[2]')
                    delete[n - 1].click()
                    sleep(1)
                    self.driver.find_elements_by_css_selector('[class="ant-btn ant-btn-primary"]')[3].click()
                    break
                else:
                    pass

            # 增加学科
            sleep(1)
            self.driver.find_element_by_css_selector('div.subjectManagement > button').click()
            self.driver.find_element_by_css_selector('span > input').send_keys('rock测试')
            sleep(1)
            self.driver.find_element_by_xpath('//*[@class="ant-modal-footer"]/div/button[2]').click()
            sleep(1)
            self.driver.find_elements_by_xpath('//*[@class="ant-pagination-options-quick-jumper"]/input')[1].send_keys(
                '100000\n')
            x = 0
            sleep(1)
            all1 = self.driver.find_elements_by_xpath('//*[@class="subjectManagement"]/div//table/tbody/tr')
            self.assertTrue(all1)
            for name in all1:
                x += 1
                if "rock测试" in name.text:
                    print('学科添加成功，学科新增功能测试正常！')
                    self.driver.save_screenshot(f'./photo/{date}/test002AddCourseSucceed.png')
                    # 下面是删除学科
                    deletes = name.find_elements_by_xpath('//*[@class="subjectManagement"]/div//table/tbody/tr/td/a[2]')
                    deletes[x - 1].click()
                    sleep(1)
                    self.driver.find_elements_by_css_selector('[class="ant-btn ant-btn-primary"]')[3].click()
                    break
        except:
            print('新增学科失败')
            self.save_img('NhyktTest_test002AddCourse')
            traceback.print_exc()
            assert False
        return

    @BeautifulReport.add_test_img('NhyktTest_test003AddSchool')
    def test003AddSchool(self):  # 新增学校
        '''admin新增学校和删除学校'''
        try:
            sleep(1)
            self.driver.find_element_by_css_selector('[class=" ant-tabs-tab"]').click()
            x = 0
            sleep(1)
            schools = self.driver.find_elements_by_css_selector('[class="ant-table-row ant-table-row-level-0"]')
            self.assertTrue(schools)
            for school in schools:
                x += 1
                if 'rock测试学校' in school.text:
                    # 下面是删除学校
                    deles = school.find_elements_by_css_selector('[class="option-danger-color"]')
                    deles[x - 1].click()
                    sleep(1)
                    self.driver.find_elements_by_css_selector('[class="ant-btn ant-btn-primary"]')[3].click()
                    sleep(1)
                    break
            sleep(1)
            self.driver.find_elements_by_css_selector('[class="ant-btn ant-btn-primary"]')[0].click()
            # 新增信息信息填写
            schoolForm = self.driver.find_elements_by_css_selector('[class="ant-input"]')
            # 学校名称
            sleep(1)
            schoolForm[0].send_keys('rock测试学校')
            # 学校简称
            schoolForm[1].send_keys('测试')
            # 学校标识码
            schoolForm[2].send_keys('1')
            # 学校类型
            self.driver.find_elements_by_css_selector('[class="select_option ant-select ant-select-enabled"]')[
                0].click()
            # 这里选的是第一个类型
            self.driver.find_elements_by_css_selector('[class="ant-select-dropdown-menu-item"]')[0].click()
            self.driver.find_element_by_xpath('//*[@class="ant-modal-footer"]/div/button[2]').click()
            # 获取第一页的学校列表
            sleep(2)
            n = 0
            Allschool = self.driver.find_elements_by_css_selector('[class="ant-table-row ant-table-row-level-0"]')
            self.assertTrue(Allschool)
            for aschool in Allschool:
                n += 1
                if 'rock测试学校' in aschool.text:
                    print('学校新增功能测试正常')
                    self.driver.save_screenshot(f'./photo/{date}/test003AddSchoolSucceed.png')
                    # 下面是删除学校
                    dele = aschool.find_elements_by_css_selector('[class="option-danger-color"]')
                    dele[n-1].click()
                    sleep(1)
                    self.driver.find_elements_by_css_selector('[class="ant-btn ant-btn-primary"]')[3].click()
                    break
        except:
            print('新增学校失败')
            self.save_img('NhyktTest_test003AddSchool')
            traceback.print_exc()
            assert False
        return

    @BeautifulReport.add_test_img('NhyktTest_test004AddTeacher')
    def test004AddTeacher(self):  # 新增老师
        '''admin新增老师'''
        global newTeacherPhone
        try:
            self.driver.find_element_by_xpath('//*[@id="menu"]/li[4]/div').click()
            self.driver.find_element_by_xpath('//*[@id="menu"]/li[4]/ul/li[1]').click()
            # 点击新增老师按钮
            self.driver.find_element_by_xpath('//*[@class="option_group"]/button[1]').click()
            # 老师信息表单
            sleep(1)
            teacherFrom = self.driver.find_elements_by_css_selector('[class="ant-input"]')
            # 老师姓名
            teacherFrom[0].send_keys('rock测试')
            # 老师手机号
            teacherFrom[1].send_keys('131' + str(phone.Phone))
            # 老师教龄
            teacherFrom[5].send_keys('1')
            # 选择老师生日
            self.driver.find_element_by_css_selector('[class="ant-calendar-picker-input ant-input"]').click()
            self.driver.find_elements_by_css_selector('[class="ant-calendar-date"]')[0].click()
            # 将屏幕滚动到最下面
            self.driver.execute_script("var q=document.documentElement.scrollTop=10000")
            # 选择所属学校
            self.driver.find_elements_by_css_selector('[class="ant-select-selection__placeholder"]')[1].click()
            self.driver.find_elements_by_css_selector('[class="ant-select-dropdown-menu-item"]')[0].click()
            # 选择学科
            self.driver.find_elements_by_css_selector('[class="ant-select-selection__placeholder"]')[2].click()
            self.driver.find_element_by_css_selector('li.ant-select-dropdown-menu-item.ant-select-dropdown-menu-item-active').click()
            # 选择教学年级
            self.driver.find_element_by_css_selector('[class="ant-tag"]').click()
            sleep(1)
            self.driver.find_elements_by_css_selector('[class="input-radio"]')[0].click()
            self.driver.find_element_by_css_selector('[class="ant-btn ant-btn-primary"]').click()
            # 提交
            self.driver.find_element_by_css_selector('[class="addbtn ant-btn ant-btn-primary"]').click()
            while True:
                ele = self.driver.find_elements_by_css_selector('[class="title_bar"]')
                teacherFrom = self.driver.find_elements_by_css_selector('[class="ant-input"]')
                self.assertTrue(teacherFrom)
                if ele:
                    # 滑到顶部
                    self.driver.execute_script("var q=document.documentElement.scrollTop=0")
                    phone.Phone += 1
                    # 清除输入框内容
                    teacherFrom[1].send_keys(Keys.CONTROL + 'a')
                    teacherFrom[1].send_keys(Keys.DELETE)
                    # 重新输入
                    newTeacherPhone = '131' + str(phone.Phone)
                    teacherFrom[1].send_keys(newTeacherPhone)
                    # 将屏幕滚动到最下面
                    self.driver.execute_script("var q=document.documentElement.scrollTop=10000")
                    try:
                        # 提交
                        sleep(1)
                        self.driver.find_element_by_css_selector('[class="addbtn ant-btn ant-btn-primary"]').click()
                    except:
                        pass

                else:
                    break
            # 获取老师列表
            sleep(1)
            teacherListPhone = self.driver.find_elements_by_xpath('//*[@class="ant-table-tbody"]/tr/td[4]')
            self.assertTrue(teacherListPhone)
            for i in teacherListPhone:
                if newTeacherPhone == i.text:
                    print('新增老师功能测试正常')
                    self.driver.save_screenshot(f'./photo/{date}/test004AddTeacherSucceed.png')
                    break
        except:
            print('新增老师失败')
            self.save_img('NhyktTest_test004AddTeacher')
            traceback.print_exc()
            assert False
        return

    @BeautifulReport.add_test_img('NhyktTest_test005AddStudent')
    def test005AddStudent(self):  # 新增学生
        '''admin新增学生'''
        global newStudentPhone
        try:
            self.driver.find_element_by_xpath('//*[@id="menu"]/li[4]/ul/li[2]').click()
            sleep(1)
            self.driver.find_element_by_xpath('//*[@class="option_group"]/button[1]').click()
            # 填写学生基本信息
            sleep(1)
            studentFrom = self.driver.find_elements_by_css_selector('[class="ant-input"]')
            # 输入学生姓名
            studentFrom[0].send_keys('rock测试')
            # 输入学生家长手机号
            studentFrom[1].send_keys('132' + str(phone.Phone))
            # 选择生日
            self.driver.find_element_by_css_selector('[class="ant-calendar-picker-input ant-input"]').click()
            self.driver.find_elements_by_css_selector('[class="ant-calendar-date"]')[0].click()
            # 选择学校
            sleep(1)
            self.driver.find_elements_by_css_selector('[class="ant-select-selection__placeholder"]')[0].click()
            self.driver.find_elements_by_css_selector('[class="ant-select-dropdown-menu-item"]')[0].click()
            # 选择年级
            self.driver.find_elements_by_css_selector('[class="ant-select-selection__placeholder"]')[1].click()
            self.driver.find_element_by_css_selector('li.ant-select-dropdown-menu-item.ant-select-dropdown-menu-item-active').click()
            # 点击提交
            self.driver.find_element_by_css_selector('[class="addbtn ant-btn ant-btn-primary"]').click()
            while True:
                ele = self.driver.find_elements_by_css_selector('[class="title_bar"]')
                if ele:
                    phone.Phone += 1
                    try:
                        # 清除输入框内容
                        studentFrom[1].send_keys(Keys.CONTROL + 'a')
                        studentFrom[1].send_keys(Keys.DELETE)
                        # 重新输入
                        newStudentPhone = '132' + str(phone.Phone)
                        studentFrom[1].send_keys(newStudentPhone)
                    # 提交
                        self.driver.find_element_by_css_selector('[class="addbtn ant-btn ant-btn-primary"]').click()
                    except:
                        pass

                else:
                    break
            # 将phone的值保存
            file = open('phone.py', 'w')
            file.write(f'Phone={phone.Phone}')
            file.close()
            # 获取学生列表
            sleep(1)
            studentListPhone = self.driver.find_elements_by_xpath('//*[@class="ant-table-tbody"]/tr/td[4]')
            self.assertTrue(studentListPhone)
            for i in studentListPhone:
                if newStudentPhone == i.text:
                    print('新增学生成功')
                    print('新增学生功能测试正常')
                    self.driver.save_screenshot(f'./photo/{date}/test005AddStudentSucceed.png')
                    break
        except:
            print('新增学生失败')
            self.save_img('NhyktTest_test005AddStudent')
            traceback.print_exc()
            assert False

        return

    @BeautifulReport.add_test_img('NhyktTest_test006AddTourClass')
    def test006AddTourClass(self): # 新增巡课
        '''admin新增巡课'''
        global timelast
        try:
            self.driver.find_element_by_xpath('//*[@id="menu"]/li[4]/ul/li[3]').click()
            sleep(1)
            self.driver.find_element_by_xpath('//*[@class="option_group"]/button[1]').click()
            # 填写巡课信息
            timelast = int(time.time()*10000) % 10000 # 获取时间戳最后几位
            auditName = 'rock巡课' + str(timelast)
            sleep(1)
            self.driver.find_elements_by_css_selector('[class="ant-input"]')[0].send_keys(auditName)
            # 生日
            self.driver.find_element_by_css_selector('[class="ant-calendar-picker-input ant-input"]').click()
            self.driver.find_elements_by_css_selector('[class="ant-calendar-date"]')[0].click()
            # 所属学校
            self.driver.find_elements_by_css_selector('[class="ant-select-selection__placeholder"]')[0].click()
            self.driver.find_elements_by_css_selector('[class="ant-select-dropdown-menu-item"]')[0].click()
            # 提交
            self.driver.find_element_by_css_selector('[class="addbtn ant-btn ant-btn-primary"]').click()
            # 获取巡课列表
            auditList = self.driver.find_elements_by_xpath('//*[@class="ant-table-tbody"]/tr/td[3]')
            self.assertTrue(auditList)
            for i in auditList:
                if auditName == i.text:
                    print('新增巡课功能测试正常')
                    self.driver.save_screenshot(f'./photo/{date}/test006AddTourClassSucceed.png')
                    break
                else:
                    print('新增巡课失败')
        except:
            print('新增巡课失败')
            self.save_img('NhyktTest_test006AddTourClass')
            traceback.print_exc()
            assert False
        return

    @BeautifulReport.add_test_img('NhyktTest_test007AddLiveCourse')
    def test007AddLiveCourse(self):
        '''admin添加直播课'''
        global courseName
        try:
            self.driver.find_element_by_xpath('//*[@id="menu"]/li[2]/div').click()
            self.driver.find_element_by_xpath('//*[@id="menu"]/li[2]/ul/li[3]').click()
            sleep(1)
            self.driver.find_elements_by_css_selector('[class="ant-btn ant-btn-primary"]')[1].click()
            # 输入课程名称
            timelast = int(time.time() * 10000) % 10000
            courseName = 'rock课程' + str(timelast)
            sleep(1)
            self.driver.find_element_by_css_selector('[class="ant-input"]').send_keys(courseName)
            # 点击上传封面
            self.driver.find_element_by_xpath('//*[@class="ant-upload"]/input').send_keys(imgFile)
            sleep(1)
            self.driver.find_element_by_css_selector('[class="ant-btn ant-btn-primary"]').click()
            # 选择学科
            sleep(1)
            self.driver.find_element_by_css_selector('[class="ant-select-selection__rendered"]').click()
            self.driver.find_element_by_css_selector(
                '[class="ant-select-dropdown-menu-item ant-select-dropdown-menu-item-active"]').click()
            # 选择上课年级
            self.driver.find_element_by_css_selector('[class="ant-tag"]').click()
            sleep(1)
            self.driver.find_elements_by_css_selector('[class="input-radio"]')[6].click()
            self.driver.find_elements_by_css_selector('[class="ant-btn ant-btn-primary"]')[1].click()
            # 输入课程简介
            self.driver.switch_to.frame('ueditor_1')
            self.driver.find_elements_by_css_selector('[class="view"]')[1].send_keys('测试课程简介')
            # 回到之前的iframe
            self.driver.switch_to.default_content()
            # 点击提交
            sleep(1)
            self.driver.find_element_by_css_selector('[class="addbtn ant-btn ant-btn-primary"]').click()
            # 获取温馨提示弹窗
            sleep(1)
            warning = self.driver.find_element_by_css_selector('[class="ant-modal-confirm-content"]')
            self.assertTrue(warning)
            print('课程新增成功')
            print('课程管理测试成功')
            # 点击以后再说
            self.driver.find_elements_by_css_selector('[class="ant-btn"]')[1].click()
            self.driver.find_element_by_xpath('//*[@id="menu"]/li[2]/ul/li[3]').click()
            self.driver.save_screenshot(f'./photo/{date}/test007AddLiveCourseSucceed.png')
            # 选择去查看
            sleep(1)
            self.driver.find_element_by_css_selector(' tr:nth-child(1) > td:nth-child(9) > a:nth-child(1)').click()
            # 滑到页面最下面点击去排课
            self.driver.execute_script("var q=document.documentElement.scrollTop=10000")
            sleep(1)
            self.driver.find_element_by_css_selector('[class="ant-btn ant-btn-primary"]').click()
        except:
            print('新增课程失败')
            self.save_img('NhyktTest_test007AddLiveCourse')
            assert False
        return courseName

    @BeautifulReport.add_test_img('NhyktTest_test008CreateLive')
    def test008CreateLive(self):
        '''admin排课'''
        global liveCourse
        try:
            # 进入快速排课,输入上课老师
            self.driver.find_element_by_css_selector('[class="ant-select ant-select-enabled ant-select-no-arrow"]').click()
            self.driver.find_elements_by_css_selector('[class="ant-select-search__field"]')[1].send_keys('rock')
            sleep(1)
            self.driver.find_element_by_css_selector('[class="title"]').click()

            # 选择开课日期为今天
            sleep(1)
            self.driver.find_element_by_css_selector('[class="ant-calendar-picker"]').click()
            sleep(1)
            self.driver.find_element_by_css_selector('[class="ant-calendar-today-btn "]').click()
            # 选择开课时间
            nowTime = time.strftime('%H%M')
            sleep(1)
            self.driver.find_elements_by_css_selector('[class="ant-time-picker-input"]')[0].click()
            sleep(1)
            allHour = self.driver.find_elements_by_xpath('//*[@class="ant-time-picker-panel-select"][1]/ul/li')
            allMinute = self.driver.find_elements_by_xpath('//*[@class="ant-time-picker-panel-select"][2]/ul/li')
            browserHour = \
            self.driver.find_elements_by_css_selector('[class="ant-time-picker-panel-select-option-selected"]')[0]
            browserMinute = \
            self.driver.find_elements_by_css_selector('[class="ant-time-picker-panel-select-option-selected"]')[1]
            nowMinute = nowTime[2] + nowTime[3]
            nowHour = nowTime[0] + nowTime[1]
            # 开始时间
            if int(nowMinute) >= 58:
                subscript1 = int(browserHour.text) + 1  # 下标
                allHour[subscript1].click()
            else:
                subscript2 = int(browserMinute.text) + 4
                allMinute[subscript2].click()
            # 选择结束时间
            self.driver.find_elements_by_css_selector('[class="ant-time-picker-input"]')[1].click()
            etime = str(int(nowHour) + 2) + ':' + str(nowMinute)
            sleep(1)
            self.driver.find_element_by_css_selector('[class="ant-time-picker-panel-input "]').send_keys(etime)
            self.driver.find_element_by_css_selector('[class="title"]').click()
            # 输入直播名称
            self.driver.find_elements_by_css_selector('[class="ant-input"]')[0].send_keys('rock测试直播')
            self.driver.execute_script("var q=document.documentElement.scrollTop=10000")
            # 点击提交
            self.driver.find_element_by_css_selector('[class="addForm ant-btn ant-btn-primary"]').click()
            sleep(1)
            liveCourse = self.driver.find_elements_by_xpath('//*[@class="ant-table-row ant-table-row-level-0"]/td[7]')
            self.assertTrue(liveCourse)
            for i in liveCourse:
                if courseName == i.text:
                    print('排课管理测试成功')
                    self.driver.save_screenshot(f'./photo/{date}/test008CreateLiveSucceed.png')
                    break
                else:
                    print('排课失败')
        except:
            print('排课失败')
            self.save_img('NhyktTest_test008CreateLive')
            traceback.print_exc()
            assert False
        return liveCourse

    @BeautifulReport.add_test_img('NhyktTest_test009TeacherLogin')
    def test009TeacherLogin(self):
        '''老师登录'''
        try:
            self.driver.execute_script(f"window.open('{teacherHost}')")
            allHandles = self.driver.window_handles
            self.driver.switch_to.window(allHandles[-1])
            self.driver.find_element_by_css_selector('[class="loginChange"]').click()
            sleep(1)
            self.driver.find_elements_by_css_selector('span > input')[0].send_keys(teacherLoginName)
            self.driver.find_elements_by_css_selector('span > input')[1].send_keys(teacherPassWord)
            code = self.GetCode(imgFile)
            # 输入验证码
            self.driver.find_elements_by_css_selector('span > input')[2].send_keys(code)
            self.driver.find_element_by_css_selector('span > button').click()

            while True:
                # 判断是否有这个元素
                try:
                    warn = self.driver.find_element_by_css_selector('[class="ant-form-explain"]')
                except:
                    break
                if warn:
                    self.driver.find_element_by_id('s-canvas').click()
                    code = self.GetCode(imgFile)
                    inp = self.driver.find_elements_by_css_selector('span > input')[2]
                    # 清除输入框内容
                    inp.send_keys(Keys.CONTROL + 'a')
                    inp.send_keys(Keys.DELETE)
                    # 输入验证码
                    inp.send_keys(code)
                    self.driver.find_element_by_css_selector('span > button').click()

                else:
                    break
            sleep(2)
            ele = self.driver.find_element_by_css_selector('[class="addLiveBtn"]')
            self.assertTrue(ele)
            if ele:
                print('老师登录成功')
                self.driver.save_screenshot(f'./photo/{date}/test009TeacherLoginSucceed.png')
            else:
                print('未登录')
        except:
            print('老师登录失败')
            self.save_img('NhyktTest_test009TeacherLogin')
            traceback.print_exc()
            assert False
        return

    @BeautifulReport.add_test_img('NhyktTest_test010TeacherLive')
    def test010TeacherLive(self):
        '''老师上课'''
        try:
            # 点击进入直播
            n = 0
            allCourse = self.driver.find_elements_by_xpath('//*[@class="ant-table-row ant-table-row-level-0"]/td[5]')
            self.assertTrue(allCourse)
            for i in allCourse:
                n += 1
                if courseName == i.text:
                    ele = self.driver.find_elements_by_xpath('//*[@class="ant-table-row ant-table-row-level-0"]')[n - 1]
                    ele.find_element_by_link_text('进入直播').click()
                    break

            # 获取所有句柄
            sleep(1)
            allHandles = self.driver.window_handles
            # 切换到最后一个句柄
            self.driver.switch_to.window(allHandles[-1])
            # 点击 三次下一步
            self.driver.find_elements_by_css_selector('[class="tic-btn ing"]')[0].click()
            self.driver.find_elements_by_css_selector('[class="tic-btn ing"]')[1].click()
            self.driver.find_elements_by_css_selector('[class="tic-btn ing"]')[1].click()
            # 点击 进入课堂
            self.driver.find_elements_by_css_selector('[class="tic-btn ing"]')[1].click()
            # 点击 上课
            self.driver.find_elements_by_css_selector('[class="tic-btn headerbtn start"]')[0].click()
            # 判断是否上课
            sleep(2)
            ele = self.driver.find_element_by_css_selector('[class="tic-btn headerbtn end red"]')
            if '下课' == ele.text:
                print(courseName + '上课成功')
                print('老师直播测试成功')
                self.driver.save_screenshot(f'./photo/{date}/test010TeacherLiveSucceed.png')
        except:
            print('老师直播失败')
            self.save_img('NhyktTest_test010TeacherLive')
            traceback.print_exc()
            assert False
        return

    @BeautifulReport.add_test_img('NhyktTest_test011StudentLogin')
    def test011StudentLogin(self):
        '''学生登录'''
        try:
            self.driver.execute_script(f"window.open('{studentHost}')")
            allHandles = self.driver.window_handles
            self.driver.switch_to.window(allHandles[-1])
            self.driver.find_element_by_css_selector('[class="blue_color"]').click()
            sleep(1)
            self.driver.find_elements_by_css_selector('span > input')[0].send_keys(studentLoginName)
            self.driver.find_elements_by_css_selector('span > input')[1].send_keys(studentPassWord)
            code = self.GetCode(imgFile)
            # 输入验证码
            self.driver.find_elements_by_css_selector('span > input')[2].send_keys(code)
            self.driver.find_element_by_css_selector('span > button').click()

            while True:
                # 判断是否有这个元素
                try:
                    warn = self.driver.find_element_by_css_selector('[class="ant-form-explain"]')
                except:
                    break
                else:
                    if warn:
                        self.driver.find_element_by_id('s-canvas').click()
                        code = self.GetCode(imgFile)
                        inp = self.driver.find_elements_by_css_selector('span > input')[2]
                        # 清除输入框内容
                        inp.send_keys(Keys.CONTROL + 'a')
                        inp.send_keys(Keys.DELETE)
                        # 输入验证码
                        inp.send_keys(code)
                        self.driver.find_element_by_css_selector('span > button').click()

                    else:
                        break

            studentName = self.driver.find_element_by_css_selector('[class="username"]')
            if studentName:
                print('学生登录成功')
                sleep(1)
                self.driver.save_screenshot(f'./photo/{date}/test011StudentLoginSucceed.png')
        except:
            print('学生登录失败')
            self.save_img('NhyktTest_test011StudentLogin')
            traceback.print_exc()
            assert False
        return

    @BeautifulReport.add_test_img('NhyktTest_test012StudentIntoLive')
    def test012StudentIntoLive(self):
        '''学生进入直播间上课'''
        try:
            # 关闭广告
            self.driver.find_element_by_css_selector('[class="ant-modal-close-x"]').click()
            # 点击进入直播
            self.driver.find_element_by_xpath('//*[@class="option_item online"]/span').click()
            sleep(2)
            allHandles = self.driver.window_handles
            self.driver.switch_to.window(allHandles[-1])
            sleep(2)
            ele = self.driver.find_element_by_css_selector('[class="left-time menu-course__time"]')
            if '已开课' in ele.text:
                print('学生进入直播间成功')
                print('学生进入直播间测试正常')
                self.driver.save_screenshot(f'./photo/{date}/test012StudentIntoLiveSucceed.png')
        except:
            print('学生进入直播间失败')
            self.save_img('NhyktTest_test012StudentIntoLive')
            traceback.print_exc()
            assert False
        return

    @BeautifulReport.add_test_img('NhyktTest_test013Clear')
    def test013Clear(self):
        '''老师下课，删除排课信息，删除新增的课程'''
        try:
            # 获取所有的浏览器句柄
            allHandles = self.driver.window_handles
            self.driver.switch_to.window(allHandles[2])
            # 老师关闭直播
            self.driver.find_element_by_css_selector('[class="tic-btn headerbtn end red"]').click()
            self.driver.find_element_by_css_selector('[class="ivu-btn ivu-btn-primary ivu-btn-large"]').click()
            # admin删除创建的直播课
            self.driver.switch_to.window(allHandles[0])
            self.driver.execute_script("var q=document.documentElement.scrollTop=10000")
            s = 0
            self.driver.find_element_by_xpath('//*[@id="menu"]/li[2]/ul/li[3]').click()
            allCourse = self.driver.find_elements_by_xpath('//*[@class="ant-table-row ant-table-row-level-0"]/td[3]')
            self.assertTrue(allCourse)
            for j in allCourse:
                s += 1
                if courseName == j.text:
                    ele1 = self.driver.find_elements_by_xpath('//*[@class="ant-table-row ant-table-row-level-0"]')[s - 1]
                    ele1.find_element_by_link_text('删除').click()
                    sleep(1)
                    self.driver.find_element_by_xpath('//*[@class="ant-modal-confirm-btns"]/button[2]').click()
                    sleep(1)
                    allCourse1 = self.driver.find_elements_by_xpath(
                        '//*[@class="ant-table-row ant-table-row-level-0"]/td[3]')
                    for course in allCourse1:
                        if courseName == course.text:
                            print('删除课程不成功')
                        else:
                            print('删除课程成功')
                            break
                break

            # admin删除排课
            sleep(1)
            n = 0
            self.driver.find_element_by_xpath('//*[@id="menu"]/li[2]/ul/li[1]').click()
            AllLiveCourse = self.driver.find_elements_by_xpath('//*[@class="ant-table-row ant-table-row-level-0"]/td[7]')
            self.assertTrue(AllLiveCourse)
            for i in AllLiveCourse:
                n += 1
                if courseName == i.text:
                    ele = self.driver.find_elements_by_xpath('//*[@class="ant-table-row ant-table-row-level-0"]')[n - 1]
                    ele.find_element_by_link_text('删除').click()
                    sleep(1)
                    self.driver.find_element_by_xpath('//*[@class="ant-modal-confirm-btns"]/button[2]').click()
                    sleep(1)
                    AllLiveCourse1 = self.driver.find_elements_by_xpath(
                        '//*[@class="ant-table-row ant-table-row-level-0"]/td[7]')
                    for LiveCourse in AllLiveCourse1:
                        if courseName == LiveCourse.text:
                            print('删除排课不成功')
                        else:
                            print('删除排课成功')
                            break
                break
        except:
            traceback.print_exc()
            self.save_img('NhyktTest_test013Clear')
            assert False
        return


if __name__ == '__main__':
    unittest.main()
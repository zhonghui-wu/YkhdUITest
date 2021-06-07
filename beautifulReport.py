import unittest, os
from BeautifulReport import BeautifulReport
from BeautifulReport.BeautifulReport import HTML_IMG_TEMPLATE


def testBeautifulReport(testCase, reportTitle, testMsg):  # 无法发送到邮件
    """
    :param testCase: 测试用例名称
    :param reportTitle:  测试报告标题
    :param testMsg:  测试用例说明
    :param report_dir:  测试报告存放位置
    """
    #                                         这个点的意思是测试脚本的路径为当前路径
    suite_tests = unittest.defaultTestLoader.discover(".", pattern=testCase, top_level_dir=None)
    BeautifulReport(suite_tests).report(filename=reportTitle, description=testMsg, report_dir=".")

    return


def force_attach_image(img_nm):
    """
    这是一个让用例运行正常测试报告中也能附上截图的函数
    :param img_nm:
    :return:
    """
    img_path = os.path.abspath('{}'.format(BeautifulReport.img_path))
    data = BeautifulReport.img2base(img_path, img_nm + '.png')
    print(HTML_IMG_TEMPLATE.format(data, data))


if __name__ == '__main__':
    # 生成测试报告
    testBeautifulReport("nhykt.py", "report", "南海云课堂管理后台回归流程测试")
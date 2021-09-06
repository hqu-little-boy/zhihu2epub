from selenium import webdriver
import os
import time
import json


def browser_initial():
    """"
    进行浏览器初始化
    """
    os.chdir('./')
    browser = webdriver.Chrome()
    log_url = 'https://www.zhihu.com'
    return log_url, browser


def get_cookies(log_url, browser):
    """
    获取cookies保存至本地
    """
    browser.get(log_url)
    input("enter:")
    # time.sleep(25)  # 进行扫码
    # dictCookies = browser.get_cookies()  # 获取list的cookies
    # jsonCookies = json.dumps(dictCookies)  # 转换成字符串保存
    # browser.close()
    #
    # with open('cookies.txt', 'w') as f:
    #     f.write(jsonCookies)
    # print('cookies保存成功！')
    cookies = browser.get_cookies()
    jsonCookies = json.dumps(cookies)
    with open('cookies.json', 'w') as f:
        f.write(jsonCookies)
    browser.close()
    print('cookies保存成功！')


if __name__ == "__main__":
    tur = browser_initial()
    get_cookies(tur[0], tur[1])

# from selenium import webdriver
# import os
# import time
# import json
#
#
# def browser_initial():
#     """"
#     进行浏览器初始化
#     """
#     os.chdir('./')
#     browser = webdriver.Chrome()
#     log_url = 'https://www.zhihu.com/signin?next=%2F'
#     return log_url, browser
#
#
# def get_cookies(log_url, browser):
#     """
#     获取cookies保存至本地
#     """
#     browser.get(log_url)
#     # time.sleep(25)  # 进行扫码
#     input("enter:")
#     dictCookies = browser.get_cookies()  # 获取list的cookies
#     jsonCookies = json.dumps(dictCookies)  # 转换成字符串保存
#     browser.close()
#
#     with open('cookies.txt', 'w') as f:
#         f.write(jsonCookies)
#     print('cookies保存成功！')
#
#
# if __name__ == "__main__":
#     tur = browser_initial()
#     get_cookies(tur[0], tur[1])

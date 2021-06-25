import logging

import requests
from bs4 import BeautifulSoup
import requests,pymysql


def assert_util(self,response,status_code,status,desc):
    self.assertEqual(status_code,response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(desc, response.json().get("description"))
def requests_third_api(form_data):
    # # 解析form表单中的内容，并提取第三方请求的数据
    # soup = BeautifulSoup(form_data, "html.parser")
    # third_url = soup.form['action']
    # logging.info("third requests url = {}".format(third_url))
    # data = {}
    # for input in soup.find_all('input'):
    #     data.setdefault(input['name'], input['value'])
    # logging.info("third requests data = {}".format(data))
    # # 发送第三方请求
    # response = requests.post(third_url, data=data)
    # return response
    # 解析form表单中的内容，并提取第三方请求的参数
    soup = BeautifulSoup(form_data, "html.parser")
    third_url = soup.form['action']
    logging.info("third request url = {}".format(third_url))
    data = {}
    for input in soup.find_all('input'):
        data.setdefault(input['name'], input['value'])
    logging.info("third request data = {}".format(data))
    # 发送第三方请求
    response = requests.post(third_url, data=data)
    return response
class DButils:
    def get_conn(self):
        conn=pymysql.connect()
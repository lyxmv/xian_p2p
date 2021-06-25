import logging
import random
import unittest

import requests

from api.loginApi import loginApi
from api.tenderApi import tenderAPI
from api.trustAPI import trustAPI
from api.approveApi import approveApi
from utils import assert_util, requests_third_api


class test_process(unittest.TestCase):
    phone = '13033447845'
    imgcode = '8888'
    pwd='123456'
    amount='10000'


    def setUp(self) -> None:
        self.login_api=loginApi()
        self.tender_api=tenderAPI()
        self.trust_api=trustAPI()
        self.approve_api=approveApi()
        self.session=requests.Session()
    def tearDown(self) -> None:
        self.session.close()


    def test01_get_img_code(self):
        r=random.random()
        response=self.login_api.getImgCode(self.session,str(r))
        self.assertEqual(200,response.status_code)
    def test02_get_sms_code(self):
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 请求短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone, self.imgcode)
        logging.info("sms verify response={}".format(response.json()))
        assert_util(self, response, 200, 200, "短信发送成功")
    def test03_reg_success(self):
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 请求短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone, self.imgcode)
        logging.info("sms verify response={}".format(response.json()))
        assert_util(self, response, 200, 200, "短信发送成功")
        response=self.login_api.register(self.session,self.phone,self.pwd)
        logging.info("reg response={}".format(response.json()))
        assert_util(self,response,200,200,"注册成功")
    def test04_login_success(self):
        response=self.login_api.login(self.session,self.phone,self.pwd)
        logging.info("loggin response={}".format(response.json()))
        assert_util(self,response,200,200,"登录成功")
        response=self.trust_api.trust_register(self.session)
        self.assertEqual(200,response.status_code)
        self.assertEqual(200,response.json().get("status"))
        form_data=response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
        response=requests_third_api(form_data)
        logging.info("third-interface response={}".format(response.text))
        self.assertEqual('UserRegister OK', response.text)
    def test05_input(self):
        r=random.random()
        response=self.trust_api.get_recharge_verify_code(self.session,str(r))
        self.assertEqual(200,response.status_code)
        amount = '1000'
        logging.info("input response={}".format(response.text))
        response = self.trust_api.recharge(self.session, amount)
        logging.info("recharge response={}".format(response.text))
        # 断言获取的开户信息是否正确
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # response=self.trust_api.recharge(self.session,self.amount)
        # logging.info("recharge response={}".format(response.text))
        # self.assertEqual(200,response.status_code)
        # self.assertEqual(200,response.json().get("status"))
        # form_data=response.json().get("description").get("form")
        # logging.info("form response={}".format(form_data))
        # response=requests_third_api(form_data)
        # logging.info("third-interface response={}".format(response.text))
        # # 断言第三方接口请求处理是否成功
        # self.assertEqual('NetSave OK', response.text)










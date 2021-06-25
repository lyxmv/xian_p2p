import logging
import random
from time import sleep

import requests
import unittest

from api.loginApi import loginApi
from utils import assert_util


class login(unittest.TestCase):
    phone1='15975365258'
    imgCode='8888'
    pwd='test123456'
    smsCode='666666'
    phone2='15978945612'
    phone3 = '15978945012'
    phone4 = '15278943012'
    def setUp(self) -> None:
        self.login_api = loginApi()
        self.session=requests.Session()
    def tearDown(self) -> None:
        self.session.close()
    #获取图片验证码
    def test01_get_img_code_random_float(self):
        #定义参数(随机小数)
        r = random.random()
        #调用接口类中的接口
        response=self.login_api.getImgCode(self.session ,str(r))
        #接受接口的返回结果，进行断言
        self.assertEqual(200,response.status_code)

    def test02_get_img_code_random_int(self):
        # 定义参数(随机整数)
        r = random.randint(9999,999999)
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接受接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
    def test03_get_img_code_random_empty(self):
        #定义参数（参数为空）
        #调用接口类中的接口
        response=self.login_api.getImgCode(self.session,"")
        #接受接口的返回结果，进行断言
        self.assertEqual(404,response.status_code)
    def test04_get_img_code_string(self):
        #定义参数（随机字符串）
        r=random.sample("abcgusfkc",5)#前面为从这些字母中取值，数字为取出的长度
        rand=''.join(r)
        logging.info(rand)
        #调用接口类中的接口
        response=self.login_api.getImgCode(self.session,rand)
        #接受接口的返回结果，进行断言
        self.assertEqual(400,response.status_code)
    #获取短信验证码
    def test05_get_sms__code_success(self):
        #获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接受接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        #获取短信验证码
        #定义参数（正确的手机号以及验证码）

        #调用接口类中的接口
        response=self.login_api.getSmsCode(self.session,self.phone1,self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        #接受接口的返回结果，并进行断言
        assert_util(self,response,200,200,"短信发送成功")
    def test06_get_sms_code_wrong_img_code(self):
        r=random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        #2.获取短信验证码
        #定义参数（手机号正确，图片验证码错误）
        error_code='8889'
        #调用接口类中的发送短信验证码的接口
        response=self.login_api.getSmsCode(self.session,self.phone1,error_code)
        #对收到的响应结果进行断言
        assert_util(self,response,200,100,"图片验证码错误")
    def test07_get_sms_code_img_null(self):
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        #2.获取短信验证码
        #定义参数（手机号正确，图片验证码为空）

        #调用接口类中的发送短信验证码的接口
        response=self.login_api.getSmsCode(self.session,self.phone1,"")
        assert_util(self,response,200,100,"图片验证码错误")
    def test08_get_sms_phonenum_null(self):
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        #2.获取短信验证码
        #定义参数（手机号为空）
        #调用接口类中的发送短信验证码接口
        response=self.login_api.getSmsCode(self.session,'',self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        #断言
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))
    def test09_register_success_must_param(self):
        #1.成功获取图片验证码
        # 获取图片验证码
        # 定义参数(随机小数)
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接受接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        #2.成功获取短信验证码
        # 获取短信验证码
        # 定义参数（正确的手机号以及验证码）

        # 调用接口类中的接口
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        assert_util(self, response, 200, 200, "短信发送成功")
        #3.成功注册-输入必填项
        response=self.login_api.register(self.session,self.phone1,self.pwd)
        logging.info("register response = {}".format(response.json()))
        #断言
        assert_util(self,response,200,200,"注册成功")
    def test10_register_all_param(self):
        #1.获取图片验证码成功
        r=random.random()
        response=self.login_api.getImgCode(self.session,str(r))
        self.assertEqual(200,response.status_code)
        #2.获取短信验证码
        response=self.login_api.getSmsCode(self.session,self.phone2,self.imgCode)
        assert_util(self,response,200,200,"短信发送成功")
        #3.输入全部参数，注册成功
        response=self.login_api.register(self.session,self.phone2,self.pwd , invite_phone='13012345678')
        assert_util(self,response,200,200,"注册成功")
    def test11_register_imgcode_wrong(self):
        # 1.获取图片验证码成功
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone2, self.imgCode)
        assert_util(self, response, 200, 200, "短信发送成功")
        # 3.图片验证码错误，注册失败
        response = self.login_api.register(self.session, self.phone2, self.pwd,imgCode='1234')
        assert_util(self, response, 200, 100, "验证码错误!")
    def test12_register_smscode_wrong(self):
        # 1.获取图片验证码成功
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone3, self.imgCode)
        assert_util(self, response, 200, 200, "短信发送成功")
        # 3.短信验证码错误。注册失败
        response = self.login_api.register(self.session, self.phone3, self.pwd, phoneCode='1234')
        assert_util(self, response, 200, 100, "验证码错误")
    def test13_register_phonenum_exist(self):
        # 1.获取图片验证码成功
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone1, self.imgCode)
        assert_util(self, response, 200, 200, "短信发送成功")
        # 3.手机已存在。注册失败
        response = self.login_api.register(self.session, self.phone1, self.pwd)
        logging.info("register response = {}".format(response.json()))
        assert_util(self, response, 200, 100, "手机已存在!")
    def test14_register_pwd_null_bug(self):
        # 1.获取图片验证码成功
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone4, self.imgCode)
        assert_util(self, response, 200, 200, "短信发送成功")
        # 3.密码为空，注册失败
        response = self.login_api.register(self.session, self.phone4, '')
        logging.info("register response = {}".format(response.json()))
        assert_util(self, response, 200, 100, "密码不能为空")
    def test15_register_disagree_bug(self):
        # 1.获取图片验证码成功
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 2.获取短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone4, self.imgCode)
        assert_util(self, response, 200, 200, "短信发送成功")
        # 3.密码为空，注册失败
        response = self.login_api.register(self.session, self.phone4,self.pwd,dyServer='off')
        logging.info("register response = {}".format(response.json()))
        assert_util(self, response, 200, 100, "请同意我们的条款")
    def test16_login_success(self):
        response=self.login_api.login(self.session)
        logging.info("register response = {}".format(response.json()))
        assert_util(self,response,200,200,"登录成功")
    def test17_login_fail_not_exist(self):
        response=self.login_api.login(self.session,'18681892281')
        logging.info("register response = {}".format(response.json()))
        assert_util(self,response,200,100,"用户不存在")
    def test18_login_pwd_null(self):
        response = self.login_api.login(self.session, pwd='')
        logging.info("register response = {}".format(response.json()))
        assert_util(self, response, 200, 100, "密码不能为空")
    def test19_login_fail_pwd_null(self):
        response = self.login_api.login(self.session, pwd='159')
        logging.info("register response = {}".format(response.json()))
        assert_util(self, response, 200, 100, "密码错误1次,达到3次将锁定账户")
        response = self.login_api.login(self.session, pwd='159')
        logging.info("register response = {}".format(response.json()))
        assert_util(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")
        response = self.login_api.login(self.session, pwd='159')
        logging.info("register response = {}".format(response.json()))
        assert_util(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        response = self.login_api.login(self.session)
        logging.info("register response = {}".format(response.json()))
        assert_util(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        sleep(60)
        response = self.login_api.login(self.session)
        logging.info("login response = {}".format(response.json()))
        #对结果进行断言
        assert_util(self,response,200,200,"登录成功")
    def test20_check_login_ok(self):
        response = self.login_api.login(self.session)
        logging.info("register response = {}".format(response.json()))
        assert_util(self, response, 200, 200, "登录成功")
        response=self.login_api.check_login(self.session)
        assert_util(self, response, 200, 200, "OK")













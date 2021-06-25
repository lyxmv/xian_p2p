import logging
import  unittest
import requests

from api.approveApi import approveApi
from api.loginApi import loginApi
from utils import assert_util


class approve(unittest.TestCase):
    phone2='15978945612'
    realname='张三'
    cardId='110117199003070995'
    cardId1='123'
    def setUp(self) -> None:
        self.login_api=loginApi()
        self.approve_api=approveApi()
        self.session=requests.Session()
    def tearDown(self) -> None:
        pass
    #认证成功
    def test01_approve_success(self):
        #1.用户登录
        response = self.login_api.login(self.session)
        logging.info('login response = {}'.format(response.json()))
        assert_util(self,response,200,200,"登录成功")
        #2.发送认证请求
        #准备参数
        #调用接口脚本中定义的方法发送请求
        response=self.approve_api.approve(self.session,self.realname,self.cardId)
        logging.info('login response = {}'.format(response.json()))
        #对结果进行断言。
        assert_util(self,response,200,200,"提交成功!")
    def test02_approve_name_null_bug(self):
        # 1.用户登录
        response = self.login_api.login(self.session,self.phone2)
        logging.info('login response = {}'.format(response.json()))
        assert_util(self, response, 200, 200, "登录成功")
        # 2.发送认证请求
        # 准备参数
        # 调用接口脚本中定义的方法发送请求
        response = self.approve_api.approve(self.session,"",self.cardId)
        logging.info('login response = {}'.format(response.json()))
        # 对结果进行断言。
        assert_util(self, response, 200, 100, "姓名不能为空")

    def test03_approve_id_null_bug(self):
        # 1.用户登录
        response = self.login_api.login(self.session, self.phone2)
        logging.info('login response = {}'.format(response.json()))
        assert_util(self, response, 200, 200, "登录成功")
        # 2.发送认证请求
        # 准备参数
        # 调用接口脚本中定义的方法发送请求
        response = self.approve_api.approve(self.session, self.realname,'')
        logging.info('login response = {}'.format(response.json()))
        # 对结果进行断言。
        assert_util(self, response, 200, 100, "身份证号不能为空")

    def test04_approve_success(self):
        # 1.用户登录
        response = self.login_api.login(self.session,self.phone2)
        logging.info('login response = {}'.format(response.json()))
        assert_util(self, response, 200, 200, "登录成功")
        # 2.发送认证请求
        # 准备参数
        # 调用接口脚本中定义的方法发送请求
        response = self.approve_api.approve(self.session, self.realname, self.cardId1)
        logging.info('login response = {}'.format(response.json()))
        # 对结果进行断言。
        assert_util(self, response, 200, 100, "身份证号格式不正确")
    def test05_check_approve(self):
        # 1.用户登录
        response = self.login_api.login(self.session)
        logging.info('login response = {}'.format(response.json()))
        assert_util(self, response, 200, 200, "登录成功")
        response=self.approve_api.get_approve(self.session)
        logging.info('login response = {}'.format(response.json()))
        self.assertEqual(200,response.status_code)
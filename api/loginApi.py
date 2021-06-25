import app
import requests
class loginApi():
    def __init__(self):
        self.getImgCode_url = app.BASE_URL + '/common/public/verifycode1/'
        self.getSmsCode_url=app.BASE_URL+'/member/public/sendSms'
        self.register_url=app.BASE_URL+'/member/public/reg'
        self.login_url=app.BASE_URL+'/member/public/login'
        self.check_login_url=app.BASE_URL+'/member/public/islogin'

    def getImgCode(self,session,r):
      url=self.getImgCode_url+r
      response=session.get(url)
      return response
    def getSmsCode(self,session,phone,imgcode):
        #准备参数
        data={'phone':phone,'imgVerifyCode': imgcode, 'type':'reg'}
        #发送请求
        response=session.post(self.getSmsCode_url,data=data)
        return response

    def register(self,session,phone,pwd,imgCode='8888',phoneCode='666666',dyServer='on',invite_phone=''):
         data = {"phone": phone,
                 "password": pwd,
                 "verifycode": imgCode,
                 "phone_code": phoneCode,
                 "dy_server": dyServer,
                 'invite_phone': invite_phone}
         response=session.post(self.register_url,data=data)
         return response
    # def login(self,session,phone='13033447711',pwd='test123'):
    #     data = {"keywords": phone,"password": pwd}
    #     response = session.post(self.login_url,data=data)
    #     return response
    def login(self,session,phone='13033447711',pwd='test123'):
        data = {"keywords": phone,"password": pwd}
        response=session.post(self.login_url,data =data)
        return response
    # def check_login(self,session):
    #     response=session.post(self.check_login_url)
    #     return response


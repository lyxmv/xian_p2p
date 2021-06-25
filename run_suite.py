import unittest
import app
import time

from lib.HTMLTestRunner_PY3 import HTMLTestRunner
from script.login import login
from script.tender import tender

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(login))
suite.addTest(unittest.makeSuite(tender))

report_file=app.BASE_DIR+"/report/report{}.html".format(time.strftime("%Y%m%d-%H%M%S"))
with open(report_file,'wb') as f:
    runner=HTMLTestRunner(f,title="p2p金融项目接口测试报告",description="test")
    runner.run(suite)
# -*- coding: utf-8 -*-

# Author : 'hxc'

# Time: 2022/9/7 12:15 AM

# File_name: 'testTvAlterServer.py'

"""
Describe: this is a demo!
"""


import time
import unittest
import requests
import json

class TestTvAlterServer(unittest.TestCase):

    def testFLModelService(self):
        """
        测试 自动对接tv 警报服务
        :return:
        """
        t = time.time()
        url = "http://123.58.196.52:80/tvAlerServer"
        input ={
  "exchange":"okx",
  "symbol":"SUSHI-USDT-SWAP",
  "comment":"tp_long",
  "price":"{{strategy.order.price}}",
  "qty":"10",
  "batch_qty":"5",
  "api_key":"5c9e6f70-6fbe-445c-a1b0-1d16c1d52e91",
  "secretKey":"EF9BD664BE0A2CBC3154FED9F209B61D",
  "passphrase":"Huang1018@",
  "diaccess_token":"",
  "keyword":""
}
        headers = {
            'Content-Type': 'application/json'
        }
        data = json.dumps(input)
        print(type(data))

        res = requests.post(url, data, headers=headers)
        print(res)
        print(json.dumps(res.json(), indent=4, ensure_ascii=False))
        print(time.time() - t)

if __name__ == '__main__':
    unittest.main()

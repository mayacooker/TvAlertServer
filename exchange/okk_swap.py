# -*- coding: utf-8 -*-

# Author : 'hxc'

# Time: 2022/10/15 11:09 AM

# File_name: 'okk_swap.py'

"""
Describe: this is a demo!
"""
import logging
from exchange.okx import Trade_api as Trade
from exchange.okx import Account_api as Account


class OkkSwap(object):

    def __init__(self, api_key, secret_key, passphrase):
        self.tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag="0")
        self.accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag="0")
        self.uid = self.get_uid()

    def get_uid(self):
        """获取用户的uid"""
        uid = '-1'
        try:
            r = self.accountAPI.get_account_config()
            uid = r['data'][0]['uid']
        except Exception as e:
            print("获取uid失败")
            print(e)

        return uid

    def set_order(self,symbol, qty,side, ordType="market",posSide=None, px=None):
        """设置订单"""

        try:
            self.tradeAPI.place_order(instId=symbol,
                                          tdMode="cross",
                                          side=side,
                                          posSide=posSide,
                                          ordType=ordType,
                                          px = px,
                                          sz=qty)


        except Exception as e:
            print("下多单失败")
            print(e)

    def set_pingall_order(self, symbol, posSide=None):
        """市场价全平"""
        try:
            self.tradeAPI.close_positions(instId=symbol,
                                              mgnMode="cross",
                                              posSide=posSide,
                                              ccy='')

        except Exception as e:
            print("市价全平失败", symbol)
            print(e)



    def updatePosition(self,symbol):
        """获取该币种单向持仓的仓位"""
        positionAmt = 0

        try:
            result = self.accountAPI.get_positions('SWAP',symbol)
            positionAmt = result['data'][0]['pos']

        except Exception as e:
            print("okx，获取{}币种的仓位失败！！！".format(symbol))
            print(e)

        return positionAmt


    def do_market(self,signal,symbol,qty):
        """市场价进行交易"""
        # if self.request_uid_verify(uid=self.uid):

        try:
            position = self.updatePosition(symbol=symbol)

            if signal == "long" and float(position)<=0:
                # 平空单
                if float(position) != 0:
                    self.set_pingall_order(symbol=symbol)

                self.set_order(symbol=symbol, qty=str(qty), side="buy")
            elif signal == "short" and float(position)>=0:
                # 平多单
                if float(position) != 0:
                    self.set_pingall_order(symbol=symbol)
                self.set_order(symbol=symbol, qty=str(qty), side="sell")

            elif signal == "tp_long_batch" and float(position)>0:

                #平多一份订单
                self.set_order(symbol=symbol, qty=str(qty), side="sell")

            elif signal == "tp_short_batch" and float(position)<0:
                #平空一份订单
                self.set_order(symbol=symbol, qty=str(qty), side="buy")

            elif signal == "tp_long":
                self.set_pingall_order(symbol=symbol)

            elif signal == "tp_short":
                self.set_pingall_order(symbol=symbol)

        except Exception as e:
            logging.error(msg='okk api出问题' + str(e))



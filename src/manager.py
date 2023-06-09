# -*- coding: utf-8 -*-

# Author : 'hxc'

# Time: 2022/9/6 10:31 PM

# File_name: 'parsingStrategy.py'

"""
Describe: this is a demo!
"""


from configs.config import longComment,shortComment,tpLongComment,tpShortComment
from src.autoTraderBot import AutoTraderBotGroup


class StratgyManger(object):
    """策略管理器"""

    def __init__(self):

        # 下单方向
        self.longComment = longComment
        self.shortComment = shortComment
        # 出局方向
        self.tpLongComment = tpLongComment
        self.tpShortComment = tpShortComment

    def __parsingSide(self,order_status_ago,action ):
        """解析方向"""
        signal = "无"
        if order_status_ago == 'flat' and action in self.longComment:
            signal = "long"
        elif order_status_ago == 'flat' and action in self.shortComment:
            signal = "short"
        elif order_status_ago == 'long' and action in self.shortComment:
            signal = "tp_long"
        elif order_status_ago == 'short' and action in self.longComment:
            signal = "tp_short"

        return signal

    def __parsingSide_comment(self, comment):
        """解析方向"""
        signal = "无"
        if comment in self.longComment:
            signal = "long"
        elif comment in self.shortComment:
            signal = "short"
        elif comment in self.tpLongComment:
            signal = "tp_long"
        elif comment in self.tpShortComment:
            signal = "tp_short"
        elif "tp_long_" in comment:
            #平一份多单
            signal = "tp_long_batch"

        elif "tp_short_" in comment:
            # 平一份空单
            signal =  "tp_short_batch"

        return signal

    def parsingMsg(self,req_data):
        """进行解析tv给的消息"""
        result = {"msg": "SUCESS"}
        #解析信息
        strategyName = req_data.strategyName
        exchange = req_data.exchange
        symbol = req_data.symbol
        order_status_ago = req_data.order_status_ago
        action = req_data.action
        price = req_data.price
        loss_price = req_data.loss_price
        win_price = req_data.win_price
        lever = req_data.lever
        qty = req_data.qty
        batch_qty = req_data.batch_qty
        api_key = req_data.api_key
        secretKey = req_data.secretKey
        passphrase = req_data.passphrase
        diaccess_token = req_data.diaccess_token
        keyword = req_data.keyword
        comment = req_data.comment
        # signal = self.__parsingSide(order_status_ago,action)
        signal = self.__parsingSide_comment(comment=comment)

        if "batch" in signal:
            qty = batch_qty

        #初始化一个自动交易机器人组
        autoTraderBot = AutoTraderBotGroup(exchange=exchange,api_key=api_key,secretKey=secretKey,
                                           passphrase=passphrase,diaccess_token=diaccess_token,keyword=keyword)
        autoTraderBot.onTick(symbol=symbol,price=price,signal=signal,qty=qty,strategyName=strategyName)
        return result



















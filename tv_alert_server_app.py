# -*- coding: utf-8 -*-

# Author : 'hxc'

# Time: 2022/5/31 4:40 PM

# File_name: 'start_run.py'

"""
Describe: this is a demo!
"""
import logging.config
from os import path
from fastapi import FastAPI
from pydantic import BaseModel
from src.manager import StratgyManger




class InputDataItem(BaseModel):
    """输入数据对象"""
    exchange:str = ""  #binance/okex/huobi/bitget/bkex
    symbol:str = ""
    orderType:str = "" #limit/market
    price:str = ""
    loss_price: str = ""  # 止损价格
    win_price: str = ""  # 止盈价格
    lever:str = ""
    qty:str = ""
    batch_qty :str = "" #分批止盈止损的时候用的qty
    api_key:str = ""
    secretKey: str = ""  # 密钥
    passphrase= ""
    strategyName:str = "" #策略名称
    diaccess_token:str = ""
    keyword:str=""
    action:str=""
    order_status_ago:str=""
    comment :str = ""


# 导入日志配置文件
log_file_path = path.join(path.dirname(path.abspath(__file__)), "configs/logging.conf")
logging.config.fileConfig(log_file_path)
# 创建日志对象
logger = logging.getLogger()
loggerInfo = logging.getLogger("TimeInfoLogger")
Consolelogger = logging.getLogger("ConsoleLogger")
app = FastAPI()
sm = StratgyManger()

@app.post("/tvAlerServer")
async def tv_service(res_item:InputDataItem):
    """haha"""
    try:
        logging.info("进来" )
        res= sm.parsingMsg(req_data=res_item)
    except Exception as e:
        logging.error("app 服务报错，报错信息："+str(e))

        res = {"msg":"报错"}

    return res






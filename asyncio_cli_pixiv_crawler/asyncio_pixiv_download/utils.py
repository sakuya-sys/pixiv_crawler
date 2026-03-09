import requests
import sys
import os
from asyncio_pixiv_download import config
from datetime import datetime, timedelta
import logging
import re

def if_file_exist(path):#检查文件是否存在
    with os.scandir(path) as item:
        return any(item)
def if_ready():#检查代理是否开启
    url="https://www.pixiv.net/"
    try:
        with requests.get(url=url,proxies={"http": "http://127.0.0.1:7890","https": "http://127.0.0.1:7890"},headers=config.header,cookies=config.cookies) as res:
            if res.status_code!=200:
                logging.error(f"请求失败 状态码:{res.status_code} 代理未开启")
                sys.exit(0)
            else:
                logging.info("代理已开启")
                return True
    except requests.exceptions.RequestException as e:
        logging.error(f"代理未开启 请求异常: {e} ")
        sys.exit(0)


def check_date(date):#检查日期是否正确
    try:
        datetime.strptime(date, '%Y%m%d')
    except ValueError:
        logging.error("日期错误 日期格式必须为YYYYMMDD")
        logging.error(f"请检查你的日期是否正确:{date}")
        sys.exit(0)

def check_p(p):#检查图片页码是否正确
    if int(p)<=0 or int(p) >10:
        logging.error("图片数量错误 图片数量不能小于等于0也不能大于10")
        logging.error(f"请检查你的图片数量是否正确:{p}")
        sys.exit(0)



def  return_yesterday():#返回昨天的日期
    today=datetime.now().date()
    yesterday=today-timedelta(days=1)
    date=yesterday.strftime("%Y%m%d")
    return date

def nextillustturl(url,i):
    url=re.sub(pattern=r'p\d+\.',repl=f"p{i}.",string=url)
    return url

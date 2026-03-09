from asyncio_pixiv_download import config
from asyncio_pixiv_download import utils
from asyncio_pixiv_download import download
from pathlib import Path
import sys
import argparse
from datetime import datetime
import logging
import asyncio

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("aiofiles").setLevel(logging.WARNING)


async def down(ids,downloader,path):
    tasks=[]
    for id in ids:
        tasks.append(asyncio.create_task(downloader.getillustdata(id)))
    results=await asyncio.gather(*tasks)
    taskdonwloads=[]
    for illust in results:
        if illust.type==0:
            pathillust=path+f"/{illust.id}_0.jpg"
            taskdonwloads.append(asyncio.create_task(downloader.downloadillust(illust.originalurl,pathillust,illust)))
        elif illust.type==1:
            pathportfolio=path+f"/{illust.id}_作品集"
            Path(pathportfolio).mkdir(parents=True, exist_ok=True)
            taskdonwloads.append(asyncio.create_task(downloader.downloadportfolio(illust.originalurl,pathportfolio,illust)))
    await asyncio.gather(*taskdonwloads)
    await asyncio.sleep(0.1)

async def down1(ids,downloader,path):
    tasks=[]
    for id in ids:
        tasks.append(asyncio.create_task(downloader.getillustdata(id)))
    results=await asyncio.gather(*tasks)
    taskdonwloads=[]
    for illust in results:
        if int(illust.bookmarkCount)>=200:
            if illust.type==0:
                pathillust=path+f"/{illust.id}_{illust.count}.jpg"
                taskdonwloads.append(asyncio.create_task(downloader.downloadillust(illust.originalurl,pathillust,illust)))
            elif illust.type==1:
                pathportfolio=path+f"{illust.id}_作品集"
                taskdonwloads.append(asyncio.create_task(downloader.downloadportfolio(illust.originalurl,pathportfolio,illust)))
        else:
            continue
    await asyncio.gather(*taskdonwloads)
    await asyncio.sleep(0.1)

async def ranklistdownload(mode,date,p=1):
    utils.check_date(date)
    utils.check_p(p)
    path=str(config.path)+f"/每日榜单-{date}-{mode}-{p}"
    pathimg=Path(path)
    ifexists=pathimg.exists()
    if ifexists:
        if utils.if_file_exist(pathimg):
            logging.error("该日期已经获取到该模式的该页码的图片")
            logging.error(f"具体图片文件地址:{path}")
            sys.exit(0)
        else:
            logging.error(f"请手动删除该文件夹:{path} 并切换为稳定节点重试")
            sys.exit(0)
    else:
        pathimg.mkdir(parents=True, exist_ok=True)
        async with download.RankingListDownloader() as downloader:
            ids=await downloader.getrankinglistillustid(mode,date,p)
            await down(ids,downloader,path)
        
async def defaultdownload():
    yesterday=utils.return_yesterday()
    path=str(config.path)+f"/每日榜单-{yesterday}"
    pathimg=Path(path)
    ifexists=pathimg.exists()
    if ifexists:
        if utils.if_file_exist(pathimg):
            logging.error("今天已经获取过图片了")
            logging.error(f"具体图片文件地址:{path}")
            sys.exit(0)
        else:
            logging.error(f"请手动删除该文件夹:{path} 并切换为稳定节点重试")
            sys.exit(0)
    else:
        pathimg.mkdir(parents=True, exist_ok=True)
        async with download.DefaultDownloader() as downloader:
            ids=await downloader.getrankinglistillustid()
            await down(ids,downloader,path)

async def tagdownload(tag,p):
    date=datetime.now().date().strftime("%Y%m%d")
    path=str(config.path)+f"/{tag}_{date}_{p}"
    pathimg=Path(path)
    ifexists=pathimg.exists()
    if ifexists:
        if utils.if_file_exist(pathimg):
            logging.error("该tag{tag}的第{p}页图片已经获取了")
            logging.error(f"具体图片文件地址:{path}")
            sys.exit(0)
        else:
            logging.error(f"请手动删除该文件夹:{path} 并切换为稳定节点重试")
            sys.exit(0)
    else:
        pathimg.mkdir(parents=True, exist_ok=True)
        async with download.TagDownloader() as downloader:
            ids=await downloader.gettagillustid(tag,p)
            if ids==False:
                pathimg.rmdir()
                sys.exit(1)
            await down1(ids,downloader,path)

async def authordownload(uid,num):
    date=datetime.now().date().strftime("%Y%m%d")
    path=str(config.path)+f"/{uid}_{date}_{num}"
    pathimg=Path(path)
    ifexists=pathimg.exists()
    if ifexists:
        if utils.if_file_exist(pathimg):
            logging.error(f"该作者的前{num}张图片已经获取了")
            logging.error(f"具体图片文件地址:{path}")
            sys.exit(0)
        else:
            logging.error(f"请手动删除该文件夹:{path} 并切换为稳定节点重试")
            sys.exit(0)
    else:
        pathimg.mkdir(parents=True, exist_ok=True)
        async with download.AuthorDownloader() as downloader:
            ids=await downloader.getauthorillustid(uid,num)
            if ids==False:
                pathimg.rmdir()
                return
            await down(ids,downloader,path)



def cli():
    utils.if_ready()
    parser=argparse.ArgumentParser(description='Pixiv 爬虫工具')
    subparsers=parser.add_subparsers(dest="mode",help="下载模式")
    # 1. 日榜
    daily_parser = subparsers.add_parser('daily', help='获取日榜')
    daily_parser.add_argument('--date', required=True, help='日期 YYYYMMDD')
    daily_parser.add_argument('--page', default='1', help='页码')

    # 2. R18日榜
    daily_r18_parser = subparsers.add_parser('daily_r18', help='获取R18日榜')
    daily_r18_parser.add_argument('--date', required=True, help='日期 YYYYMMDD')
    daily_r18_parser.add_argument('--page', default='1', help='页码')

    # 3. 作者
    author_parser = subparsers.add_parser('author', help='下载作者作品')
    author_parser.add_argument('--uid', required=True, help='作者ID')
    author_parser.add_argument('--num', default='10', help='获取作品数量')

    # 4. 标签
    tag_parser = subparsers.add_parser('tag', help='按标签搜索')
    tag_parser.add_argument('--tag', required=True, help='标签名')
    tag_parser.add_argument('--page', default='1', help='页码')

    # 5. 默认（昨天日榜）
    subparsers.add_parser('default', help='日榜前50')


    args = parser.parse_args()

    # 根据模式调用对应的下载函数
    if args.mode == 'daily':
        asyncio.run(ranklistdownload(args.mode,args.date,args.page))
    elif args.mode == 'daily_r18':
        asyncio.run(ranklistdownload(args.mode,args.date,args.page))
    elif args.mode == 'author':
        asyncio.run(authordownload(args.uid, args.num))
    elif args.mode == 'tag':
        asyncio.run(tagdownload(args.tag, args.page))
    elif args.mode == 'default':
        asyncio.run(defaultdownload())
    else:
        parser.print_help()

        
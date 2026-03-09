from pathlib import Path
from asyncio_pixiv_download import config
from asyncio_pixiv_download import utils
import asyncio 
import httpx
import logging
import aiofiles


class Illust():
    def __init__(self,id,count,type,bookmarkCount,originalurl):
        self.id=id
        self.count=count
        self.type=type
        self.bookmarkCount=bookmarkCount
        self.originalurl=originalurl


class BaseDownloader():
    def __init__(self):
            self.proxies=config.proxy
            self.headers=config.header
            self.cookies=config.cookies
            self.max_retries=config.max_retries
            self.semaphore=asyncio.Semaphore(10)
            self.illust_api_url="https://www.pixiv.net/ajax/illust/"

    async def __aenter__(self):
         self.client=httpx.AsyncClient(proxy=self.proxies,headers=self.headers,cookies=self.cookies,timeout=10.0)
         return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
        return False
         

    async def getillustdata(self,id):#作品id一定存在
         url=self.illust_api_url+str(id)
         async with self.semaphore:
              res=await self.client.get(url)
              data=res.json()
              originalurl=data["body"]["urls"]["original"]
              count=data["body"]["pageCount"]
              type=data["body"]["illustType"]
              bookmarkCount=data["body"]["bookmarkCount"]
              return Illust(id,count,type,bookmarkCount,originalurl)
    
    async def downloadillust(self,url,pathillust,illust,i=0):#作品url一定存在
         max_tries=3
         temp=0
         while temp<max_tries:
               temp+=1
               try:
                    async with self.semaphore:
                         async with self.client.stream("GET",url) as res:
                              async with aiofiles.open(pathillust,"wb") as f:
                                   async for chunk in res.aiter_bytes(chunk_size=1024):
                                        await f.write(chunk) 
                              logging.info(f"✓ id为{illust.id}_{i}的作品下载成功")
                              return
               except Exception as e:
                    if temp>max_tries:
                         logging.error(f"id为{illust.id}_{i}的作品下载失败:{e}")
                         return 
                    else:
                         logging.warning(f"id为{illust.id}的作品下载失败 (尝试{temp}/{max_tries}): {e}")
     
    async def downloadportfolio(self,url,pathportfolio,illust):#作品url一定存在
         countillusts=illust.count
         tasks=[]
         for i in range(countillusts):
              url=utils.nextillustturl(url,i)
              pathillust=pathportfolio+f"/{illust.id}_{i}.jpg"
              tasks.append(asyncio.create_task(self.downloadillust(url,pathillust,illust,i)))
         await asyncio.gather(*tasks)
                   
    
    
         

class AuthorDownloader(BaseDownloader):

    def __init__(self):
         super().__init__()

    async def getauthorillustid(self,uid,num):
              url=f"https://www.pixiv.net/ajax/user/{uid}/profile/all"
              res=await self.client.get(url)
              data=res.json()
              if int(num)<=0:
                   logging.error("数量不能小于等于0")
                   return False
              if data["error"]=="true":#作者不一定存在
                    logging.error(f"不存在uid为{uid}的作者")
                    return False
              else:
                try:
                    count=int(num)
                    if count>len(data["body"]["illusts"]):
                         count=len(data["body"]["illusts"])
                    ids=list(data["body"]["illusts"].keys())[:count]
                    print(ids)
                    return ids
                except Exception as e:#作者不一定有作品
                     print(data["body"]["illusts"])
                     logging.error(f"uid为{uid}的作者没有作品:{e}")
                     return False
              

class TagDownloader(BaseDownloader):
     def __init__(self):
          super().__init__()
     async def gettagillustid(self,tag,p):
               url=f"https://www.pixiv.net/ajax/search/artworks/{tag}?order=date_d&mode=safe&p={p}&csw=1&s_mode=s_tag&type=all&lang=zh"
               res=await self.client.get(url)
               data=res.json()
               if int(p)<=0:
                    logging.error(f"页码错误 {p}")
                    return False
               lastPage=data["body"]["illustManga"]["lastPage"]
               if int(p)>int(lastPage):#页码错误
                    logging.error(f"页码太大了 {p}")
                    return False
               total=data["body"]["illustManga"]["total"]
               if int(total)==0:
                    logging.error(f"没有关于{tag}的作品")
                    return False
               else:
                    length=len(data["body"]["illustManga"]["data"])
                    ids=[data["body"]["illustManga"]["data"][i]["id"] for i in range(length)]
                    return ids
     async def findhotillust(self,illust):
          if int(illust.bookmarkCount) >=200:
               return illust





class RankingListDownloader(BaseDownloader):
     def __init__(self):
          super().__init__()

     async def getrankinglistillustid(self,mode,date,p=1):
               url=f"https://www.pixiv.net/ranking.php?mode={mode}&date={date}&format=json&p={p}"
               res=await self.client.get(url) 
               data=res.json()
               length=len(data["contents"])
               ids=[data["contents"][i]["illust_id"] for i in range(length)]
               return ids

class DefaultDownloader(BaseDownloader):
     def __init__(self):
          super().__init__()
     
     async def getrankinglistillustid(self):
               url=f"https://www.pixiv.net/ranking.php?mode=daily&format=json&p=1"
               res=await self.client.get(url)
               data=res.json()
               length=len(data["contents"])
               ids=[data["contents"][i]["illust_id"] for i in range(length)]
               return ids


         
         
